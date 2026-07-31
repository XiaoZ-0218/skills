# 贡献指南

感谢你对 `coding-instructions` 的关注！本仓库是面向 AI 辅助编程的 **Agent Skill** 包，欢迎通过 Issue 或 Pull Request 参与改进。

## 仓库结构（请保持）

```
.
├── SKILL.md                 # Skill 入口（frontmatter + 主规范）
├── references/              # 代理按需阅读的详细参考
│   └── commit-messages.md
├── README.md                # 人类可读的安装与简介
├── CONTRIBUTING.md
├── LICENSE
└── .gitignore
```

- **不要**把主入口命名为其他文件名；各 Agent 约定入口为 `SKILL.md`。
- 细节参考放在 `references/`，主文件用相对链接引用，避免 SKILL 体量过大。
- `README.md` / `CONTRIBUTING.md` 面向人类；`SKILL.md` 面向代理（可执行、可扫描）。

## 如何贡献

### 1. 提交 Issue

如果你发现：

- 规范描述存在歧义或错误
- 缺少某种常见场景的约定
- 示例不够清晰
- frontmatter / 安装路径与主流 Agent 不兼容

请先搜索是否已有相关 Issue；没有则新建，描述清楚问题或建议。

### 2. 提交 Pull Request

1. Fork 本仓库并 clone 到本地。
2. 同步主分支：
   ```bash
   git pull origin main
   ```
3. 从主分支切出功能分支：
   - 新增规范：`git checkout -b feature/<简短描述> main`
   - 修复问题：`git checkout -b fix/<简短描述> main`
   - 文档改进：`git checkout -b docs/<简短描述> main`

   > 若通过 `git worktree` 维护，请从对应 worktree 的上游分支切出功能分支，并在该 worktree 内开发。

4. 在功能分支上修改，每次只做一个逻辑改动。
5. 提交遵循本项目的 Conventional Commits 规范，见 [`references/commit-messages.md`](./references/commit-messages.md)。
6. 确保 Markdown 格式正确、链接可用；改完后本地确认：
   - `SKILL.md` 顶部 YAML frontmatter 可解析（`name`、`description` 必填）
   - `SKILL.md` 内指向 `references/` 的相对链接有效
7. 向 `main` 发起 Pull Request，说明改动原因与影响范围。
8. PR 合并后删除已合并功能分支。

## 规范修改原则

- **保持简洁**：宁可拆分多条规则，也不要把多种场景硬塞进一条。
- **保持可执行**：每条规范都应能被 AI 代理直接执行（命令、分支名、许可步骤写清楚）。
- **保持一致**：新增内容应与现有 Karpathy 准则和 Git 工作流风格一致。
- **提供示例**：抽象约定最好配具体示例。
- **描述可发现**：改 `description` / 触发语时，想清楚 Agent 何时应自动加载本 skill。

## 文风

- 规范正文使用中文。
- Markdown 标题层级清晰，避免过深嵌套。
- 列表项标点与格式保持一致。
- `SKILL.md` 优先清单与硬性步骤；人类背景说明放在 `README.md`。

## 行为准则

请保持友善、尊重与建设性。不同团队的工作流各有差异，本规范的目标是提炼一套通用且可落地的约定。
