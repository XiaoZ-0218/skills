# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///
"""rare-plane-spotter CLI — find today's interesting aircraft at any city.

Subcommands:
  resolve <city>            City / IATA / ICAO -> matching airports (JSON)
  live <city>               Live FR24 feed snapshot near the city's airports
  parse-fr24 <file>         Normalize an FR24 airport.json browser dump
  enrich <REG...>|--stdin   Planespotters photo lookup + thumbnail download
  livery list|check|add     Special-livery registry management

All machine-readable output goes to stdout as JSON; chatter goes to stderr.
"""
import ipaddress, json, os, re, socket, sys, time
from pathlib import Path
from urllib.parse import urlparse

import requests

BASE = Path(__file__).resolve().parent
AIRPORTS_JSON = BASE / "airports.json"
LIVERY_DB = BASE / "liveries.json"
CACHE = Path(os.environ.get("RPS_CACHE", Path.home() / ".cache" / "rare-plane-spotter"))

UA = {"User-Agent": "RarePlaneSpotter/0.1 (+https://example.com/contact)"}
FR24_UA = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Referer": "https://www.flightradar24.com/",
}
FEED_URL = "https://data-cloud.flightradar24.com/zones/fcgi/feed.js"
PLNSPTTRS_URL = "https://api.planespotters.net/pub/photos/reg/"

# Every outbound request goes through http_get, which only talks to these
# known data hosts over https, after verifying DNS answers are public IPs.
ALLOWED_HOSTS = frozenset({
    "data-cloud.flightradar24.com",
    "api.planespotters.net",
    "t.plnspttrs.net",
})


