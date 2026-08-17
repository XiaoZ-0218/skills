---
name: rare-plane-spotter
description: 检索全球任意城市当天起降的稀有、好看、值得拍摄的飞机（特殊涂装、罕见机型、罕见航司等），给出具体时间、机场、航班号、机型和注册号。当用户是飞友/航空摄影爱好者，问"今天有什么值得拍的飞机""某城市今天有什么好货""某机场今天有什么稀有机型/彩绘"，或定时任务要求按城市巡检当日值得拍的飞机时，必须使用本 skill——即使只提到城市名加"飞机""拍机""好货"也应触发。
---

# rare-plane-spotter

给定一个城市，找出**当天**在该城市机场起降的、值得专程去拍的飞机，输出时间、机场、航班号、机型、注册号、看点（特殊涂装 / 罕见机型 / 罕见航司）。

本 skill 自带 CLI（`main.py` + 内置全球机场库 + 特殊涂装库），用 `uv run` 从任意目录运行。所有机器可读输出走 **stdout(JSON)**，日志走 stderr。

```bash
uv run "/Users/zhangxiao/.agents/skills/rare-plane-spotter/main.py" <子命令>
```

## 总流程（按顺序做）

1. **解析城市** → 2. **拿当日时刻表**（浏览器优先，实时流兜底） → 3. **稀有度初筛** → 4. **逐架查照片确认涂装并更新涂装库** → 5. **输出中文报告**

### 1. 解析城市

```bash
uv run ".../main.py" resolve 上海
```

支持中文城市名（内置别名）、英文城市名、机场名、IATA/ICAO 代码。`matched` 可能有多个机场（如上海→PVG+SHA），**全部都要查**。如果匹配到的城市和用户意图明显不符，先和用户确认。

### 2. 拿当日时刻表

**首选：浏览器抓 FR24 全天时刻表**（含未来航班，curl 会被 Cloudflare 拦，必须用浏览器）：

1. 用 `browser-use:control-browser` skill 打开浏览器，访问：
   `https://api.flightradar24.com/common/v1/airport.json?code=<IATA>&plugin[]=schedule&plugin-setting[schedule][mode]=&plugin-setting[schedule][timestamp]=<当天12:00UTC的unix时间戳>&page=1&limit=100`
   （在真实浏览器里这个 URL 直接返回 JSON；arrivals/departures 都在里面。limit=100 不够就翻页 `page=2`。）
2. 把 JSON 原文存成文件（如 `/tmp/fr24_pvg.json`），然后：

   ```bash
   uv run ".../main.py" parse-fr24 /tmp/fr24_pvg.json
   ```

   输出已按 `rarity_score` 排序，含航班号、机型、注册号、时刻（**unix UTC，报告里必须转成机场当地时间**）、航司、看点理由。

**兜底：实时流快照**（零配置随时可用，但只能看到"现在正在飞的"，适合白天运行或浏览器不可用时）：

```bash
uv run ".../main.py" live 上海
```

返回城市机场周边 ±150km 内在空的飞机，`involves_city=true` 的即正在进出该城市。用它补充正在进港的重型机，并在报告中注明"实时快照，非全天计划"。

### 3. 稀有度初筛

CLI 已给出 `rarity_score` 和 `reasons`。筛选时**不要只看分数**，结合你的判断：

- **高分项**：747/A340/A380/MD-11/DC-10/An-124/An-22/Il-76/Il-96/图-204、727/707/DC-8 等老机、涂装库命中。
- **加分项**：货航重型机（尤其国内机场白天的外航货机）、该机场罕见的航司（如非洲/南美/中亚航司出现在东亚）、军/政府/要员专机、调机/包机。
- **地域常识**：C919 在国内常见但在国外极稀有；A350/787 在枢纽不稀奇，在支线机场值得提。结合城市规模调整期望值。
- **排除**：本地基地航司的常规窄体（320/737）一律不推荐，除非涂装库命中。

### 4. 查照片、更新涂装库（每次运行必做）

对第 3 步筛出的候选（重点是宽体、罕见航司、注册号陌生的），批量查照片：

```bash
uv run ".../main.py" enrich B-2006 HL8509 9V-SKI
```

- 输出里 `photos` 是下载到本地的缩略图路径。**用 Read 工具亲眼查看这些照片**，判断是否特殊涂装/好看涂装。
- 确认是特殊涂装的，写回涂装库（这就是涂装库的自我更新机制）：

  ```bash
  uv run ".../main.py" livery add B-XXXX --airline "XXX航空" --aircraft "Boeing 777-300ER" --livery "涂装名称" --notes "补充说明"
  ```

- 确认是普通涂装的不用记录；发现库里某注册号已换回普通涂装，用 `livery add` 覆盖并在 notes 里注明"已换回普涂（YYYY-MM-DD 照片核实）"。
- planespotters 无照片（小航司/新飞机常见）时不要臆断，报告里标注"无照片可查"。

### 5. 输出报告（中文）

按时间排序，示例格式：

| 时间(本地) | 机场 | 航班 | 机型 | 航司 | 注册号 | 看点 |
|---|---|---|---|---|---|---|
| 09:35 到 | PVG | MU588 | B777-300ER | 中国东方 | B-2002 | 进博号彩绘（照片已核实） |
| 14:20 发 | PVG | 5X063 | B747-8F | UPS | N6xxUP | 748F 货机 |

- 只列值得拍的；**常见机型常规涂装不要列**。最后可以加一行"其他在空的关注目标"（来自 live 快照）。
- 标注数据来源与时效（"FR24 全天计划"或"实时快照"），计划可能临时换机型/换机，提醒用户以实际为准。
- 缓存的照片在 `~/.cache/rare-plane-spotter/photos/`，报告里可附确认涂装的照片路径。

## 定时任务用法

用户设 cron 时，prompt 里写明城市即可，例如：

> 用 rare-plane-spotter skill 检索**上海**今天值得拍的稀有/好看飞机，给出时间、机场、航班号、机型、注册号和看点，涂装要用照片核实。

## 维护与限制

- 机场库来自 OurAirports（公有领域）。更新：`curl -sL -o /tmp/airports.csv https://davidmegginson.github.io/ourairports-data/airports.csv` 然后 `python3 tools/build_airports.py /tmp/airports.csv`（在 skill 目录下运行）。
- 涂装库 `liveries.json` 是种子数据 + 运行时累积，条目可能过时（飞机换涂装），靠第 4 步照片核实纠偏。
- FR24 页面/接口结构若变动，浏览器抓取失败时：退到 `live` 快照出报告并明确告知用户。
- 中国大陆社区 ADS-B 覆盖差，不要依赖 adsb.lol/OpenSky 等社区源（实测不可用/配额极小）。
- 开发完成后需同步到 `~/.agents/skills/rare-plane-spotter/`。
