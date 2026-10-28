---
type: workflow
status: active
created: 2026-08-07
tags: [system, ai, literature]
---

# AI 论文阅读工作流

## 1. 输入

- Zotero 条目或原始 PDF
- citekey、DOI、题目、作者和年份
- 本次阅读目的：理解、复现、比较、找研究空白或服务某个项目

## 2. AI 草稿

AI 同时生成：

1. `00-Inbox/AI-Drafts/<citekey> - <短标题>.md`
2. `40-Sources/AI-HTML/<citekey>/index.html`
3. 必要的 HTML 资源文件

Markdown 必须包含研究问题、方法、数据、实验设置、关键证据、局限、开放问题和 HTML 回链。HTML 必须标明来源、生成日期和“AI 生成，尚需核验”。

## 3. 证据核验

- 对关键结论定位页码、章节、图表或公式。
- 检查模型、数据集、基线和指标名称是否与原文一致。
- 检查 AI 是否把相关性写成因果、把作者推测写成实证结论。
- 无法核验的内容删除或明确标注“未核验”。

## 4. 正式入库

核验完成后：

- 将状态改为 `verified`。
- 把文献笔记移动到 `30-Knowledge/Literature/`。
- 只在具有复用价值时建立概念、方法、数据集或模型笔记。
- 在相关项目中用 Wikilink 和 `projects` 属性引用，不复制笔记。

## 5. 文件关系

```text
30-Knowledge/Literature/<citekey> - <短标题>.md
  └─ html_artifact → 40-Sources/AI-HTML/<citekey>/index.html

40-Sources/AI-HTML/<citekey>/HTML资料索引.md
  └─ paired_note → 文献笔记
```

## 6. 完成标准

- [ ] DOI、citekey 和 Zotero 链接可追溯
- [ ] 关键结论有证据位置
- [ ] AI 解释与作者原话已区分
- [ ] “我的判断”由用户本人填写或确认
- [ ] Markdown 与 HTML 双向链接
- [ ] 与至少一个研究问题、主题或项目关联

