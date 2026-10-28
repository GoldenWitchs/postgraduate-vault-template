---
name: research-vault-harness
description: Use when working in this Obsidian research Vault on literature reading or summarization, paired Markdown/HTML artifacts, multi-file or cross-session tasks, formal knowledge promotion, durable preference updates, failure review, or Harness validation. Applies scoped just-in-time retrieval, evidence discipline, file-backed task state, risk-adaptive verification, and controlled write boundaries.
---

# Research Vault Harness

Use the Vault as the source of truth without loading it wholesale.

## Start

1. Read the root `AGENTS.md` if it is not already in context.
2. Read `_system/AI-Harness/INDEX.md`.
3. Classify the request as L0–L3 using `_system/AI-Harness/契约与验证规则.md` when the task writes files, spans sessions, updates memory, or has unclear boundaries.
4. Read `个人协作档案.md` only when a confirmed preference is relevant.
5. Reuse an existing `tasks/active/<task-id>/` before creating a new task.

## Retrieve Just in Time

- Begin with the current note, selection, user-mentioned files, citekey, title, Properties, Wikilinks, and exact terms.
- Read roughly 5–8 high-signal files on the first pass. Narrow excessive results; expand only when evidence is inadequate.
- Exclude `.claudian/sessions/`, attachments, archives, and unrelated generated HTML unless the request needs them.
- Store paths and concise evidence in task files instead of copying large source bodies.

## Route State and Writes

- Keep L0 questions lightweight; do not create task state or memory records.
- For L2/L3, multi-file, or cross-session work, maintain `TASK.md`, `evidence.md`, `verification.md`, and append-only `log.jsonl` under `tasks/active/<task-id>/`.
- Start each task Markdown file with YAML containing the exact `task_id`, an allowed `status`, and its type: `ai-harness-task`, `ai-harness-task-evidence`, or `ai-harness-task-verification`; `TASK.md` also requires `level: L0|L1|L2|L3`. Use `active`/`in-progress`/`review` under `tasks/active/` and `completed` after archival.
- Write new Markdown to `00-Inbox/AI-Drafts/` and task-related HTML packages to `40-Sources/AI-HTML/`.
- Do not modify `30-Knowledge/`, locked rules/configuration, or move/delete existing material without explicit current authorization.

## Handle Literature

- Treat Zotero or the primary paper/book as the bibliographic and factual authority.
- Never invent DOI, citekey, page, section, figure, equation, table, or experimental value. Mark unverifiable claims as `未核验`.
- Separate author claims, source evidence, AI explanation, user judgment, and open questions.
- Produce paired Markdown and HTML when requested. Set Markdown `html_artifact`; set HTML `<meta name="paired_note">`; keep local CSS/images/scripts with the HTML package.
- Leave the user's judgment for the user unless they explicitly confirm a proposed statement.

## Learn Preferences Carefully

- When the user explicitly states a durable preference (`记住`, `以后都这样`, or equivalent), update `个人协作档案.md` with date and source.
- Put inferred preferences only in `memory/偏好候选.jsonl`; promote them only after confirmation.
- Append corrections and repeated failure patterns to `memory/失败与纠正.jsonl`. Never rewrite prior JSONL lines.
- Do not store secrets, transient task demands, emotion, or sensitive inferences as durable memory.

## Verify and Stop

- Select checks by risk. Verify claims, source fidelity, file formats, links, pairing, permissions, and rollback only where applicable.
- Run this after Harness, task-state, Claudian-setting, or paired-artifact changes:

```powershell
python .agents\skills\research-vault-harness\scripts\validate_harness.py --vault .
```

- Repair only failed checks and rerun the affected validation. Stop as soon as the task's completion conditions pass.
- If evidence conflicts or cannot be obtained, preserve the uncertainty and report it instead of looping or guessing.
