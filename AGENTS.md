# Postgraduate Vault · Codex 工作约定

## 1. Vault 性质

- 当前目录是个人研究生 Obsidian Vault，不是普通代码仓库。
- Markdown 使用 Obsidian Flavored Markdown：优先 Wikilink、嵌入、Callout 和 YAML Properties。
- Zotero 是 PDF、书目元数据和引用键的事实源；Vault 不批量复制 Zotero PDF。

## 2. 默认写入边界

- AI 新生成的笔记默认写入 `00-Inbox/AI-Drafts/`，状态必须是 `ai-draft`。
- 网页原始剪藏进入 `00-Inbox/Web-Clips/`；随手输入进入 `00-Inbox/Quick-Notes/`。
- 只有用户明确要求“核验通过、晋升或正式入库”时，AI 才能把内容写入 `30-Knowledge/`。
- `.obsidian/`、`.codex/`、`.claudian/`、`_system/`、`_templates/` 属结构与配置区；除非用户明确要求配置或架构变更，否则只读。
- 不创建、记录或回显 API key、访问令牌、Cookie、私钥和完整认证信息。

## 3. 文献证据规则

- 不得猜测或编造 DOI、citekey、页码、章节、图号、表号、公式号、实验数值和引用。
- 无法从原文验证的信息必须标记为“未核验”，不得写成确定事实。
- 文献笔记应区分：作者结论、原文证据、AI 解释、我的判断、开放问题。
- AI 不替用户填写“我的判断”；可以提出问题或候选观点，但要标明是 AI 建议。
- 具体论断尽量附页码、章节、图表或公式位置；引用关系回到 Zotero 条目或 DOI。

## 4. Markdown / HTML 双载体

- 数学公式只使用 `$...$`（行内）与前后独占一行的 `$$...$$`（块级）；不要使用 `\(...\)` 或 `\[...\]`。矩阵换行使用 `\\`，块公式前后保留空行。
- 每份 AI 论文 HTML 必须有配套 Markdown 文献笔记。
- Markdown 放在 `30-Knowledge/Literature/`；AI 生成后、人工核验前先放 `00-Inbox/AI-Drafts/`。
- HTML 文件包放在 `40-Sources/AI-HTML/<citekey>/`，入口统一为 `index.html`。
- CSS、图片和脚本与 HTML 一起保留，移动时必须整体移动，不能破坏相对路径。
- Markdown 的 `html_artifact` 必须指向 HTML 入口；HTML 索引的 `paired_note` 必须回链 Markdown。
- HTML 是讲解与展示附件，不是正式知识的唯一载体。

## 5. 文件与链接安全

- 重命名、移动或删除前，先检查反向链接、嵌入、Canvas 和 Base 引用并向用户报告影响。
- 涉及已有笔记的移动优先通过 Obsidian File Manager；不得用批量文件系统重命名破坏链接。
- Windows 命令行读取 Vault 文本时显式使用 UTF-8；看到乱码先检查终端编码，不得据此重写原文件。
- 文献文件名使用 `<citekey> - <短标题>.md`；实验使用 `EXP-YYYYMMDD-序号-简述.md`。
- 避免 `未命名`、`current`、`final-final` 和大量同名 `README.md`。
- 同一份文献笔记只保留一份，项目通过 `projects` 属性或 Wikilink 引用，禁止复制多份。

## 6. 归位规则

- 有明确完成条件：`10-Projects/`
- 需要长期维护：`20-Areas/`
- 已核验、可跨项目复用：`30-Knowledge/`
- 原始材料或展示附件：`40-Sources/`
- 尚未判断或尚未核验：`00-Inbox/`
- 已完成或不再活跃：`90-Archive/`

## 7. 变更验证

- 修改 JSON 后必须解析验证。
- 修改模板或 Markdown Properties 后必须验证 YAML frontmatter。
- 修改 `.base` 后必须验证 YAML，并检查视图字段与 Properties 规范一致。
- 批量操作前列文件清单；完成后报告新增、修改、移动和删除项。

## 8. 上下文与检索

- 整个 Vault 可读，但不得把“可读”理解为每轮全库加载；使用即时、分层检索。
- 顺序为：当前笔记/选区/`@` 文件 → `_system/AI-Harness/INDEX.md` → 标题、Properties、citekey、Wikilink 和精确关键词 → 相关正文。
- 首轮通常读取 5–8 个最相关文件；证据不足才扩大范围，命中过多时先缩小查询。
- 默认排除 `.obsidian/`、`.claudian/sessions/`、`_assets/`、`90-Archive/` 和无关生成物；任务明确涉及时例外。
- 不因 Vault 变大就引入向量库；只有记录到可复现的检索失败或延迟问题后再评估。

## 9. Harness 与任务路由

- Harness 入口是 `_system/AI-Harness/INDEX.md`；详细契约按需读取，不复制到提示词或每次对话。
- L0 简单问答不创建任务目录；L1 研究任务保留来源与不确定性。
- L2 文件修改、跨多文件或跨会话任务使用 `_system/AI-Harness/tasks/active/<task-id>/`。
- L3 配置、规则、正式晋升、批量移动或删除必须先列影响并取得明确批准。
- 活动任务包含 `TASK.md`、`evidence.md`、`verification.md`、`log.jsonl`；完成后进入 `tasks/completed/`。

## 10. 控制表面与个人记忆

- 可编辑面：`00-Inbox/AI-Drafts/`、任务相关的 `40-Sources/AI-HTML/`、活动任务目录。
- 仅追加面：`_system/AI-Harness/memory/工作日志.jsonl`、`偏好候选.jsonl`、`失败与纠正.jsonl`；不得重写旧行。
- 锁定面：`AGENTS.md`、Harness 契约/质量规则、Skills 和配置；只有明确的架构或配置请求可修改。
- 人工控制面：`30-Knowledge/`、已有正式笔记、批量移动/删除和偏好晋升；遵守本文件更严格的既有规则。
- 用户明确表达的长期偏好可更新 `个人协作档案.md`；AI 推断只能追加为候选，得到确认后才晋升。
- `.claudian/sessions/` 和全局 Codex memories 不是本 Vault 的权威任务或偏好记录。

## 11. 风险自适应验证与停止

- 回答前检查是否直接作答、关键事实是否有依据、推断是否已标明；高风险任务增加对应检查。
- 文献、JSON/JSONL、YAML、链接和 Markdown/HTML 配对使用确定性检查，必要时运行 `$research-vault-harness` 提供的校验脚本。
- 只修复未通过的项目并重新验证；全部完成条件通过后立即停止，不执行固定次数或无意义的 loop。
- 证据冲突时保留冲突并报告；无法核验时标记“未核验”，不得用猜测填补。
