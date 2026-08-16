#!/usr/bin/env python3
"""Build airports.json from an OurAirports airports.csv (public domain).

Usage: python3 tools/build_airports.py <airports.csv>
Fetch the CSV yourself first (it is public domain):
  curl -sL -o /tmp/airports.csv https://davidmegginson.github.io/ourairports-data/airports.csv
Output: airports.json next to this script's parent directory.
Keeps large/medium airports plus any airport with scheduled service.
"""
import csv, io, json, sys
from pathlib import Path

OUT = (Path(__file__).resolve().parent.parent / "airports.json")
KEEP_TYPES = {"large_airport", "medium_airport"}

# Chinese (and a few local-language) city-name aliases for major spotting
# cities. Keys must be lowercase. Extend freely.
ALIASES = {
    "北京": "beijing", "上海": "shanghai", "广州": "guangzhou", "深圳": "shenzhen",
    "成都": "chengdu", "重庆": "chongqing", "西安": "xi'an", "杭州": "hangzhou",
    "南京": "nanjing", "武汉": "wuhan", "长沙": "changsha", "厦门": "xiamen",
    "昆明": "kunming", "青岛": "qingdao", "天津": "tianjin", "郑州": "zhengzhou",
    "乌鲁木齐": "urumqi", "哈尔滨": "harbin", "沈阳": "shenyang", "大连": "dalian",
    "贵阳": "guiyang", "海口": "haikou", "三亚": "sanya", "拉萨": "lhasa",
    "兰州": "lanzhou", "银川": "yinchuan", "西宁": "xining", "呼和浩特": "hohhot",
    "济南": "jinan", "福州": "fuzhou", "合肥": "hefei", "南昌": "nanchang",
    "宁波": "ningbo", "无锡": "wuxi", "珠海": "zhuhai", "香港": "hong kong",
    "澳门": "macau", "台北": "taipei", "高雄": "kaohsiung", "台中": "taichung",
    "东京": "tokyo", "大阪": "osaka", "名古屋": "nagoya", "札幌": "sapporo",
    "福冈": "fukuoka", "首尔": "seoul", "釜山": "busan", "新加坡": "singapore",
    "曼谷": "bangkok", "吉隆坡": "kuala lumpur", "雅加达": "jakarta",
    "马尼拉": "manila", "河内": "hanoi", "胡志明市": "ho chi minh city",
    "德里": "delhi", "孟买": "mumbai", "迪拜": "dubai", "多哈": "doha",
    "阿布扎比": "abu dhabi", "伊斯坦布尔": "istanbul", "莫斯科": "moscow",
    "伦敦": "london", "巴黎": "paris", "法兰克福": "frankfurt", "慕尼黑": "munich",
    "阿姆斯特丹": "amsterdam", "马德里": "madrid", "巴塞罗那": "barcelona",
    "罗马": "rome", "米兰": "milan", "苏黎世": "zurich", "日内瓦": "geneva",
    "维也纳": "vienna", "布鲁塞尔": "brussels", "哥本哈根": "copenhagen",
    "斯德哥尔摩": "stockholm", "奥斯陆": "oslo", "赫尔辛基": "helsinki",
    "里斯本": "lisbon", "雅典": "athens", "华沙": "warsaw", "布拉格": "prague",
    "布达佩斯": "budapest", "纽约": "new york", "洛杉矶": "los angeles",
    "旧金山": "san francisco", "西雅图": "seattle", "芝加哥": "chicago",
    "波士顿": "boston", "华盛顿": "washington", "迈阿密": "miami",
    "亚特兰大": "atlanta", "达拉斯": "dallas", "休斯敦": "houston",
    "丹佛": "denver", "拉斯维加斯": "las vegas", "安克雷奇": "anchorage",
    "檀香山": "honolulu", "多伦多": "toronto", "温哥华": "vancouver",
    "蒙特利尔": "montreal", "墨西哥城": "mexico city", "圣保罗": "sao paulo",
    "里约热内卢": "rio de janeiro", "布宜诺斯艾利斯": "buenos aires",
    "圣地亚哥": "santiago", "利马": "lima", "波哥大": "bogota",
    "悉尼": "sydney", "墨尔本": "melbourne", "布里斯班": "brisbane",
    "珀斯": "perth", "奥克兰": "auckland", "开罗": "cairo",
    "约翰内斯堡": "johannesburg", "开普敦": "cape town", "内罗毕": "nairobi",
    "亚的斯亚贝巴": "addis ababa", "卡萨布兰卡": "casablanca",
}

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    raw = Path(sys.argv[1]).read_text(encoding="utf-8")
    out = []
    for row in csv.DictReader(io.StringIO(raw)):
        if row["type"] not in KEEP_TYPES and row["scheduled_service"] != "yes":
            continue
        iata = row["iata_code"].strip()
        icao = row["icao_code"].strip() or row["ident"].strip()
        if not iata and not icao:
            continue
        out.append({
            "iata": iata, "icao": icao, "name": row["name"],
            "city": row["municipality"], "country": row["iso_country"],
            "lat": float(row["latitude_deg"]), "lon": float(row["longitude_deg"]),
            "type": row["type"],
        })
    out.sort(key=lambda a: (a["country"], a["city"], a["name"]))
    payload = {"aliases": ALIASES, "airports": out}
    OUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"wrote {OUT}: {len(out)} airports, {len(ALIASES)} aliases")

if __name__ == "__main__":
    main()
