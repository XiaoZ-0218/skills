# rare-plane-spotter

给定城市，找出当天在该城市机场起降、值得专程去拍的飞机。

本目录就是一个自包含 skill：根目录 `SKILL.md` 负责触发约定，`main.py` 是 CLI 入口，机场库和涂装库与入口放在一起，方便 `uv run` 从任意工作目录调用。

```text
.
├── SKILL.md           # agent 触发与流程
├── main.py            # CLI（PEP 723，uv run 即可）
├── airports.json      # 全球机场库
├── liveries.json      # 特殊涂装库
└── tools/
    └── build_airports.py
```

```bash
uv run main.py resolve 上海
uv run main.py live 上海
```

安装到本机：

```bash
ln -sfn "$PWD" ~/.agents/skills/rare-plane-spotter
```

调用约定见 [SKILL.md](SKILL.md)。
