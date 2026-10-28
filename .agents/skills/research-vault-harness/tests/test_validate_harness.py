from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from validate_harness import validate_vault


def write(path: Path, text: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def valid_frontmatter(doc_type: str) -> str:
    return f"---\ntype: {doc_type}\nstatus: active\n---\n\n# Fixture\n"


def make_valid_fixture(root: Path) -> Path:
    math_policy = (
        r"Math uses $...$ inline and standalone $$...$$ blocks; "
        r"never \(...\) or \[...\]; matrix rows use \\."
    )
    write(root / "AGENTS.md", f"# Fixture Vault Rules\n\n{math_policy}\n")
    write(
        root / ".agents/skills/research-vault-harness/SKILL.md",
        "---\nname: research-vault-harness\ndescription: fixture description long enough for validation\n---\n",
    )
    write(root / "_system/AI-Harness/INDEX.md", valid_frontmatter("ai-harness-index"))
    write(root / "_system/AI-Harness/个人协作档案.md", valid_frontmatter("ai-profile"))
    write(root / "_system/AI-Harness/契约与验证规则.md", valid_frontmatter("ai-contract"))
    write(root / "_system/AI-Harness/quality/检查清单.md", valid_frontmatter("checklist"))

    record = json.dumps(
        {
            "schema_version": 1,
            "type": "schema",
            "timestamp": "2026-08-10T00:00:00+08:00",
        },
        ensure_ascii=False,
    )
    for name in ("工作日志.jsonl", "偏好候选.jsonl", "失败与纠正.jsonl"):
        write(root / "_system/AI-Harness/memory" / name, record + "\n")

    (root / "_system/AI-Harness/tasks/active").mkdir(parents=True)
    (root / "_system/AI-Harness/tasks/completed").mkdir(parents=True)

    note_path = "00-Inbox/AI-Drafts/paper.md"
    html_path = "40-Sources/AI-HTML/paper/index.html"
    write(
        root / note_path,
        f"---\nstatus: ai-draft\nhtml_artifact: {html_path}\n---\n\n# Paper\n",
    )
    write(
        root / html_path,
        '<!doctype html><meta name="paired_note" '
        f'content="{note_path}"><title>Paper</title>',
    )

    settings = {
        "permissionMode": "normal",
        "systemPrompt": (
            "Follow the Vault AGENTS.md and load the harness on demand. "
            + math_policy
        ),
        "persistentExternalContextPaths": [],
        "providerConfigs": {"codex": {"safeMode": "workspace-write"}},
        "savedProviderPermissionMode": {"codex": "normal"},
    }
    write(
        root / ".claudian/claudian-settings.json",
        json.dumps(settings, ensure_ascii=False, indent=2) + "\n",
    )
    return root


def error_codes(vault: Path) -> set[str]:
    return {item.code for item in validate_vault(vault) if item.level == "error"}


class HarnessValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.vault = make_valid_fixture(Path(self.temporary.name))

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_valid_fixture_passes(self) -> None:
        self.assertEqual(set(), error_codes(self.vault))

    def test_missing_required_file_fails(self) -> None:
        (self.vault / "_system/AI-Harness/INDEX.md").unlink()
        self.assertIn("required-file-missing", error_codes(self.vault))

    def test_invalid_jsonl_fails(self) -> None:
        path = self.vault / "_system/AI-Harness/memory/偏好候选.jsonl"
        path.write_text("{invalid}\n", encoding="utf-8")
        self.assertIn("jsonl-invalid", error_codes(self.vault))

    def test_incomplete_active_task_fails(self) -> None:
        (self.vault / "_system/AI-Harness/tasks/active/demo").mkdir()
        self.assertIn("task-file-missing", error_codes(self.vault))

    def test_missing_html_artifact_fails(self) -> None:
        note = self.vault / "00-Inbox/AI-Drafts/paper.md"
        note.write_text(
            "---\nstatus: ai-draft\n"
            "html_artifact: 40-Sources/AI-HTML/missing/index.html\n---\n",
            encoding="utf-8",
        )
        self.assertIn("html-artifact-missing", error_codes(self.vault))

    def test_mismatched_paired_note_fails(self) -> None:
        html = self.vault / "40-Sources/AI-HTML/paper/index.html"
        html.write_text(
            '<!doctype html><meta name="paired_note" content="wrong.md">',
            encoding="utf-8",
        )
        self.assertIn("paired-note-mismatch", error_codes(self.vault))

    def test_html_relative_pair_and_url_encoded_resource_passes(self) -> None:
        old_note = self.vault / "00-Inbox/AI-Drafts/paper.md"
        new_note = self.vault / "00-Inbox/AI-Drafts/paper note.md"
        old_note.replace(new_note)
        html = self.vault / "40-Sources/AI-HTML/paper/index.html"
        html.write_text(
            '<!doctype html><meta name="paired_note" '
            'content="../../../00-Inbox/AI-Drafts/paper note.md">'
            '<a href="../../../00-Inbox/AI-Drafts/paper%20note.md">note</a>',
            encoding="utf-8",
        )
        self.assertEqual(set(), error_codes(self.vault))

    def test_javascript_resource_fails(self) -> None:
        html = self.vault / "40-Sources/AI-HTML/paper/index.html"
        html.write_text(
            '<!doctype html><meta name="paired_note" '
            'content="00-Inbox/AI-Drafts/paper.md">'
            '<a href="javascript:alert(1)">unsafe</a>',
            encoding="utf-8",
        )
        self.assertIn("html-unsafe-resource", error_codes(self.vault))

    def test_orphan_html_fails(self) -> None:
        write(
            self.vault / "40-Sources/AI-HTML/orphan/index.html",
            "<!doctype html><title>Orphan</title>",
        )
        self.assertIn("paired-note-missing", error_codes(self.vault))

    def test_task_frontmatter_must_match_directory(self) -> None:
        task = self.vault / "_system/AI-Harness/tasks/active/demo"
        write(task / "TASK.md", "# no frontmatter\n")
        write(task / "evidence.md", valid_frontmatter("ai-harness-task-evidence"))
        write(task / "verification.md", valid_frontmatter("ai-harness-task-verification"))
        write(
            task / "log.jsonl",
            '{"schema_version":1,"type":"task_created",'
            '"timestamp":"2026-08-10T00:00:00+08:00"}\n',
        )
        self.assertIn("task-frontmatter-invalid", error_codes(self.vault))

    def test_consistent_yolo_permission_passes(self) -> None:
        path = self.vault / ".claudian/claudian-settings.json"
        settings = json.loads(path.read_text(encoding="utf-8"))
        settings["permissionMode"] = "yolo"
        settings["savedProviderPermissionMode"]["codex"] = "yolo"
        path.write_text(json.dumps(settings), encoding="utf-8")
        self.assertEqual(set(), error_codes(self.vault))

    def test_inconsistent_permission_modes_fail(self) -> None:
        path = self.vault / ".claudian/claudian-settings.json"
        settings = json.loads(path.read_text(encoding="utf-8"))
        settings["permissionMode"] = "yolo"
        settings["savedProviderPermissionMode"]["codex"] = "normal"
        path.write_text(json.dumps(settings), encoding="utf-8")
        self.assertIn("claudian-permission-invalid", error_codes(self.vault))

    def test_unknown_permission_mode_fails(self) -> None:
        path = self.vault / ".claudian/claudian-settings.json"
        settings = json.loads(path.read_text(encoding="utf-8"))
        settings["permissionMode"] = "unknown"
        settings["savedProviderPermissionMode"]["codex"] = "unknown"
        path.write_text(json.dumps(settings), encoding="utf-8")
        self.assertIn("claudian-permission-invalid", error_codes(self.vault))

    def test_missing_agents_math_policy_fails(self) -> None:
        (self.vault / "AGENTS.md").write_text("# Fixture Vault Rules\n", encoding="utf-8")
        self.assertIn("agents-math-policy-missing", error_codes(self.vault))

    def test_missing_claudian_math_policy_fails(self) -> None:
        path = self.vault / ".claudian/claudian-settings.json"
        settings = json.loads(path.read_text(encoding="utf-8"))
        settings["systemPrompt"] = "Follow the Vault AGENTS.md."
        path.write_text(json.dumps(settings), encoding="utf-8")
        self.assertIn("claudian-math-policy-missing", error_codes(self.vault))

    def test_invalid_harness_frontmatter_fails(self) -> None:
        path = self.vault / "_system/AI-Harness/契约与验证规则.md"
        path.write_text("---\ntype: [broken\n---\n", encoding="utf-8")
        self.assertIn("frontmatter-invalid", error_codes(self.vault))


if __name__ == "__main__":
    unittest.main()
