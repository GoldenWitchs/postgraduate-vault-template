# Postgraduate Vault V2 · 研究生知识库架构模板

用于 Obsidian 的研究、学习和项目知识库框架，包含 AI Harness、来源核验规则、可恢复任务结构、Markdown/HTML 双载体约定及研究模板。它是一份空白架构，供你建立自己的知识库。

## 开始使用

1. 点击 GitHub **Use this template** 创建你自己的仓库，或使用 **Code → Download ZIP** 下载并解压。记录个人内容时建议使用私有仓库。
2. 在 Obsidian 中把解压后的文件夹作为现有 Vault 打开，从 [首页](首页.md) 开始。
3. 内置 Templates、Bases 等配置随库提供；模板目录是 `_templates/`。本版保留原始八种研究模板，没有添加发布者本机的每日复盘或课程配置。
4. 需要 AI 协作时，让你的助手先读取 [AGENTS.md](AGENTS.md) 和 [AI Harness 索引](_system/AI-Harness/INDEX.md)。
5. 如需 Obsidian 内 AI 面板或 Zotero 导入，请自行安装 [Claudian](https://github.com/YishenTu/claudian) 或 [Zotero Integration](https://github.com/mgmeyers/obsidian-zotero-integration)，使用自己的账号和设备配置。本仓库不附带插件程序或账号信息，社区插件默认不启用。

## 目录与流程

| 目录 | 用途 |
| --- | --- |
| `00-Inbox/` | 待处理资料、AI 草稿、网页剪藏和随手记录 |
| `10-Projects/` | 有结束条件的课程、研究、论文与实验项目 |
| `20-Areas/` | 长期维护的研究方向、能力和责任 |
| `30-Knowledge/` | 人工核验后可复用的文献、概念、方法与数据集笔记 |
| `40-Sources/` | 原始来源、网页与 HTML 讲解包 |
| `90-Archive/` | 已完成或失活内容 |
| `_system/` | 规则、Properties 规范、Bases 工作台与 AI Harness |
| `_templates/` | 原始研究模板 |
| `.agents/skills/` | Vault 协作、解释与 Obsidian 文件格式技能 |

默认流程是“来源 → AI 草稿 → 人工核验 → 知识 → 项目引用 → 归档”。个人偏好、任务进度与正式知识分开保存；阅读或听过不代表掌握，AI 不填写使用者的判断。

## 记忆与跨会话协作

- `个人协作档案.md` 是空白占位，只保存本人明确确认的偏好。
- `memory/` 三份 JSONL 初始为空，用于工作轨迹、偏好候选和纠正事件。
- `tasks/active/` 与 `tasks/completed/` 初始为空；长任务按契约创建 TASK、evidence、verification 和追加日志。
- `quality/LESSONS.md` 初始为空。没有附带任何人的背景、偏好、旧任务、学习记录或错误历史。
- Claudian 仅提供无凭据、无机器路径的通用设置：`normal`、`workspace-write`、空外部上下文路径。它不是从任一设备复制的登录配置，具体模型与 CLI 位置由使用者设置。

## 验证

验证器需要 Python 和 PyYAML；可用 uv 建立环境，或在自己的虚拟环境中安装依赖：

```sh
python -m pip install -r requirements-dev.txt
python .agents/skills/research-vault-harness/scripts/validate_harness.py --vault .
python -m unittest discover -s .agents/skills/research-vault-harness/tests -v
```

2026-10-27 发布前检查：框架校验 0 错误 / 0 警告，原验证器 16 项测试通过；JSON、28 份 Markdown frontmatter、1 份 Base 及框架文档链接解析通过。

上面的命令验证框架、结构与验证器测试，不表示插件已安装或完成实际设备接入。原始 Bases 规则和研究模板保留其基线行为，使用者可按自己的工作流调整。

## 来源与公开范围

由 `GoldenWitchs/postgraduate-vault-backup` 的远端提交 `3db4021005e7fa35df24964ba464e3eb0261bda4` 提取。原框架历史作者为 `dingan323424-dev`；发布者只制作空白模板与使用说明。文件来源、保留哈希与重置项见 [架构来源清单](ARCHITECTURE_SOURCE.json)。

发布采用全新 Git 历史。没有复制原仓库历史、个人笔记、论文/课件、私人档案、旧任务、历史记忆、插件程序、设备路径或本机新增配置。原私有备份及本机 Vault 保持原样。

许可与归属见 [NOTICE.md](NOTICE.md)；本仓库公开不代表给未标注许可的上游内容重新授予许可证。
