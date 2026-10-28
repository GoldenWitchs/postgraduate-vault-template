---
type: ai-harness-index
status: active
version: 2
created: 2026-08-10
updated: 2026-09-09
tags: [system, ai, harness]
---

# AI Harness 索引

> [!info]
> 本页是导航，不是常驻上下文包。先判断任务，再读取必要文件；不要一次加载本目录全部内容。

## 路由表

| 需要 | 读取 | 何时加载 |
|---|---|---|
| 写入权限、任务级别、完成条件 | [[契约与验证规则]] | L2/L3、跨会话、正式晋升或边界不清时 |
| 已确认的协作偏好 | [[个人协作档案]] | 表达方式、长期工作习惯或偏好更新与当前任务相关时 |
| 当前长任务状态 | `tasks/active/<task-id>/` | 用户继续、恢复或检查一个已有长任务时 |
| 质量门 | [[quality/检查清单]] | 创建/修改文件、文献产物或配置时 |
| 已提炼 Lessons | [[quality/LESSONS]] | 相似错误复现、用户纠正、执行前风险检查或经验晋升评审时 |
| 候选偏好 | `memory/偏好候选.jsonl` | 评审、晋升或去重候选偏好时；不默认读取全文 |
| 已知失败与纠正 | `memory/失败与纠正.jsonl` | 相似错误复现或用户要求复盘时；先精确搜索错误类型 |
| 工作轨迹 | `memory/工作日志.jsonl` | 恢复 Harness 维护任务或审计变更时 |

## 默认检索

1. 当前笔记、选区和用户 `@` 指定文件。
2. 标题、Properties、citekey、Wikilink、反向链接和精确关键词。
3. 首轮约 5–8 个最相关文件；证据不足再扩大。
4. 默认不读 `.claudian/sessions/`、附件、归档或无关 HTML 正文。

## 入口 Skill

复杂研究、文献双载体、长期任务、偏好更新与 Harness 验证使用 `$research-vault-harness`。普通问答无需强制调用。
