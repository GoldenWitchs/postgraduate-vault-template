from __future__ import annotations

import argparse
import json
import os
from html.parser import HTMLParser
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, Sequence
from urllib.parse import unquote

import yaml


@dataclass(frozen=True)
class Finding:
    level: str
    code: str
    path: str
    message: str


REQUIRED_FILES = (
    "AGENTS.md",
    ".agents/skills/research-vault-harness/SKILL.md",
    ".claudian/claudian-settings.json",
    "_system/AI-Harness/INDEX.md",
    "_system/AI-Harness/个人协作档案.md",
    "_system/AI-Harness/契约与验证规则.md",
    "_system/AI-Harness/quality/检查清单.md",
    "_system/AI-Harness/memory/工作日志.jsonl",
    "_system/AI-Harness/memory/偏好候选.jsonl",
    "_system/AI-Harness/memory/失败与纠正.jsonl",
)

HARNESS_MARKDOWN = (
    "_system/AI-Harness/INDEX.md",
    "_system/AI-Harness/个人协作档案.md",
    "_system/AI-Harness/契约与验证规则.md",
    "_system/AI-Harness/quality/检查清单.md",
)

MEMORY_LOGS = (
    "_system/AI-Harness/memory/工作日志.jsonl",
    "_system/AI-Harness/memory/偏好候选.jsonl",
    "_system/AI-Harness/memory/失败与纠正.jsonl",
)

TASK_FILES = ("TASK.md", "evidence.md", "verification.md", "log.jsonl")

OBSIDIAN_MATH_POLICY_MARKERS = (
    "$...$",
    "$$...$$",
    r"\(...\)",
    r"\[...\]",
    r"\\",
)


class ArtifactHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.paired_note: Optional[str] = None
        self.resources: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        values = {key.casefold(): value for key, value in attrs}
        if tag.casefold() == "meta" and (values.get("name") or "").casefold() == "paired_note":
            self.paired_note = values.get("content")
        for attribute in ("src", "href"):
            value = values.get(attribute)
            if value:
                self.resources.append(value)


def finding(code: str, path: Path | str, message: str, level: str = "error") -> Finding:
    return Finding(level=level, code=code, path=Path(path).as_posix(), message=message)


def has_obsidian_math_policy(text: str) -> bool:
    return all(marker in text for marker in OBSIDIAN_MATH_POLICY_MARKERS)


def read_frontmatter(path: Path) -> tuple[Optional[dict[str, Any]], Optional[str]]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return None, f"cannot read UTF-8 Markdown: {exc}"
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "missing opening YAML frontmatter delimiter"
    try:
        end = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return None, "missing closing YAML frontmatter delimiter"
    try:
        data = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as exc:
        return None, f"invalid YAML frontmatter: {exc}"
    if not isinstance(data, dict):
        return None, "frontmatter must be a YAML mapping"
    return data, None


def is_within(root: Path, candidate: Path) -> bool:
    try:
        return os.path.commonpath((str(root.resolve()), str(candidate.resolve()))) == str(root.resolve())
    except (OSError, ValueError):
        return False


def validate_required_files(vault: Path) -> list[Finding]:
    results: list[Finding] = []
    for relative in REQUIRED_FILES:
        if not (vault / relative).is_file():
            results.append(finding("required-file-missing", relative, "required Harness file is missing"))
    for relative in ("_system/AI-Harness/tasks/active", "_system/AI-Harness/tasks/completed"):
        if not (vault / relative).is_dir():
            results.append(finding("required-directory-missing", relative, "required task directory is missing"))
    agents = vault / "AGENTS.md"
    if agents.is_file() and agents.stat().st_size > 32768:
        results.append(
            finding("agents-too-large", "AGENTS.md", "AGENTS.md exceeds Codex's default 32 KiB project-doc budget")
        )
    if agents.is_file():
        try:
            agents_text = agents.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            results.append(finding("agents-read-invalid", "AGENTS.md", str(exc)))
        else:
            if not has_obsidian_math_policy(agents_text):
                results.append(
                    finding(
                        "agents-math-policy-missing",
                        "AGENTS.md",
                        "Vault rules must require Obsidian dollar math delimiters and matrix row breaks",
                    )
                )
    return results


