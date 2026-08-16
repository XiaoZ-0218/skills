# Skills

Agent skill 合集仓库，每个子目录是一个独立的 skill（含 `SKILL.md`）。

## 收录的 Skills

| Skill | 说明 |
|-------|------|
| [coding-instructions](./coding-instructions) | 编码规范与协作指令 |
| [multi-agent-workflow](./multi-agent-workflow) | 多智能体工作流编排 |
| [humanizer-zh](./humanizer-zh) | 中文文本人性化润色 |
| [rare-plane-spotter](./rare-plane-spotter) | 稀有彩绘飞机查询 |
| [web-video-presentation](./web-video-presentation) | 网页视频演示生成 |

## 安装

克隆本仓库后，将需要的 skill 目录链接或复制到 agent 的 skills 目录：

```bash
git clone https://github.com/XiaoZ-0218/skills.git
ln -s "$PWD/skills/coding-instructions" ~/.zcode/skills/coding-instructions
```

## 独立仓库的工具型 Skills

以下是带独立发布周期的完整工具项目，保留单独仓库：

- [bt-search](https://github.com/XiaoZ-0218/bt-search) — BT 资源搜索 CLI（Python 包）
- [use-grok](https://github.com/XiaoZ-0218/use-grok) — Grok 代码评审 CLI（npm 包）
- [flights-kml-search](https://github.com/XiaoZ-0218/flights-kml-search) — 航班 KML 轨迹查询（Python 包）
