---
type: schema
status: active
created: 2026-08-07
tags: [system, properties]
---

# Properties 规范

## 通用字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `type` | text | 笔记类型，使用下表固定值 |
| `status` | text | 生命周期状态 |
| `topics` | list | 主题名称，保持少量、稳定 |
| `projects` | list | 关联项目 |
| `created` | date | 创建日期 |
| `updated` | date | 最近实质更新日期 |

## type 值

`overview`、`project`、`literature`、`concept`、`method`、`dataset`、`experiment`、`html-source`、`web-source`、`weekly-review`、`guide`、`workflow`、`schema`、`health`

## status 值

`inbox` → `reading` → `ai-draft` → `verified` → `evergreen` → `archived`

项目可额外使用：`active`、`paused`、`completed`、`cancelled`。

## 文献字段

| 字段 | 说明 |
| --- | --- |
| `citekey` | 稳定引用键，也是文件名前缀 |
| `doi` | DOI；不确定时留空，不猜测 |
| `zotero_uri` | 返回 Zotero 条目的链接 |
| `source_file` | PDF 或来源标识，不强制复制 PDF |
| `html_artifact` | 配套 HTML 入口 |
| `evidence_checked` | 是否对照原文核验关键论断 |

## 实验字段

`experiment_id`、`project`、`hypothesis`、`dataset`、`code_repo`、`environment`、`seed`、`metrics`、`result`、`related_literature`

## 使用原则

- Properties 用于稳定、可查询的结构；Wikilink 用于语义关系；标签只用于少量横向主题。
- 不为一次性信息创建字段，不同时维护同义字段。
- `status` 不放进 tags；项目或主题不通过复制目录表达。