def validate_harness_frontmatter(vault: Path) -> list[Finding]:
    results: list[Finding] = []
    for relative in HARNESS_MARKDOWN:
        path = vault / relative
        if not path.is_file():
            continue
        _, error = read_frontmatter(path)
        if error:
            results.append(finding("frontmatter-invalid", relative, error))
    return results


def validate_jsonl(path: Path, vault: Path) -> list[Finding]:
    results: list[Finding] = []
    if not path.is_file():
        return results
    relative = path.relative_to(vault)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        return [finding("jsonl-invalid", relative, f"cannot read JSONL: {exc}")]
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            results.append(finding("jsonl-invalid", relative, f"line {line_number}: {exc.msg}"))
            continue
        if not isinstance(record, dict):
            results.append(finding("jsonl-invalid", relative, f"line {line_number}: record must be an object"))
            continue
        missing = [key for key in ("schema_version", "type", "timestamp") if key not in record]
        if missing:
            results.append(
                finding("jsonl-schema-invalid", relative, f"line {line_number}: missing {', '.join(missing)}")
            )
    return results


def validate_logs(vault: Path) -> list[Finding]:
    results: list[Finding] = []
    for relative in MEMORY_LOGS:
        results.extend(validate_jsonl(vault / relative, vault))
    for state in ("active", "completed"):
        root = vault / "_system/AI-Harness/tasks" / state
        if not root.is_dir():
            continue
        for child in root.iterdir():
            if not child.is_dir() or child.name.startswith("."):
                continue
            for name in TASK_FILES:
                target = child / name
                if not target.is_file() or target.stat().st_size == 0:
                    results.append(
                        finding(
                            "task-file-missing",
                            target.relative_to(vault),
                            f"{state} task must contain a non-empty {name}",
                        )
                    )
            expected_types = {
                "TASK.md": "ai-harness-task",
                "evidence.md": "ai-harness-task-evidence",
                "verification.md": "ai-harness-task-verification",
            }
            for name, expected_type in expected_types.items():
                target = child / name
                if not target.is_file() or target.stat().st_size == 0:
                    continue
                metadata, error = read_frontmatter(target)
                if error or not metadata:
                    results.append(
                        finding("task-frontmatter-invalid", target.relative_to(vault), error or "missing mapping")
                    )
                    continue
                problems: list[str] = []
                if metadata.get("type") != expected_type:
                    problems.append(f"type must be {expected_type}")
                if metadata.get("task_id") != child.name:
                    problems.append(f"task_id must be {child.name}")
                status = metadata.get("status")
                allowed_statuses = {"active", "in-progress", "review"} if state == "active" else {"completed"}
                if status not in allowed_statuses:
                    problems.append(f"status must be one of {sorted(allowed_statuses)}")
                if name == "TASK.md" and metadata.get("level") not in {"L0", "L1", "L2", "L3"}:
                    problems.append("level must be L0, L1, L2, or L3")
                if problems:
                    results.append(
                        finding("task-frontmatter-invalid", target.relative_to(vault), "; ".join(problems))
                    )
            results.extend(validate_jsonl(child / "log.jsonl", vault))
    return results


def iter_artifact_notes(vault: Path) -> list[Path]:
    notes: list[Path] = []
    for relative in ("00-Inbox/AI-Drafts", "30-Knowledge/Literature"):
        root = vault / relative
        if root.is_dir():
            notes.extend(path for path in root.rglob("*.md") if path.is_file())
    return notes


