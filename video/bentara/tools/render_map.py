"""Draws the light 'real map' basemaps for the location scene from OpenStreetMap data.

Input : area.json from tools/osm_extract.py (roads, rivers, areas, places around the site)
Output: assets/map/base-detail.jpg and assets/map/base-wide.jpg, plus base-layers.json with
        each image's world rectangle. World coords match build.py's W(): 100 units = 1 km.
Usage : python3 tools/render_map.py /path/to/area.json   (needs node + playwright)
Map data (c) OpenStreetMap contributors, ODbL.
"""
import json, math, subprocess, sys, os, tempfile

LON0, LAT0 = 101.53, 2.96
KX = 111.32 * math.cos(math.radians(2.95)) * 100
KY = 110.57 * 100
W = lambda lon, lat: ((lon - LON0) * KX, -(lat - LAT0) * KY)

LAYERS = {
    # name: world rect (x0, y0, x1, y1), px per world unit, style scale
    "detail": ((-480, -540, 460, 1100), 2.4, "detail"),
    "wide":   ((-960, -1560, 740, 1440), 0.9, "wide"),
}

COL = dict(land="#f4f2ee", urban="#ebe8e3", building="#dedad3", park="#c4e5bb", forest="#b9dcb0",
           farm="#e8ecd8", wetland="#cfe8d8", water="#a8d3f5", label="#4d5156", halo="#ffffff")
ROAD = {  # hw: (detail width, wide width, fill, casing)
    "motorway": (15, 7, "#f6c55c", "#d9982b"), "trunk": (13, 6, "#fbd57a", "#dba84a"),
    "primary": (12, 4.5, "#fde69a", "#d8bc6a"), "secondary": (10.5, 3.2, "#ffffff", "#cfcac2"),
    "tertiary": (9, 2.4, "#ffffff", "#d3cec6"), "unclassified": (7, 1.4, "#ffffff", "#d6d1c9"),
    "residential": (6.5, 1.1, "#ffffff", "#d6d1c9"), "living_street": (6, 0, "#ffffff", "#d6d1c9"),
    "service": (3.5, 0, "#ffffff", "#dcd7cf"), "track": (2.5, 0, "#f4f2ee", "#cdbfa8"),
    "construction": (6, 2, "#f1eee8", "#d0cbc2"),
}
for k in ("motorway", "trunk", "primary", "secondary", "tertiary"):
    ROAD[k + "_link"] = (ROAD[k][0] * .6, ROAD[k][1] * .6, ROAD[k][2], ROAD[k][3])
ORDER = ["track", "service", "living_street", "residential", "unclassified", "construction", "tertiary_link",
         "tertiary", "secondary_link", "secondary", "primary_link", "primary", "trunk_link", "trunk",
         "motorway_link", "motorway"]


