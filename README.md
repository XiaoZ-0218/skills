# coding-instructions

> Andrej Karpathy 编程准则 + Conventional Commits 提交规范 + 功能分支工作流 + 可爱语气回复规范

一套面向 AI 辅助编程的 **Agent Skill** 包：帮助个人与小团队在借助 AI 写代码时保持代码简洁、提交历史清晰、合并流程可控。

## 特性

- **极简主义编码**：从最短、自包含、零依赖的实现开始，逐步增加复杂度
- **先复制，再创新**：优先复用成熟方案，一次只引入一个复杂度
- **理解底层原理**：避免黑盒调用，代码体现对底层机制的理解
- **功能分支开发**：从当前上游分支切出独立分支；兼容普通仓库与 `git worktree`
- **Conventional Commits 提交规范**：type + 中文描述（详见 `references/commit-messages.md`）
- **测试通过后合并**：合并前必须完成测试并请求许可，禁止自行合并
- **可爱语气对话**：所有回复使用可爱、温柔、撒娇的语气

## Skill 包结构

本仓库根目录即为可安装的 skill 目录（符合 Grok / Claude Code 等 Agent Skill 约定）：

```
coding-instructions/
├── SKILL.md                      # 入口：frontmatter + 代理可执行规范
├── references/
│   └── commit-messages.md        # 提交信息规范详细参考
├── README.md
├── CONTRIBUTING.md
├── LICENSE
└── .gitignore
```

| 文件 | 说明 |
|------|------|
| `SKILL.md` | Skill 入口。含 `name` / `description` frontmatter，以及编码、Git、语气规则 |
| `references/commit-messages.md` | 提交格式、速查表、示例与 AI 提交守则 |
| `README.md` | 项目简介与安装指南 |
| `CONTRIBUTING.md` | 贡献指南 |
| `LICENSE` | MIT 许可证 |

## 安装

将本仓库（或其中 skill 目录）放到各工具的 skills 扫描路径即可。目录名建议为 `coding-instructions`。

### Grok

```bash
# 用户级（所有项目可用）
git clone <本仓库 URL> ~/.grok/skills/coding-instructions

# 或仅当前项目
git clone <本仓库 URL> .grok/skills/coding-instructions
```

- 斜杠命令：`/coding-instructions`
- 自动触发：当描述匹配「写代码 / 提交 / 分支 / 合并 / 可爱语气」等意图时

### Claude Code

```bash
# 用户级
git clone <本仓库 URL> ~/.claude/skills/coding-instructions

# 或项目级
git clone <本仓库 URL> .claude/skills/coding-instructions
```

### Cursor

```bash
git clone <本仓库 URL> ~/.cursor/skills/coding-instructions
# 或
git clone <本仓库 URL> .cursor/skills/coding-instructions
```

### 手动同步 / 软链

若已 clone 到别处，可用软链避免重复拷贝：

```bash
ln -s /path/to/coding-instructions ~/.grok/skills/coding-instructions
ln -s /path/to/coding-instructions ~/.claude/skills/coding-instructions
```

> 更新 skill：在 clone 目录中 `git pull` 即可。

## 使用方式

1. 按上文安装到对应 skills 目录
2. 新开会话，或显式运行 `/coding-instructions`
3. AI 代理在编码、提交、分支与合并过程中应自动遵循本规范

**是否生效的简单判断**：若回复不再使用可爱语气，说明当前上下文可能未加载本 skill，请重新激活或检查安装路径。

## 规范摘要

### 编码原则

1. 极简主义 — 从简开始  
2. 「不要做英雄」— 先复制，再创新  
3. 理解底层原理  
4. 从简单到复杂  
5. 简洁代码风格  
6. 最小依赖  

### Git 工作流

- 从当前上游切出 `feature|fix|test|docs/<描述>` 开发
- 每完成一个逻辑步骤提交一次（格式见 `references/commit-messages.md`）
- 合并前跑完整测试，向用户请求合并许可
- 合入主分支使用 `git merge --no-ff`，禁止 squash / rebase merge 替代
- 合并后删除已合并功能分支

### 对话语气

- 可爱、温柔、撒娇；技术内容保持专业准确

完整可执行规范见 [`SKILL.md`](./SKILL.md)。

## 贡献

欢迎通过 Issue 或 Pull Request 提出改进建议。请先阅读 [`CONTRIBUTING.md`](./CONTRIBUTING.md)。

## 许可证

本项目采用 [MIT 许可证](./LICENSE)。