def is_external_resource(value: str) -> bool:
    lowered = value.strip().casefold()
    return lowered.startswith(("http://", "https://", "mailto:", "data:", "#"))


def decode_local_path(value: str) -> str:
    without_fragment = value.split("#", 1)[0].split("?", 1)[0]
    return unquote(without_fragment).replace("\\", "/")


def parse_html(path: Path) -> tuple[Optional[ArtifactHTMLParser], Optional[str]]:
    parser = ArtifactHTMLParser()
    try:
        parser.feed(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as exc:
        return None, f"cannot read UTF-8 HTML: {exc}"
    return parser, None


def resolve_reference(vault: Path, base: Path, value: str) -> Optional[Path]:
    decoded = Path(decode_local_path(value))
    if decoded.is_absolute():
        return None
    for candidate in (vault / decoded, base / decoded):
        if is_within(vault, candidate) and candidate.exists():
            return candidate.resolve()
    return None


def validate_html_resources(vault: Path, html: Path, parser: ArtifactHTMLParser) -> list[Finding]:
    results: list[Finding] = []
    for resource in parser.resources:
        if resource.strip().casefold().startswith("javascript:"):
            results.append(
                finding("html-unsafe-resource", html.relative_to(vault), "javascript: URLs are not allowed")
            )
            continue
        if is_external_resource(resource):
            continue
        resource_path = html.parent / decode_local_path(resource)
        if not is_within(vault, resource_path):
            results.append(finding("html-resource-outside-vault", html.relative_to(vault), resource))
        elif not resource_path.exists():
            results.append(finding("html-resource-missing", html.relative_to(vault), resource))
    return results


def validate_artifacts(vault: Path) -> list[Finding]:
    results: list[Finding] = []
    checked_html: set[Path] = set()
    for note in iter_artifact_notes(vault):
        metadata, error = read_frontmatter(note)
        if error or not metadata:
            continue
        artifact = metadata.get("html_artifact")
        if artifact is None:
            continue
        note_relative = note.relative_to(vault).as_posix()
        if not isinstance(artifact, str) or not artifact.strip():
            results.append(finding("html-artifact-invalid", note.relative_to(vault), "html_artifact must be a path string"))
            continue
        html = vault / artifact
        if Path(artifact).is_absolute() or not is_within(vault, html):
            results.append(finding("html-artifact-outside-vault", note.relative_to(vault), artifact))
            continue
        if not html.is_file():
            results.append(finding("html-artifact-missing", note.relative_to(vault), artifact))
            continue
        checked_html.add(html.resolve())
        parser, parse_error = parse_html(html)
        if parse_error or parser is None:
            results.append(finding("html-read-invalid", html.relative_to(vault), parse_error or "unknown error"))
            continue
        if not parser.paired_note:
            results.append(finding("paired-note-missing", html.relative_to(vault), "paired_note meta tag is missing"))
        else:
            paired_value = decode_local_path(parser.paired_note)
            paired_path = Path(paired_value)
            candidates = (vault / paired_path, html.parent / paired_path)
            note_resolved = note.resolve()
            matched = any(
                not paired_path.is_absolute()
                and is_within(vault, candidate)
                and candidate.resolve() == note_resolved
                for candidate in candidates
            )
            if not matched:
                results.append(
                    finding(
                        "paired-note-mismatch",
                        html.relative_to(vault),
                        f"paired_note={parser.paired_note!r}, expected {note_relative!r}",
                    )
                )
        results.extend(validate_html_resources(vault, html, parser))

    html_root = vault / "40-Sources/AI-HTML"
    if html_root.is_dir():
        for html in (path for path in html_root.rglob("*.html") if path.is_file()):
            if html.resolve() in checked_html:
                continue
            parser, parse_error = parse_html(html)
            if parse_error or parser is None:
                results.append(finding("html-read-invalid", html.relative_to(vault), parse_error or "unknown error"))
                continue
            if not parser.paired_note:
                results.append(
                    finding("paired-note-missing", html.relative_to(vault), "paired_note meta tag is missing")
                )
            else:
                paired = resolve_reference(vault, html.parent, parser.paired_note)
                if paired is None or not paired.is_file():
                    results.append(
                        finding(
                            "paired-note-target-missing",
                            html.relative_to(vault),
                            f"paired_note target does not exist: {parser.paired_note}",
                        )
                    )
                else:
                    metadata, frontmatter_error = read_frontmatter(paired)
                    declared = metadata.get("html_artifact") if metadata else None
                    declared_path = vault / declared if isinstance(declared, str) else None
                    if (
                        frontmatter_error
                        or declared_path is None
                        or not is_within(vault, declared_path)
                        or declared_path.resolve() != html.resolve()
                    ):
                        results.append(
                            finding(
                                "html-backlink-mismatch",
                                html.relative_to(vault),
                                "paired Markdown must point back with html_artifact",
                            )
                        )
            results.extend(validate_html_resources(vault, html, parser))
    return results


def validate_claudian(vault: Path) -> list[Finding]:
    path = vault / ".claudian/claudian-settings.json"
    if not path.is_file():
        return []
    try:
        settings = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [finding("claudian-settings-invalid", path.relative_to(vault), str(exc))]
    results: list[Finding] = []
    permission_mode = settings.get("permissionMode")
    saved_mode = (settings.get("savedProviderPermissionMode") or {}).get("codex")
    allowed_permission_modes = {"normal", "yolo"}
    if (
        permission_mode not in allowed_permission_modes
        or saved_mode not in allowed_permission_modes
        or permission_mode != saved_mode
    ):
        results.append(
            finding(
                "claudian-permission-invalid",
                path.relative_to(vault),
                "both Codex permission fields must match and be either normal or yolo",
            )
        )
    safe_mode = ((settings.get("providerConfigs") or {}).get("codex") or {}).get("safeMode")
    if safe_mode != "workspace-write":
        results.append(
            finding("claudian-sandbox-invalid", path.relative_to(vault), "Codex safeMode must remain workspace-write")
        )
    persistent = settings.get("persistentExternalContextPaths")
    if persistent != []:
        results.append(
            finding("claudian-persistent-context", path.relative_to(vault), "persistentExternalContextPaths must stay empty")
        )
    prompt = settings.get("systemPrompt")
    if not isinstance(prompt, str) or not prompt.strip() or len(prompt) > 2000:
        results.append(
            finding("claudian-bootstrap-invalid", path.relative_to(vault), "systemPrompt must be a non-empty bootstrap under 2000 characters")
        )
    if isinstance(prompt, str) and prompt.strip() and not has_obsidian_math_policy(prompt):
        results.append(
            finding(
                "claudian-math-policy-missing",
                path.relative_to(vault),
                "systemPrompt must require Obsidian dollar math delimiters and matrix row breaks",
            )
        )
    return results


def validate_vault(vault: Path) -> list[Finding]:
    """Return deterministic validation findings for a Vault harness."""
    root = vault.resolve()
    results: list[Finding] = []
    results.extend(validate_required_files(root))
    results.extend(validate_harness_frontmatter(root))
    results.extend(validate_logs(root))
    results.extend(validate_artifacts(root))
    results.extend(validate_claudian(root))
    return results


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the Research Vault Harness deterministically.")
    parser.add_argument("--vault", type=Path, default=Path.cwd(), help="Vault root (default: current directory)")
    args = parser.parse_args(argv)
    findings = validate_vault(args.vault)
    for item in findings:
        print(f"{item.level.upper()} [{item.code}] {item.path}: {item.message}")
    errors = [item for item in findings if item.level == "error"]
    if errors:
        print(f"FAIL: {len(errors)} error(s), {len(findings) - len(errors)} warning(s)")
        return 1
    print(f"PASS: 0 errors, {len(findings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
