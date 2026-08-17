# Skills

Agent skill 合集仓库，采用插件市场（plugin marketplace）结构：每个 `skills/` 子目录是一个独立的 skill（含 `SKILL.md`）。

## 收录的 Skills

| Skill | 说明 |
|-------|------|
| [coding-instructions](./skills/coding-instructions) | 编码规范与协作指令 |
| [multi-agent-workflow](./skills/multi-agent-workflow) | 多智能体工作流编排 |
| [humanizer-zh](./skills/humanizer-zh) | 中文文本人性化润色 |
| [rare-plane-spotter](./skills/rare-plane-spotter) | 稀有彩绘飞机查询 |
| [web-video-presentation](./skills/web-video-presentation) | 网页视频演示生成 |

## 安装

方式一：作为插件市场一键安装（推荐）：

```
/plugin marketplace add XiaoZ-0218/skills
```

方式二：手动克隆后链接需要的 skill：

```bash
git clone https://github.com/XiaoZ-0218/skills.git
ln -sfn "$PWD/skills/skills/coding-instructions" ~/.agents/skills/coding-instructions
```

手动安装请链到 `~/.agents/skills/<name>`。不要链到 `~/.zcode/skills/`，同名时它会盖住 agents 里的副本。

## 独立仓库的工具型 Skills

以下是带独立发布周期的完整工具项目，保留单独仓库：

- [bt-search](https://github.com/XiaoZ-0218/bt-search) — BT 资源搜索 CLI（Python 包）
- [use-grok](https://github.com/XiaoZ-0218/use-grok) — Grok 代码评审 CLI（npm 包）
- [flight-kml-search](https://github.com/XiaoZ-0218/flight-kml-search) — 航班 KML 轨迹查询（Python 包；skill 名与仓库名均为 `flight-kml-search`）