def _assert_public_host(host):
    for info in socket.getaddrinfo(host, 443, proto=socket.IPPROTO_TCP):
        ip = ipaddress.ip_address(info[4][0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local
                or ip.is_multicast or ip.is_reserved or ip.is_unspecified):
            raise ValueError(f"{host} resolves to non-public address {ip}")


def http_get(url, headers=None, timeout=25, params=None):
    parsed = urlparse(url)
    host = parsed.hostname or ""
    if parsed.scheme != "https" or host not in ALLOWED_HOSTS:
        raise ValueError(f"refusing to fetch non-allowlisted URL: {url}")
    _assert_public_host(host)
    r = requests.get(url, headers=headers, timeout=timeout, params=params,
                     allow_redirects=False)
    r.raise_for_status()
    return r


# Rough rarity weights by ICAO/IATA type designator prefix. Scores are
# deliberately simple: they rank a day's list, they are not gospel.
TYPE_SCORES = {
    "A225": 100,
    "A124": 90,
    "B743": 80, "B744": 80, "B748": 82, "B74": 80, "747": 80,
    "A388": 78, "A380": 78,
    "A342": 76, "A343": 76, "A345": 78, "A346": 78, "A340": 76,
    "MD11": 75, "DC10": 78, "L101": 80,
    "IL76": 72, "IL96": 75, "IL62": 78, "TU204": 70, "TU214": 72,
    "AN12": 60, "AN22": 85, "AN26": 45, "AN72": 60,
    "B722": 70, "B727": 70, "B707": 85, "DC8": 85, "DC9": 55, "MD80": 55,
    "MD82": 55, "MD83": 55, "MD90": 58,
    "B762": 45, "B763": 40, "B764": 45,
    "B772": 25, "B77L": 30, "B77W": 25, "B778": 30, "B779": 35,
    "A332": 15, "A333": 12, "A359": 15, "A35K": 18, "B789": 12, "B788": 10,
    "C919": 30, "SSJ": 35, "E190": 8,
}
CARGO_HINTS = ("CARGO", "CARGOLUX", "FEDEX", "UPS", "DHL", "ATLAS", "KALITTA",
               "SILK WAY", "VOLGA-DNEPR", "AIR BRIDGE", "SF AIRLINES",
               "SUPARNA", "POLAR", "NCA", "NIPPON CARGO")


def eprint(*a):
    print(*a, file=sys.stderr)


def load_airports():
    data = json.loads(AIRPORTS_JSON.read_text(encoding="utf-8"))
    return data["aliases"], data["airports"]


def load_livery_db():
    if LIVERY_DB.exists():
        return json.loads(LIVERY_DB.read_text(encoding="utf-8"))
    return {}


def save_livery_db(db):
    LIVERY_DB.write_text(json.dumps(db, ensure_ascii=False, indent=2, sort_keys=True),
                         encoding="utf-8")


def type_score(typecode):
    t = (typecode or "").upper().strip()
    if t in TYPE_SCORES:
        return TYPE_SCORES[t]
    for k in sorted(TYPE_SCORES, key=len, reverse=True):
        if k and t.startswith(k):
            return TYPE_SCORES[k]
    return 0


def rarity(typecode, airline, reg, livery_db):
    reasons = []
    score = type_score(typecode)
    if score >= 70:
        reasons.append(f"very rare type {typecode}")
    elif score >= 40:
        reasons.append(f"uncommon type {typecode}")
    if airline and any(h in airline.upper() for h in CARGO_HINTS):
        score += 10
        reasons.append("cargo operator")
    info = livery_db.get((reg or "").upper())
    if info:
        score += 50
        reasons.append(f"livery DB hit: {info.get('livery', '?')}")
    return score, reasons


# ---------------------------------------------------------------- resolve
def cmd_resolve(city):
    aliases, airports = load_airports()
    q = city.strip()
    ql = aliases.get(q.lower(), q.lower())
    qu = q.upper()

    def city_norm(a):
        return (a["city"] or "").split(" (")[0].lower()

    rank = {"large_airport": 0, "medium_airport": 1}
    out = []
    for a in airports:
        if qu and qu in (a["iata"], a["icao"]):
            out.insert(0, a)
        elif ql and (ql == city_norm(a) or ql in (a["name"] or "").lower()):
            out.append(a)
    if not out:
        # substring on city name, for inputs like "shanghai pudong"
        for a in airports:
            if ql and ql in city_norm(a):
                out.append(a)
    out = [a for a in out if a["iata"] or a["icao"] == qu] \
        or out  # scheduled airports first; bare-code match kept
    out.sort(key=lambda a: rank.get(a["type"], 2))
    return {"query": city, "matched": out[:12]}


# ---------------------------------------------------------------- live
def feed_box(lat, lon, deg=1.5):
    params = {
        "bounds": f"{lat + deg:.2f},{lat - deg:.2f},{lon - deg:.2f},{lon + deg:.2f}",
        "faa": 1, "mlat": 1, "flarm": 1, "adsb": 1,
        "gnd": 1, "air": 1, "vehicles": 0, "estimated": 1,
        "maxage": 14400, "gliders": 0,
    }
    return http_get(FEED_URL, headers=FR24_UA, params=params).json()


def cmd_live(city):
    res = cmd_resolve(city)
    if not res["matched"]:
        eprint(f"no airports matched '{city}'")
        sys.exit(1)
    livery_db = load_livery_db()
    local_codes = {a["iata"] for a in res["matched"] if a["iata"]}
    seen, out = {}, []
    for a in [a for a in res["matched"] if a["iata"]][:4]:
        try:
            data = feed_box(a["lat"], a["lon"])
        except Exception as ex:
            eprint(f"feed failed for {a['iata'] or a['icao']}: {ex}")
            continue
        for key, v in data.items():
            if not isinstance(v, list) or len(v) < 17 or key in seen:
                continue
            seen[key] = 1
            # v: [hex, lat, lon, track, alt, gs, squawk, radar, type, reg,
            #     ts, origin, dest, flight, ?, ?, callsign, ?, airline]
            origin, dest = v[11] or "", v[12] or ""
            relevant = (origin in local_codes or dest in local_codes)
            score, reasons = rarity(v[8], v[18] if len(v) > 18 else "", v[9], livery_db)
            if relevant or score >= 40:
                out.append({
                    "hex": v[0], "type": v[8], "reg": v[9],
                    "callsign": v[16] or v[13], "airline": v[18] if len(v) > 18 else "",
                    "origin": origin, "dest": dest, "alt_ft": v[4], "gs_kt": v[5],
                    "involves_city": relevant,
                    "rarity_score": score, "reasons": reasons,
                })
        time.sleep(1)  # be polite to the free feed
    out.sort(key=lambda x: -x["rarity_score"])
    return {"query": city, "airports": [
                {k: a[k] for k in ("iata", "icao", "name", "city")}
                for a in res["matched"]],
            "snapshot_utc": int(time.time()), "aircraft": out}


# ---------------------------------------------------------------- parse-fr24
def walk_flights(node):
    """Yield flight dicts from an FR24 airport.json schedule dump."""
    try:
        sched = node["result"]["response"]["airport"]["pluginData"]["schedule"]
    except (KeyError, TypeError):
        return
    for mode in ("arrivals", "departures"):
        for item in (sched.get(mode) or {}).get("data") or []:
            f = item.get("flight") or {}
            ac = f.get("aircraft") or {}
            airport = f.get("airport") or {}
            yield {
                "mode": mode,
                "flight_no": ((f.get("identification") or {}).get("number") or {}).get("default"),
                "callsign": (f.get("identification") or {}).get("callsign"),
                "airline": (f.get("airline") or {}).get("name"),
                "type": (ac.get("model") or {}).get("code"),
                "reg": ac.get("registration"),
                "other_airport": (((airport.get("origin") or {}).get("code") or {}).get("iata"))
                    if mode == "arrivals" else
                    (((airport.get("destination") or {}).get("code") or {}).get("iata")),
                "time_utc": ((f.get("time") or {}).get("scheduled") or {}).get(
                    "arrival" if mode == "arrivals" else "departure")
                    or ((f.get("time") or {}).get("estimated") or {}).get(
                        "arrival" if mode == "arrivals" else "departure"),
                "status": (f.get("status") or {}).get("text"),
            }


def cmd_parse_fr24(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    livery_db = load_livery_db()
    out = []
    for f in walk_flights(data):
        score, reasons = rarity(f["type"], f["airline"] or "", f["reg"], livery_db)
        f["rarity_score"] = score
        f["reasons"] = reasons
        out.append(f)
    out.sort(key=lambda x: (-x["rarity_score"], x["time_utc"] or 0))
    return {"count": len(out), "flights": out}


# ---------------------------------------------------------------- enrich
def cmd_enrich(regs):
    livery_db = load_livery_db()
    (CACHE / "photos").mkdir(parents=True, exist_ok=True)
    results = []
    for reg in regs:
        reg = reg.strip().upper()
        if not re.fullmatch(r"[A-Z0-9\-]{2,12}", reg):
            eprint(f"skipping implausible registration: {reg!r}")
            continue
        entry = {"reg": reg, "in_livery_db": reg in livery_db,
                 "livery_info": livery_db.get(reg), "photos": []}
        try:
            r = http_get(PLNSPTTRS_URL + reg, headers=UA, timeout=20)
            for ph in (r.json().get("photos") or [])[:3]:
                url = (ph.get("thumbnail_large") or {}).get("src") \
                    or (ph.get("thumbnail") or {}).get("src")
                if not url:
                    continue
                try:
                    img = http_get(url, headers=UA, timeout=20)
                except ValueError as ex:  # off-allowlist CDN host
                    eprint(str(ex))
                    continue
                if len(img.content) > 1000:
                    p = CACHE / "photos" / f"{reg}_{ph['id']}.jpg"
                    p.write_bytes(img.content)
                    entry["photos"].append(str(p))
        except Exception as ex:
            eprint(f"planespotters {reg}: {ex}")
        results.append(entry)
        time.sleep(0.5)
    return {"results": results}


# ---------------------------------------------------------------- livery
def cmd_livery(args):
    db = load_livery_db()
    if args[0] == "list":
        return {"count": len(db), "liveries": db}
    if args[0] == "check":
        reg = args[1].upper()
        return {"reg": reg, "known": reg in db, "info": db.get(reg)}
    if args[0] == "add":
        # livery add REG --airline X --aircraft Y --livery Z --notes N
        reg = args[1].upper()
        kv = {}
        it = iter(args[2:])
        for tok in it:
            if tok.startswith("--"):
                kv[tok[2:]] = next(it, "")
        db[reg] = {
            "airline": kv.get("airline", ""), "aircraft": kv.get("aircraft", ""),
            "livery": kv.get("livery", ""), "notes": kv.get("notes", ""),
            "updated": time.strftime("%Y-%m-%d"),
        }
        save_livery_db(db)
        return {"added": reg, "info": db[reg], "total": len(db)}
    sys.exit(f"unknown livery action: {args[0]}")


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    cmd, rest = args[0], args[1:]
    if cmd == "resolve":
        out = cmd_resolve(rest[0])
    elif cmd == "live":
        out = cmd_live(rest[0])
    elif cmd == "parse-fr24":
        out = cmd_parse_fr24(rest[0])
    elif cmd == "enrich":
        if rest and rest[0] == "--stdin":
            regs = [x["reg"] for x in json.load(sys.stdin) if x.get("reg")]
        else:
            regs = rest
        out = cmd_enrich(regs)
    elif cmd == "livery":
        out = cmd_livery(rest)
    else:
        sys.exit(f"unknown command: {cmd}\n{__doc__}")
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
    print()


if __name__ == "__main__":
    main()