def svg_for(data, rect, ppu, style):
    x0, y0, x1, y1 = rect
    Wpx, Hpx = int((x1 - x0) * ppu), int((y1 - y0) * ppu)
    P = lambda lon, lat: ((W(lon, lat)[0] - x0) * ppu, (W(lon, lat)[1] - y0) * ppu)
    m = 60
    def visible(pts):
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        return max(xs) > -m and min(xs) < Wpx + m and max(ys) > -m and min(ys) < Hpx + m
    def d(coords, close=False):
        pts = [P(*c) for c in coords]
        if not visible(pts): return None
        return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + (" Z" if close else "")
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wpx}" height="{Hpx}" viewBox="0 0 {Wpx} {Hpx}">',
           f'<rect width="{Wpx}" height="{Hpx}" fill="{COL["land"]}"/>']
    kinds = ["urban", "farm", "forest", "park", "wetland", "water"] + (["building"] if style == "detail" else [])
    for k in kinds:
        paths = []
        for a in data["areas"]:
            if a["k"] != k: continue
            dd = d(a["c"], True)
            if not dd: continue
            for h in a.get("h", []):
                hh = d(h, True)
                if hh: dd += " " + hh
            paths.append(dd)
        extra = ' stroke="#d2cdc5" stroke-width="0.8"' if k == "building" else ""
        out.append(f'<path fill="{COL[k]}" fill-rule="evenodd"{extra} d="{" ".join(paths)}"/>')
    for r in data["rivers"]:
        w = {"river": 7, "canal": 5, "stream": 2.5, "drain": 2}[r["ww"]] * (1 if style == "detail" else .45)
        dd = d(r["c"])
        if dd and w >= .8:
            out.append(f'<path d="{dd}" fill="none" stroke="{COL["water"]}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
    wi = 0 if style == "detail" else 1
    by = {k: [] for k in ORDER}
    for r in data["roads"]:
        if r["hw"] in by and ROAD[r["hw"]][wi] > 0:
            dd = d(r["c"])
            if dd: by[r["hw"]].append(dd)
    for k in ORDER:  # casings then fills, minor first
        if by[k]:
            w, c = ROAD[k][wi], ROAD[k][3]
            out.append(f'<path d="{" ".join(by[k])}" fill="none" stroke="{c}" stroke-width="{w + (2.6 if style == "detail" else 1.2):.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    for k in ORDER:
        if by[k]:
            w, f = ROAD[k][wi], ROAD[k][2]
            out.append(f'<path d="{" ".join(by[k])}" fill="none" stroke="{f}" stroke-width="{w:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    # place labels
    keep = ("town", "suburb", "village", "quarter", "neighbourhood") if style == "detail" else ("city", "town", "suburb", "village")
    fs = {"detail": 34, "wide": 30}[style]
    placed = []
    SKIP = {"Tropicana Aman", "Eco Sanctuary", "Bandar Rimbayu"}   # drawn as pins by the video
    RENAME = {"Teluk Panglima Garang": "Telok Panglima Garang"}
    for p in sorted(data["places"], key=lambda p: ("city", "town", "suburb", "village", "quarter", "neighbourhood", "hamlet").index(p["type"])):
        if p["type"] not in keep or p["name"] in SKIP: continue
        p = {**p, "name": RENAME.get(p["name"], p["name"])}
        x, y = P(*p["c"])
        if not (40 < x < Wpx - 40 and 40 < y < Hpx - 40): continue
        bw = len(p["name"]) * fs * .56
        if any(abs(x - a) < (bw + b) / 2 + 10 and abs(y - c) < fs * 1.4 for a, c, b in placed): continue
        placed.append((x, y, bw))
        big = p["type"] in ("city", "town")
        out.append(f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="middle" font-family="Inter, sans-serif" font-weight="{700 if big else 600}" '
                   f'font-size="{fs * (1.15 if big else 1):.0f}" fill="{COL["label"]}" stroke="{COL["halo"]}" stroke-width="7" paint-order="stroke" '
                   f'stroke-linejoin="round">{p["name"].replace("&", "&amp;")}</text>')
    out.append("</svg>")
    return "\n".join(out), Wpx, Hpx


def main():
    data = json.load(open(sys.argv[1]))
    os.makedirs("assets/map", exist_ok=True)
    meta = {}
    tmp = tempfile.mkdtemp()
    jobs = []
    for name, (rect, ppu, style) in LAYERS.items():
        svg, Wpx, Hpx = svg_for(data, rect, ppu, style)
        sp = os.path.join(tmp, name + ".svg"); open(sp, "w").write(svg)
        jobs.append({"svg": sp, "png": os.path.join(tmp, name + ".png"), "w": Wpx, "h": Hpx})
        meta[name] = {"x": rect[0], "y": rect[1], "w": rect[2] - rect[0], "h": rect[3] - rect[1]}
        print(name, Wpx, "x", Hpx, f"{len(svg) / 1e6:.1f} MB svg")
    js = os.path.join(tmp, "shot.js")
    open(js, "w").write("""
const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch();
  for (const j of JSON.parse(process.argv[2])) {
    const p = await b.newPage({ viewport: { width: j.w, height: j.h } });
    await p.setContent('<html><body style="margin:0">' + fs.readFileSync(j.svg, 'utf8') + '</body></html>', { timeout: 300000 });
    await p.screenshot({ path: j.png, clip: { x: 0, y: 0, width: j.w, height: j.h }, timeout: 300000 }); await p.close(); }
  await b.close(); })();""")
    subprocess.run(["node", js, json.dumps(jobs)], check=True, cwd=tmp)
    for name, j in zip(LAYERS, jobs):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", j["png"], "-q:v", "3", f"assets/map/base-{name}.jpg"], check=True)
    json.dump(meta, open("assets/map/base-layers.json", "w"), indent=1)
    print("done", meta)


if __name__ == "__main__":
    main()
