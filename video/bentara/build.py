"""Generates index.html for the Jalan Pipit semi-D voice-over cut.

All cue times below are in *voice-over time* (seconds into assets/vo/voiceover-tight.wav,
from the word-level transcript). VO_START shifts the whole VO into film time.
Run:  python3 build.py
"""

VO_START = 0.25
VO_LEN = 73.0
END_HOLD = 4.0
FILM = round(VO_START + VO_LEN + END_HOLD, 2)


def F(t):
    return round(t + VO_START, 3)


# ---------------------------------------------------------------- scenes (VO time)
SC = {
    "hook":    (0.0, 9.8),    # Kalau anda tengah cari ... harga bawah RM500,000 / cuba tengok yang ini
    "ext":     (9.8, 15.55),  # Terletak di Jalan Pipit ... rumah berkembar 1 tingkat
    "price":   (15.55, 20.0),  # dengan harga bermula RM485,700 sahaja
    "plan":    (20.0, 32.1),   # keluasan tanah 2,814 / binaan 1,266 / 4 bilik tidur + 2 bilik air
    "int":     (32.1, 35.5),   # sesuai untuk keluarga
    "status":  (35.5, 40.6),   # leasehold Rizab Melayu, 8 unit sahaja
    "eta":     (40.6, 44.0),   # dijangka siap Q4 2027
    "loc":     (44.0, 55.25),  # Tropicana Aman, Eco Sanctuary, Bandar Rimbayu / SKVE KESAS WCE LKSA
    "promo":   (55.25, 64.35), # booking RM1,000, free SPA legal fee, disbursements, MOT
    "cta":     (64.35, VO_LEN + END_HOLD),  # DM saya / jangan tunggu 8 unit habis
}


def scene_attrs(key):
    a, b = SC[key]
    start = 0 if key == "hook" else F(a)  # hook owns frame 0 (the social thumbnail)
    return f'data-start="{start}" data-duration="{round(F(b) - start, 3)}"'


# ---------------------------------------------------------------- sound design (VO time)
SFX = [
    # hook
    ("pop", 0.05, 0.6), ("tick", 1.34, 0.7), ("tick", 3.08, 0.7), ("tick", 4.34, 0.7),
    ("riser", 4.9, 0.45), ("impact", 6.14, 0.75),
    # reveal
    ("whoosh", 7.95, 0.85), ("impact", 8.54, 0.85),
    # exterior / location
    ("whoosh", 9.65, 0.6), ("pop", 9.92, 0.55), ("pop", 10.27, 0.55), ("swoosh", 11.75, 0.45), ("pop", 13.75, 0.55),
    # price
    ("whoosh", 15.35, 0.8), ("counter", 16.53, 0.5), ("impact", 19.25, 0.8),
    # plan
    ("whoosh", 19.85, 0.75), ("snap", 20.12, 0.6), ("swoosh", 21.24, 0.45),
    ("counter-short", 22.64, 0.5), ("swoosh", 25.45, 0.45), ("counter-short", 26.36, 0.5),
    # interior
    ("swoosh", 29.2, 0.45), *[("tick", round(29.75 + i * 0.09, 3), 0.6) for i in range(4)], ("pop", 29.8, 0.5),
    ("tick", 31.11, 0.6), ("tick", 31.2, 0.6), ("pop", 31.15, 0.5), ("whoosh", 31.95, 0.8), ("pop", 32.3, 0.55),
    # status
    ("whoosh", 35.35, 0.75), ("pop", 36.87, 0.55), ("pop", 37.43, 0.55),
    *[("tick", round(38.55 + i * 0.085, 3), 0.55) for i in range(8)],
    ("impact", 39.23, 0.7),
    # eta
    ("swoosh", 40.5, 0.5), ("sparkle", 42.95, 0.5),
    # location
    ("whoosh", 43.85, 0.8), ("pop", 44.6, 0.45), ("pop", 46.32, 0.55), ("pop", 47.5, 0.55), ("pop", 48.64, 0.55), ("whoosh", 49.45, 0.6),
    ("tick", 51.17, 0.7), ("tick", 52.35, 0.7), ("tick", 53.29, 0.7), ("tick", 54.25, 0.7),
    # promo
    ("whoosh", 55.1, 0.8), ("pop", 56.36, 0.6), ("sparkle", 57.16, 0.45),
    ("pop", 58.4, 0.6), ("pop", 60.16, 0.6), ("pop", 62.0, 0.6),
    # cta
    ("whoosh", 64.2, 0.8), ("pop", 66.75, 0.55), ("impact", 68.87, 0.8),
    *[("tick", round(69.5 + i * 0.07, 3), 0.5) for i in range(8)],
    ("sparkle", 72.45, 0.55),
]
SFX_LEN = {"pop": 0.16, "tick": 0.06, "riser": 1.3, "impact": 1.4, "whoosh": 0.7, "swoosh": 0.38,
           "counter": 1.7, "counter-short": 0.85, "snap": 0.12, "sparkle": 1.6}


def sfx_tags():
    out = []
    busy = {}  # track -> end time; give each cue the first free lane so nothing layers on one track
    for i, (name, t, vol) in enumerate(SFX):
        trk = next(k for k in range(11, 40) if busy.get(k, -1) <= t)
        busy[trk] = t + SFX_LEN[name]
        # whooshes/risers are placed so their peak lands on the cut, so start a bit earlier
        out.append(
            f'<audio id="sfx-{i:02d}-{name}" src="assets/sfx/{name}.wav" data-start="{F(t)}" '
            f'data-duration="{SFX_LEN[name]}" data-volume="{vol}" data-track-index="{trk}"></audio>'
        )
    return "\n      ".join(out)


HOUSE = ('<svg viewBox="0 0 64 64" width="{w}" height="{w}"><path d="M8 30 L32 10 L56 30 L56 56 L8 56 Z" '
         'fill="currentColor"/><rect x="26" y="38" width="12" height="18" fill="rgba(0,0,0,.35)"/></svg>')
PIN = ('<svg viewBox="0 0 48 64" width="{w}" height="{h}"><path d="M24 2C12 2 3 11 3 23c0 16 21 39 21 39s21-23 21-39C45 11 36 2 24 2z" '
       'fill="currentColor"/><circle cx="24" cy="23" r="8" fill="#fff"/></svg>')


# ---------------------------------------------------------------- map (OpenStreetMap data, assets/map/*.json)
import json, math
LON0, LAT0 = 101.53, 2.96
KX = 111.32 * math.cos(math.radians(2.95)) * 100   # world px per degree lon (100 px = 1 km)
KY = 110.57 * 100


def W(lon, lat):
    return (round((lon - LON0) * KX, 1), round(-(lat - LAT0) * KY, 1))


def road_paths(key):
    feats = json.load(open(f"assets/map/{key}.json"))["features"]
    out = []
    for f in feats:
        g = f["geometry"]
        lines = [g["coordinates"]] if g["type"] == "LineString" else g["coordinates"] if g["type"] == "MultiLineString" else []
        for ln in lines:
            pts = [W(*c) for c in ln]
            out.append("M" + " L".join(f"{x},{y}" for x, y in pts))
    return out


def anchor(key, lon, lat):
    tx, ty = W(lon, lat)
    best = None
    for f in json.load(open(f"assets/map/{key}.json"))["features"]:
        if f["geometry"]["type"] != "LineString":
            continue
        for c in f["geometry"]["coordinates"]:
            x, y = W(*c)
            d = (x - tx) ** 2 + (y - ty) ** 2
            if best is None or d < best[0]:
                best = (d, x, y)
    return best[1], best[2]


POIS = {k: W(*v) for k, v in json.load(open("assets/map/pois.json")).items()}
HWY = {  # id: (osm file, label, preferred label spot lon/lat)
    "skve": ("skve", "SKVE", 101.575, 2.945),
    "kesas": ("kesas", "KESAS", 101.50, 3.012),
    "wce": ("wce", "WCE", 101.488, 2.96),
    "lksa": ("lksa", "LKSA", 101.533, 3.02),
}


def map_svg():
    parts = []
    for k in ("ft5", "kebun"):
        parts += [f'<path class="mroad" d="{d}"/>' for d in road_paths(k)]
    for hid, (f, _, _, _) in HWY.items():
        parts += [f'<path class="mhwy" d="{d}"/>' for d in road_paths(f)]
    for hid, (f, _, _, _) in HWY.items():
        parts.append(f'<g id="hl-{hid}" class="mhl">' + "".join(f'<path pathLength="1" d="{d}"/>' for d in road_paths(f)) + "</g>")
    parts += [f'<path class="mpipit" d="{d}"/>' for d in road_paths("pipit")]
    sx, sy = POIS["site"]
    for i, k in enumerate(("tropicana", "eco", "rimbayu"), 1):
        x, y = POIS[k]
        parts.append(f'<path id="mlk{i}" class="mlink" pathLength="1" d="M{sx},{sy} L{x},{y}"/>')
    return "\n          ".join(parts)


def map_js_data():
    anchors = {hid: anchor(f, lo, la) for hid, (f, _, lo, la) in HWY.items()}
    return json.dumps({"pois": POIS, "hwy": anchors})


def houses(cls, n=8, w=96):
    return "".join(f'<div class="{cls}">{HOUSE.format(w=w)}</div>' for _ in range(n))


HTML = r"""<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <!-- GENERATED by build.py: edit build.py, not this file -->
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      @font-face { font-family: "Disp"; src: url("assets/fonts/InterDisplay-Black.otf"); font-weight: 900; }
      @font-face { font-family: "Disp"; src: url("assets/fonts/InterDisplay-ExtraBold.otf"); font-weight: 800; }
      @font-face { font-family: "Disp"; src: url("assets/fonts/InterDisplay-Bold.otf"); font-weight: 700; }
      @font-face { font-family: "Body"; src: url("assets/fonts/Inter-SemiBold.otf"); font-weight: 600; }
      @font-face { font-family: "Body"; src: url("assets/fonts/Inter-Medium.otf"); font-weight: 500; }
      :root {
        --ground: #141416; --charcoal: #26262a; --sand: #e2b384; --sand-ink: #a8703f;
        --paper: #f4f1ec; --ink: #ffffff; --ink-dark: #1c1c1f; --green: #1f7a4a;
        --font-display: "Disp", sans-serif; --font-body: "Body", sans-serif;
      }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: var(--ground); }
      #root { position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: var(--font-body); color: var(--ink); }
      .clip { position: absolute; inset: 0; overflow: hidden; }
      .fill { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
      .kicker { font-family: var(--font-display); font-weight: 800; letter-spacing: .14em; text-transform: uppercase; font-size: 32px; }
      .mega { font-family: var(--font-display); font-weight: 900; letter-spacing: -.035em; line-height: .92; text-transform: uppercase; }
      .shadow { text-shadow: 0 6px 30px rgba(0,0,0,.55), 0 2px 6px rgba(0,0,0,.5); }
      .scrim-top { position: absolute; left: 0; right: 0; top: 0; height: 820px; background: linear-gradient(rgba(0,0,0,.7), rgba(0,0,0,0)); }
      .scrim-bot { position: absolute; left: 0; right: 0; bottom: 0; height: 1000px; background: linear-gradient(rgba(0,0,0,0), rgba(0,0,0,.78)); }
      .dim { position: absolute; inset: 0; background: rgba(14,14,16,.55); }
      .card { position: absolute; display: flex; align-items: center; gap: 22px; padding: 26px 36px 26px 26px; border-radius: 26px; background: rgba(20,20,22,.86); }
      .card .ico { flex: none; width: 70px; height: 70px; border-radius: 18px; background: var(--sand); color: var(--ink-dark); display: flex; align-items: center; justify-content: center; font-family: var(--font-display); font-weight: 900; font-size: 38px; }
      .card .txt { font-family: var(--font-display); font-weight: 800; font-size: 50px; line-height: 1.04; letter-spacing: -.01em; }
      .card .txt small { display: block; font-family: var(--font-body); font-weight: 500; font-size: 30px; opacity: .8; margin-top: 6px; letter-spacing: 0; }
      .chip { position: absolute; display: inline-flex; padding: 14px 26px; border-radius: 999px; font-family: var(--font-display); font-weight: 900; font-size: 32px; letter-spacing: .08em; text-transform: uppercase; }
      .chip.sand { background: var(--sand); color: var(--ink-dark); }
      .chip.white { background: #fff; color: var(--ink-dark); }
      .grid { position: absolute; inset: 0; background-image: linear-gradient(rgba(28,28,31,.06) 2px, transparent 2px), linear-gradient(90deg, rgba(28,28,31,.06) 2px, transparent 2px); background-size: 60px 60px; }

      /* hook */
      #hook-bg { transform-origin: 50% 40%; }
      #hook .renderwrap { position: absolute; left: 0; top: 0; height: 1920px; width: 1080px; overflow: hidden; }
      #hook .renderwrap img { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; object-position: 22% 50%; transform-origin: 30% 45%; }
      #hook .real { transform-origin: 62% 42%; }
      #wipe { opacity: 0; position: absolute; top: 0; left: 0; width: 8px; height: 1920px; margin-left: -4px; background: #fff; box-shadow: 0 0 40px 8px rgba(255,255,255,.55); }
      #hook-head { position: absolute; left: 64px; right: 64px; top: 210px; font-size: 118px; }
      #hook-head em { font-style: normal; color: var(--sand); }
      #checks { position: absolute; left: 64px; top: 1080px; }
      .chk { display: flex; align-items: center; gap: 22px; margin-bottom: 22px; padding: 18px 34px 18px 18px; border-radius: 22px; background: rgba(20,20,22,.84); font-family: var(--font-display); font-weight: 800; font-size: 50px; width: max-content; }
      .chk i { width: 62px; height: 62px; border-radius: 16px; background: var(--sand); color: var(--ink-dark); display: flex; align-items: center; justify-content: center; font-style: normal; font-weight: 900; font-size: 40px; }
      .chk.big { background: var(--sand); color: var(--ink-dark); font-size: 64px; font-weight: 900; }
      .chk.big i { background: var(--ink-dark); color: var(--sand); }
      #reveal-head { opacity: 0; position: absolute; left: 64px; right: 64px; top: 220px; font-size: 112px; }
      #reveal-head em { font-style: normal; color: var(--sand); }
      #tag-render { left: 60px; top: 1500px; opacity: 0; } #tag-real { opacity: 0; } #tag-real { right: 60px; top: 1500px; }

      /* exterior */
      #ext-pin { position: absolute; left: 60px; top: 210px; display: flex; gap: 22px; align-items: flex-start; }
      #ext-pin .pin { color: var(--sand); margin-top: 6px; }
      #ext-pin .l1 { font-family: var(--font-display); font-weight: 900; font-size: 88px; letter-spacing: -.02em; line-height: 1; text-transform: uppercase; }
      #ext-pin .l2 { font-family: var(--font-display); font-weight: 800; font-size: 46px; margin-top: 12px; opacity: .95; }
      #ext-new { left: 60px; top: 1230px; }
      #ext-type { left: 60px; top: 1330px; }

      /* price */
      #price { background: var(--charcoal); }
      #price .bg { filter: blur(14px) brightness(.45); transform: scale(1.1); }
      #price .inner { position: absolute; left: 0; right: 0; top: 560px; text-align: center; }
      #price .lead { font-family: var(--font-display); font-weight: 800; font-size: 56px; letter-spacing: .02em; }
      #price .num { margin-top: 26px; font-family: var(--font-display); font-weight: 900; font-size: 196px; letter-spacing: -.04em; line-height: 1; color: var(--sand); font-variant-numeric: tabular-nums; }
      #price .num span { font-size: 96px; vertical-align: 62px; margin-right: 10px; color: #fff; }
      #price-stamp { position: absolute; left: 50%; top: 1060px; margin-left: -220px; width: 440px; text-align: center; padding: 22px 0; border-radius: 20px; background: #fff; color: var(--ink-dark); font-family: var(--font-display); font-weight: 900; font-size: 72px; letter-spacing: .04em; text-transform: uppercase; }
      #price-sub { position: absolute; left: 0; right: 0; top: 1300px; text-align: center; font-family: var(--font-display); font-weight: 700; font-size: 40px; opacity: .85; }

      /* plan */
      #plan { background: var(--paper); color: var(--ink-dark); }
      #plan-head { position: absolute; left: 60px; top: 170px; }
      #plan-head .kicker { color: var(--sand-ink); margin-bottom: 12px; }
      #plan-head .mega { font-size: 104px; }
      #plan-card { position: absolute; left: 40px; top: 420px; width: 1000px; height: 1010px; border-radius: 34px; overflow: hidden; background: #fff; box-shadow: 0 30px 80px rgba(28,28,31,.18); }
      #plan-cam { position: absolute; left: 0; top: 0; width: 1387px; height: 1849px; transform-origin: 0 0; }
      #plan-cam img, #plan-cam svg { position: absolute; left: 0; top: 0; width: 1387px; height: 1849px; }
      #lot-line { fill: rgba(91,154,74,.16); stroke: #2f8a3e; stroke-width: 10; stroke-dasharray: 4200; stroke-linejoin: round; }
      #bu-line { fill: rgba(226,179,132,.42); stroke: #b87a44; stroke-width: 9; stroke-dasharray: 2200; }
      .stat { position: absolute; padding: 26px 34px; border-radius: 28px; background: var(--charcoal); color: #fff; }
      .stat b { display: block; font-family: var(--font-display); font-weight: 900; font-size: 100px; line-height: 1; color: var(--sand); letter-spacing: -.03em; font-variant-numeric: tabular-nums; }
      .stat b small { font-size: 46px; color: #fff; margin-left: 10px; letter-spacing: 0; }
      .stat span { display: block; margin-top: 10px; font-family: var(--font-display); font-weight: 800; font-size: 32px; letter-spacing: .06em; text-transform: uppercase; }
      #st-land { left: 40px; top: 1480px; width: 490px; }
      #st-bu { left: 550px; top: 1480px; width: 490px; }
      #st-bed { left: 40px; top: 1480px; width: 490px; } #st-bath { left: 550px; top: 1480px; width: 490px; }
      #plan-head2 { position: absolute; left: 60px; top: 170px; opacity: 0; }
      #plan-head2 .kicker { color: var(--sand-ink); margin-bottom: 12px; }
      #plan-head2 .mega { font-size: 104px; }
      .room { position: absolute; border-radius: 10px; border: 7px solid #b87a44; background: rgba(226,179,132,.55); opacity: 0; }
      .room.bath { border-color: #2f7fb8; background: rgba(120,180,230,.45); }
      .room i { position: absolute; left: 50%; top: 50%; width: 52px; height: 52px; margin: -26px 0 0 -26px; border-radius: 50%; background: var(--ink-dark); color: #fff; font-style: normal; font-family: var(--font-display); font-weight: 900; font-size: 30px; display: flex; align-items: center; justify-content: center; }

      /* interior */
      #int-head { position: absolute; left: 60px; top: 210px; }
      #int-head .mega { font-size: 92px; margin-top: 12px; }
      .roomstat { position: absolute; top: 1180px; width: 460px; padding: 30px 34px; border-radius: 30px; background: rgba(20,20,22,.86); }
      .roomstat b { display: block; font-family: var(--font-display); font-weight: 900; font-size: 150px; line-height: .9; color: var(--sand); }
      .roomstat span { display: block; margin-top: 12px; font-family: var(--font-display); font-weight: 800; font-size: 44px; }
      #rs-bed { left: 60px; } #rs-bath { left: 560px; }
      #int-family { left: 60px; top: 1380px; }

      /* status */
      #status { background: var(--paper); color: var(--ink-dark); }
      #status-head { position: absolute; left: 60px; top: 190px; }
      #status-head .kicker { color: var(--sand-ink); margin-bottom: 12px; }
      #status-head .mega { font-size: 104px; }
      .tcard { position: absolute; left: 60px; right: 60px; padding: 34px 40px; border-radius: 30px; background: var(--charcoal); color: #fff; }
      .tcard .k { font-family: var(--font-display); font-weight: 800; font-size: 30px; letter-spacing: .12em; text-transform: uppercase; color: var(--sand); }
      .tcard .v { margin-top: 10px; font-family: var(--font-display); font-weight: 900; font-size: 72px; letter-spacing: -.02em; }
      #tc-lease { top: 520px; } #tc-rizab { top: 740px; }
      #units { position: absolute; left: 60px; right: 60px; top: 1010px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; }
      .unit { height: 150px; border-radius: 24px; background: #fff; color: var(--sand); display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 30px rgba(28,28,31,.08); }
      #units-label { position: absolute; left: 60px; right: 60px; top: 1370px; text-align: center; padding: 30px 0; border-radius: 30px; background: var(--sand); font-family: var(--font-display); font-weight: 900; font-size: 84px; letter-spacing: -.01em; text-transform: uppercase; }

      /* eta */
      #eta-head { position: absolute; left: 60px; right: 60px; top: 210px; }
      #eta-head .mega { font-size: 120px; margin-top: 12px; }
      #eta-head .mega em { font-style: normal; color: var(--sand); }
      #eta-bar { position: absolute; left: 60px; right: 60px; top: 1420px; }
      #eta-bar .track { position: relative; height: 18px; border-radius: 9px; background: rgba(255,255,255,.25); }
      #eta-bar .fillbar { position: absolute; left: 0; top: 0; bottom: 0; width: 100%; border-radius: 9px; background: var(--sand); transform-origin: 0 50%; }
      #eta-bar .dot { position: absolute; top: -15px; width: 48px; height: 48px; border-radius: 50%; background: #fff; border: 8px solid var(--sand); }
      #eta-bar .lbl { position: absolute; top: 60px; font-family: var(--font-display); font-weight: 800; font-size: 36px; white-space: nowrap; }

      /* location */
      #loc { background: #18191c; }
      #loc .mapgrid { position: absolute; inset: 0; background-image: linear-gradient(rgba(255,255,255,.04) 2px, transparent 2px), linear-gradient(90deg, rgba(255,255,255,.04) 2px, transparent 2px); background-size: 72px 72px; }
      #loc svg.map { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
      #loc .mroad { fill: none; stroke: rgba(255,255,255,.16); stroke-width: 5; stroke-linecap: round; stroke-linejoin: round; vector-effect: non-scaling-stroke; }
      #loc .mhwy { fill: none; stroke: rgba(255,255,255,.3); stroke-width: 9; stroke-linecap: round; stroke-linejoin: round; vector-effect: non-scaling-stroke; }
      #loc .mhl { opacity: 0; } #loc .mhl path { fill: none; stroke: #3ecf7a; stroke-width: 13; stroke-linecap: round; stroke-linejoin: round; vector-effect: non-scaling-stroke; }
      #loc .mpipit { fill: none; stroke: var(--sand); stroke-width: 9; stroke-linecap: round; vector-effect: non-scaling-stroke; }
      #loc .mlink { fill: none; stroke: var(--sand); stroke-width: 5; stroke-dasharray: .02 .02; vector-effect: non-scaling-stroke; opacity: 0; }
      #loc-head { position: absolute; left: 60px; top: 190px; z-index: 2; }
      #loc-head .mega { font-size: 104px; margin-top: 12px; }
      #loc .topfade { position: absolute; left: 0; right: 0; top: 0; height: 460px; background: linear-gradient(#18191c 55%, rgba(24,25,28,0)); z-index: 1; }
      #loc .botfade { position: absolute; left: 0; right: 0; bottom: 0; height: 560px; background: linear-gradient(rgba(24,25,28,0), #18191c 45%); z-index: 1; }
      .poi { position: absolute; left: 0; top: 0; z-index: 1; }
      .poi .p { position: absolute; left: -20px; top: -52px; color: #fff; }
      .poi .n { position: absolute; top: -50px; padding: 12px 22px; border-radius: 14px; background: #fff; color: var(--ink-dark); font-family: var(--font-display); font-weight: 800; font-size: 36px; white-space: nowrap; }
      .poi .n.r { left: 34px; } .poi .n.l { right: 34px; }
      #poi-home .p { color: var(--sand); left: -24px; top: -64px; }
      #poi-home .n { background: var(--sand); top: 6px; left: -110px; }
      .hlabel { position: absolute; left: 0; top: 0; z-index: 1; margin: -32px 0 0 -70px; width: 140px; text-align: center; padding: 10px 0; border-radius: 12px; background: var(--green); border: 4px solid #fff; font-family: var(--font-display); font-weight: 900; font-size: 34px; letter-spacing: .04em; opacity: 0; }
      #hwy { position: absolute; left: 60px; right: 60px; top: 1560px; display: flex; gap: 18px; z-index: 2; }
      .hw { flex: 1; text-align: center; padding: 22px 0; border-radius: 16px; background: var(--green); border: 5px solid #fff; font-family: var(--font-display); font-weight: 900; font-size: 46px; letter-spacing: .04em; }
      #hwy-label { position: absolute; left: 60px; top: 1480px; z-index: 2; }
      #loc-note { position: absolute; right: 60px; top: 1760px; font-size: 28px; opacity: .55; z-index: 2; }

      /* promo */
      #promo { background: var(--sand); color: var(--ink-dark); }
      #promo .rays { position: absolute; left: 50%; top: 50%; width: 2600px; height: 2600px; margin: -1300px 0 0 -1300px; background: repeating-conic-gradient(rgba(255,255,255,.16) 0 10deg, rgba(255,255,255,0) 10deg 20deg); }
      #promo-head { position: absolute; left: 60px; top: 190px; }
      #promo-head .mega { font-size: 120px; }
      #ticket { position: absolute; left: 60px; right: 60px; top: 470px; padding: 40px 44px; border-radius: 34px; background: var(--ink-dark); color: #fff; }
      #ticket .k { font-family: var(--font-display); font-weight: 800; font-size: 36px; letter-spacing: .12em; text-transform: uppercase; color: var(--sand); }
      #ticket .v { margin-top: 8px; font-family: var(--font-display); font-weight: 900; font-size: 150px; letter-spacing: -.04em; line-height: 1; }
      #ticket .v small { font-size: 56px; letter-spacing: 0; margin-left: 12px; opacity: .85; }
      .free { position: absolute; left: 60px; right: 60px; display: flex; align-items: center; gap: 26px; padding: 26px 34px; border-radius: 28px; background: #fff; box-shadow: 0 16px 40px rgba(28,28,31,.15); }
      .free .tag { flex: none; padding: 12px 22px; border-radius: 14px; background: var(--green); color: #fff; font-family: var(--font-display); font-weight: 900; font-size: 40px; letter-spacing: .06em; }
      .free .t { font-family: var(--font-display); font-weight: 900; font-size: 54px; letter-spacing: -.01em; }
      #fr1 { top: 880px; } #fr2 { top: 1060px; } #fr3 { top: 1240px; }
      #promo-note { position: absolute; left: 60px; right: 60px; top: 1430px; font-family: var(--font-display); font-weight: 700; font-size: 38px; }

      /* cta */
      #cta-pan { position: absolute; left: 0; top: 0; height: 1920px; width: 3413px; }
      #cta-pan img { width: 3413px; height: 1920px; display: block; }
      #cta-head { position: absolute; left: 60px; right: 60px; top: 220px; }
      #cta-head .mega { font-size: 136px; }
      #cta-q { left: 60px; top: 480px; }
      #cta-loan { left: 60px; top: 600px; }
      #cta-btn { position: absolute; left: 60px; right: 60px; top: 1130px; text-align: center; padding: 40px 0; border-radius: 999px; background: var(--sand); color: var(--ink-dark); font-family: var(--font-display); font-weight: 900; font-size: 84px; letter-spacing: -.01em; text-transform: uppercase; box-shadow: 0 20px 60px rgba(0,0,0,.4); }
      #cta-units { position: absolute; left: 60px; right: 60px; top: 1330px; display: flex; justify-content: space-between; }
      .cunit { width: 108px; height: 108px; border-radius: 22px; background: rgba(20,20,22,.86); color: var(--sand); display: flex; align-items: center; justify-content: center; }
      #cta-scar { position: absolute; left: 0; right: 0; top: 1480px; text-align: center; font-family: var(--font-display); font-weight: 900; font-size: 60px; }
      #endcard { position: absolute; inset: 0; background: rgba(18,18,20,.9); }
      #endcard .inner { position: absolute; left: 70px; right: 70px; top: 560px; text-align: center; }
      #endcard .logo { font-family: var(--font-display); font-weight: 900; font-size: 104px; letter-spacing: -.02em; line-height: .95; text-transform: uppercase; }
      #endcard .logo span { color: var(--sand); display: block; font-size: 78px; margin-top: 18px; letter-spacing: -.01em; }
      #endcard .bar { width: 160px; height: 10px; background: var(--sand); margin: 40px auto; border-radius: 5px; }
      #endcard .sub { font-family: var(--font-display); font-weight: 700; font-size: 44px; opacity: .92; line-height: 1.3; }
      #endcard .btn { margin-top: 70px; display: inline-flex; padding: 34px 56px; border-radius: 999px; background: var(--sand); color: var(--ink-dark); font-family: var(--font-display); font-weight: 900; font-size: 56px; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="__FILM__" data-width="1080" data-height="1920">

      <!-- 1 · HOOK: qualifying checklist over the render, then render -> realiti wipe -->
      <div id="hook" class="clip" __SC_hook__ data-track-index="1">
        <img class="fill real" src="assets/img/real-corner.jpg" alt="" />
        <div class="renderwrap"><img id="hook-bg" src="assets/img/render-corner.jpg" alt="" /></div>
        <div id="wipe"></div>
        <div class="scrim-top"></div>
        <div class="scrim-bot" id="hook-scrim"></div>
        <div id="hook-head" class="mega shadow">Semi-D bawah <em>RM500K?</em></div>
        <div id="checks">
          <div class="chk" id="ck1"><i>&#10003;</i>Semi-D setingkat</div>
          <div class="chk" id="ck2"><i>&#10003;</i>Tanah luas</div>
          <div class="chk" id="ck3"><i>&#10003;</i>Lokasi strategik</div>
          <div class="chk big" id="ck4"><i>&#10003;</i>Bawah RM500K</div>
        </div>
        <div id="reveal-head" class="mega shadow">Cuba tengok <em>yang ini.</em></div>
        <div id="tag-render" class="chip white">Render 3D</div>
        <div id="tag-real" class="chip sand">Tapak sebenar</div>
      </div>

      <!-- 2 · EXTERIOR (slow-mo arc): location + product type -->
      <video id="v-ext" class="clip fill" src="assets/footage/exterior-slow.mp4" __SC_ext__ data-media-start="0" muted playsinline data-track-index="0"></video>
      <div id="ext" class="clip" __SC_ext__ data-track-index="1">
        <div class="scrim-top"></div>
        <div class="scrim-bot"></div>
        <div id="ext-pin">
          <div class="pin">__PIN90__</div>
          <div><div class="l1 shadow">Jalan Pipit</div><div class="l2 shadow">Telok Panglima Garang</div></div>
        </div>
        <div id="ext-new" class="chip sand">Projek baharu</div>
        <div id="ext-type" class="card"><div class="ico">1</div><div class="txt">Rumah berkembar<small>Semi-D 1 tingkat</small></div></div>
      </div>

      <!-- 3 · PRICE -->
      <div id="price" class="clip" __SC_price__ data-track-index="1">
        <img class="fill bg" src="assets/img/render-front.jpg" alt="" />
        <div class="inner">
          <div class="lead">Harga bermula</div>
          <div class="num"><span>RM</span><b id="price-num">485,700</b></div>
        </div>
        <div id="price-stamp">Sahaja</div>
      </div>

      <!-- 4 · PLAN: land + built-up -->
      <div id="plan" class="clip" __SC_plan__ data-track-index="1">
        <div class="grid"></div>
        <div id="plan-head"><div class="kicker">Apa yang menarik?</div><div class="mega">Tanah luas</div></div>
        <div id="plan-head2"><div class="kicker">Susun atur</div><div class="mega">4 + 2 bilik</div></div>
        <div id="plan-card">
          <div id="plan-cam">
            <img src="assets/img/floorplan.png" alt="" />
            <svg viewBox="0 0 1387 1849">
              <polygon id="lot-line" points="342,425 1285,425 1285,1433 565,1433 270,1175" />
              <polygon id="bu-line" points="772,636 1262,636 1262,1172 772,1172" />
            </svg>
            <div class="room bed" style="left:1038px;top:676px;width:186px;height:96px"><i>1</i></div>
            <div class="room bed" style="left:1038px;top:782px;width:226px;height:90px"><i>2</i></div>
            <div class="room bed" style="left:1040px;top:880px;width:222px;height:72px"><i>3</i></div>
            <div class="room bed" style="left:1038px;top:1048px;width:226px;height:124px"><i>4</i></div>
            <div class="room bath" style="left:842px;top:796px;width:134px;height:68px"><i>B</i></div>
            <div class="room bath" style="left:1126px;top:988px;width:136px;height:54px"><i>B</i></div>
          </div>
        </div>
        <div class="stat" id="st-land"><b><em id="n-land">2,814</em><small>kps</small></b><span>Keluasan tanah&nbsp;&plusmn;</span></div>
        <div class="stat" id="st-bu"><b><em id="n-bu">1,266</em><small>kps</small></b><span>Keluasan binaan</span></div>
        <div class="stat" id="st-bed"><b>4</b><span>Bilik tidur</span></div>
        <div class="stat" id="st-bath"><b>2</b><span>Bilik air</span></div>
      </div>

      <!-- 5 · INTERIOR (slow-mo): rooms -->
      <video id="v-int" class="clip fill" src="assets/footage/interior-slow.mp4" __SC_int__ data-media-start="0" muted playsinline data-track-index="0"></video>
      <div id="int" class="clip" __SC_int__ data-track-index="1">
        <div class="scrim-top"></div>
        <div class="scrim-bot"></div>
        <div id="int-head"><div class="kicker shadow">Dalam rumah</div><div class="mega shadow">Ruang selesa</div></div>
        <div id="int-family" class="card"><div class="ico">&#9829;</div><div class="txt">Sesuai untuk keluarga</div></div>
      </div>

      <!-- 6 · STATUS: tenure + units -->
      <div id="status" class="clip" __SC_status__ data-track-index="1">
        <div class="grid"></div>
        <div id="status-head"><div class="kicker">Info projek</div><div class="mega">Status</div></div>
        <div class="tcard" id="tc-lease"><div class="k">Pegangan</div><div class="v">Leasehold</div></div>
        <div class="tcard" id="tc-rizab"><div class="k">Status tanah</div><div class="v">Rizab Melayu</div></div>
        <div id="units">__UNITS__</div>
        <div id="units-label">8 unit sahaja</div>
      </div>

      <!-- 7 · ETA: real site today -> Q4 2027 -->
      <div id="eta" class="clip" __SC_eta__ data-track-index="1">
        <img class="fill" id="eta-bg" src="assets/img/real-corner.jpg" alt="" />
        <div class="scrim-top"></div>
        <div class="scrim-bot"></div>
        <div id="eta-head"><div class="kicker shadow">Dijangka siap</div><div class="mega shadow">Suku ke-4 <em>2027</em></div></div>
        <div id="eta-bar">
          <div class="track"><div class="fillbar" id="eta-fill"></div></div>
          <div class="dot" style="left:-6px"></div><div class="lbl shadow" style="left:0">Sekarang</div>
          <div class="dot" id="eta-dot" style="right:-6px"></div><div class="lbl shadow" id="eta-lbl" style="right:0">Q4 2027</div>
        </div>
      </div>

      <!-- 8 · LOCATION: real road geometry (OpenStreetMap), animated camera -->
      <div id="loc" class="clip" __SC_loc__ data-track-index="1">
        <div class="mapgrid"></div>
        <svg class="map" data-layout-allow-overflow viewBox="0 0 1080 1920">
          <g id="mworld">
          __MAPSVG__
          </g>
        </svg>
        <div class="poi" id="poi-home"><div class="p">__PIN64__</div><div class="n">Tapak projek</div></div>
        <div class="poi" id="poi-1"><div class="p">__PIN52__</div><div class="n l">Tropicana Aman</div></div>
        <div class="poi" id="poi-2"><div class="p">__PIN52__</div><div class="n r">Eco Sanctuary</div></div>
        <div class="poi" id="poi-3"><div class="p">__PIN52__</div><div class="n l">Bandar Rimbayu</div></div>
        <div class="hlabel" id="hl-lb-skve">SKVE</div><div class="hlabel" id="hl-lb-kesas">KESAS</div>
        <div class="hlabel" id="hl-lb-wce">WCE</div><div class="hlabel" id="hl-lb-lksa">LKSA</div>
        <div class="topfade"></div><div class="botfade"></div>
        <div id="loc-head"><div class="kicker" style="color:var(--sand)">Lokasi</div><div class="mega">Dekat dengan</div></div>
        <div id="hwy-label" class="kicker" style="color:var(--sand)">Akses mudah</div>
        <div id="hwy"><div class="hw" id="hw1">SKVE</div><div class="hw" id="hw2">KESAS</div><div class="hw" id="hw3">WCE</div><div class="hw" id="hw4">LKSA</div></div>
        <div id="loc-note">Data peta &copy; OpenStreetMap</div>
      </div>

      <!-- 9 · PROMO -->
      <div id="promo" class="clip" __SC_promo__ data-track-index="1">
        <div class="rays" id="rays"></div>
        <div id="promo-head"><div class="mega">Lagi menarik!</div></div>
        <div id="ticket"><div class="k">Booking hanya</div><div class="v">RM1,000</div></div>
        <div class="free" id="fr1"><div class="tag">FREE</div><div class="t">SPA legal fee</div></div>
        <div class="free" id="fr2"><div class="tag">FREE</div><div class="t">SPA disbursements</div></div>
        <div class="free" id="fr3"><div class="tag">FREE</div><div class="t">MOT*</div></div>
        <div id="promo-note">*Untuk pembeli rumah pertama</div>
      </div>

      <!-- 10 · CTA + end card -->
      <div id="cta" class="clip" __SC_cta__ data-track-index="1">
        <div id="cta-pan"><img src="assets/img/render-front.jpg" alt="" /></div>
        <div class="dim"></div>
        <div id="cta-head"><div class="mega shadow">Berminat?</div></div>
        <div id="cta-q" class="card"><div class="ico">?</div><div class="txt">Nak tahu lebih lanjut</div></div>
        <div id="cta-loan" class="card" style="top:780px"><div class="ico">&#10003;</div><div class="txt">Semak kelayakan pinjaman</div></div>
        <div id="cta-btn">DM saya sekarang</div>
        <div id="cta-units">__CUNITS__</div>
        <div id="cta-scar" class="shadow">Jangan tunggu 8 unit ni habis!</div>
        <div id="endcard">
          <div class="inner">
            <div class="logo">Jalan Pipit<br /><span>Telok Panglima Garang</span></div>
            <div class="bar"></div>
            <div class="sub">Dari RM485,700 &middot; 8 unit sahaja</div>
            <div class="btn">DM untuk info</div>
          </div>
        </div>
      </div>

      <!-- AUDIO -->
      <audio id="a-vo" src="assets/vo/voiceover-tight.wav" data-start="__VO_START__" data-duration="__VO_LEN__" data-media-start="0" data-volume="1" data-track-index="9"></audio>
      <audio id="a-music" src="assets/sfx/music-long.wav" data-start="0" data-duration="76" data-media-start="0" data-volume="0.16" data-fade-in="0.4" data-fade-out="2.5" data-track-index="10"></audio>
      __SFX__
    </div>

    <script>
      window.__timelines = window.__timelines || {};
      const VO = __VO_START__;
      const v = (t) => +(t + VO).toFixed(3);   // VO time -> film time
      const tl = gsap.timeline({ paused: true });
      const W = 1080;
      const popIn = (sel, t, from = {}) => tl.fromTo(sel, { y: 50, opacity: 0, scale: .9, ...from }, { y: 0, x: 0, opacity: 1, scale: 1, duration: .38, ease: "back.out(1.9)" }, v(t));
      const outUp = (sel, t) => tl.to(sel, { y: -40, opacity: 0, duration: .22, ease: "power2.in", stagger: .03 }, v(t));
      const counter = (sel, to, t, d) => { const o = { n: 0 }; tl.to(o, { n: to, duration: d, ease: "power3.out", onUpdate: () => { document.querySelector(sel).textContent = Math.round(o.n).toLocaleString("en-US"); } }, v(t)); };

      /* 1 · HOOK */
      // frame 0 is the thumbnail: headline already on screen, it just settles
      tl.set("#hook .renderwrap", { width: W }, 0).set("#wipe", { x: W }, 0)
        .fromTo("#hook-bg", { scale: 1.0 }, { scale: 1.12, duration: v(8.1), ease: "none" }, 0)
        .fromTo("#hook-head", { scale: 1.08 }, { scale: 1, duration: .5, ease: "expo.out" }, 0);
      popIn("#ck1", 1.34, { x: -60, y: 0 }); popIn("#ck2", 3.08, { x: -60, y: 0 }); popIn("#ck3", 4.34, { x: -60, y: 0 });
      popIn("#ck4", 6.14, { scale: 1.4, y: 0 });
      tl.to("#hook-head em", { scale: 1.08, duration: .18, yoyo: true, repeat: 1, transformOrigin: "50% 50%", display: "inline-block" }, v(6.14));
      // reveal on "cuba tengok yang ini"
      outUp("#hook-head, .chk", 7.75);
      tl.to("#wipe", { opacity: 1, duration: .05 }, v(8.0))
        .to("#hook .renderwrap", { width: 0, duration: .55, ease: "power3.inOut" }, v(8.0))
        .to("#wipe", { x: 0, duration: .55, ease: "power3.inOut" }, v(8.0))
        .fromTo("#hook .real", { scale: 1.18 }, { scale: 1.04, duration: 1.2, ease: "power2.out" }, v(8.5))
        .fromTo("#reveal-head", { scale: 1.3, opacity: 0 }, { scale: 1, opacity: 1, duration: .3, ease: "expo.out" }, v(8.5))
        .to("#hook .renderwrap", { width: W * .5, duration: .4, ease: "power3.out" }, v(8.56))
        .to("#wipe", { x: W * .5, duration: .4, ease: "power3.out" }, v(8.56))
        .to("#tag-render, #tag-real", { opacity: 1, duration: .2 }, v(8.6));

      /* 2 · EXTERIOR */
      tl.fromTo("#v-ext", { scale: 1.15 }, { scale: 1.0, duration: .5, ease: "power3.out" }, v(9.8));
      popIn("#ext-pin", 9.9, { x: -60, y: 0 });
      tl.fromTo("#ext-pin .l2", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: .3 }, v(10.27));
      popIn("#ext-new", 11.85, { x: -60, y: 0 }); popIn("#ext-type", 13.75, { x: -80, y: 0 });
      outUp("#ext-pin, #ext-new, #ext-type", 15.3);

      /* 3 · PRICE */
      tl.fromTo("#price .bg", { scale: 1.25 }, { scale: 1.1, duration: 4.4, ease: "power1.out" }, v(15.55))
        .fromTo("#price .lead", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: .35, ease: "power3.out" }, v(15.7))
        .fromTo("#price .num", { scale: .7, opacity: 0 }, { scale: 1, opacity: 1, duration: .4, ease: "back.out(1.6)" }, v(16.45));
      counter("#price-num", 485700, 16.5, 1.75);
      tl.fromTo("#price-stamp", { scale: 2.2, opacity: 0, rotation: -8 }, { scale: 1, opacity: 1, rotation: -4, duration: .25, ease: "power4.in" }, v(19.0))
        .fromTo("#price .inner", { x: 0 }, { x: 10, duration: .05, yoyo: true, repeat: 5 }, v(19.25))


      /* 4 · PLAN */
      const cam = (s, cx, cy) => ({ scale: s, x: 500 - cx * s, y: 505 - cy * s });
      tl.set("#plan-cam", cam(.9615, 770, 930), v(20.0))
        .set("#lot-line", { attr: { "stroke-dashoffset": 4200 }, fillOpacity: 0 }, v(20.0))
        .set("#bu-line", { attr: { "stroke-dashoffset": 2200 }, fillOpacity: 0 }, v(20.0))
        .fromTo("#plan-head", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: .4, ease: "power3.out" }, v(20.1))
        .fromTo("#plan-card", { y: 160, opacity: 0, rotation: -2 }, { y: 0, opacity: 1, rotation: 0, duration: .55, ease: "power3.out" }, v(20.1))
        .to("#lot-line", { attr: { "stroke-dashoffset": 0 }, duration: 1.1, ease: "power2.inOut" }, v(21.24))
        .to("#lot-line", { fillOpacity: 1, duration: .4 }, v(22.2));
      popIn("#st-land", 22.5); counter("#n-land", 2814, 22.64, .85);
      tl.to("#plan-cam", { ...cam(1.32, 905, 905), duration: .8, ease: "power3.inOut" }, v(25.45))
        .to("#lot-line", { opacity: .35, duration: .3 }, v(25.45))
        .to("#bu-line", { attr: { "stroke-dashoffset": 0 }, duration: .8, ease: "power2.inOut" }, v(25.85))
        .to("#bu-line", { fillOpacity: 1, duration: .3 }, v(26.55));
      popIn("#st-bu", 26.2); counter("#n-bu", 1266, 26.36, .85);
      // rooms: "Siap ada 4 bilik tidur dan 2 bilik air" (STORE on the drawing is counted as a bedroom)
      tl.to("#plan-head, #st-land, #st-bu", { opacity: 0, y: -30, duration: .22, ease: "power2.in" }, v(29.2))
        .fromTo("#plan-head2", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .35, ease: "power3.out" }, v(29.35))
        .to("#bu-line", { fillOpacity: 0, opacity: .5, duration: .3 }, v(29.4))
        .fromTo(".room.bed", { opacity: 0, scale: .6 }, { opacity: 1, scale: 1, duration: .3, stagger: .09, ease: "back.out(2.2)" }, v(29.75))
        .fromTo(".room.bath", { opacity: 0, scale: .6 }, { opacity: 1, scale: 1, duration: .3, stagger: .09, ease: "back.out(2.2)" }, v(31.11));
      popIn("#st-bed", 29.8, { scale: 1.3, y: 0 }); popIn("#st-bath", 31.15, { scale: 1.3, y: 0 });
      outUp("#plan-head2, #plan-card, #st-bed, #st-bath", 31.9);

      /* 5 · INTERIOR */
      tl.fromTo("#v-int", { scale: 1.15 }, { scale: 1.02, duration: .5, ease: "power3.out" }, v(32.1));
      popIn("#int-head", 32.2, { x: -60, y: 0 });
      popIn("#int-family", 32.5, { x: -80, y: 0 });
      outUp("#int-head, #int-family", 35.25);

      /* 6 · STATUS */
      tl.fromTo("#status-head", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: .4, ease: "power3.out" }, v(35.6));
      popIn("#tc-lease", 36.87, { x: -100, y: 0 }); popIn("#tc-rizab", 37.43, { x: -100, y: 0 });
      tl.fromTo(".unit", { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: .3, stagger: .085, ease: "back.out(2.4)" }, v(38.55));
      popIn("#units-label", 39.23, { scale: 1.5, y: 0 });
      tl.to(".unit", { color: "#1c1c1f", duration: .2, stagger: .04 }, v(39.4));
      outUp("#status-head, .tcard, #units, #units-label", 40.4);

      /* 7 · ETA */
      tl.fromTo("#eta-bg", { scale: 1.22 }, { scale: 1.05, duration: 3.4, ease: "power1.out" }, v(40.6));
      popIn("#eta-head", 40.75, { x: -60, y: 0 });
      tl.fromTo("#eta-fill", { scaleX: 0 }, { scaleX: 1, duration: 1.8, ease: "power2.inOut" }, v(41.3))
        .fromTo("#eta-dot, #eta-lbl", { opacity: 0, scale: .5 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }, v(42.95))
        .to("#eta-head em", { scale: 1.12, duration: .2, yoyo: true, repeat: 1, display: "inline-block", transformOrigin: "0 50%" }, v(42.99));

      /* 8 · LOCATION: camera over real road geometry; pins/labels follow the camera */
      const MAP = __MAPDATA__;
      const MC = { s: 1.2, x: -20, y: 260 };           // camera: scale + world point at screen focus
      const FX = 540, FY = 960;
      const toScr = (wx, wy) => [FX + (wx - MC.x) * MC.s, FY + (wy - MC.y) * MC.s];
      const place = (sel, w) => { const [x, y] = toScr(w[0], w[1]); const el = document.querySelector(sel); el.style.left = x + "px"; el.style.top = y + "px"; };
      const applyCam = () => {
        document.querySelector("#mworld").setAttribute("transform", `translate(${FX - MC.x * MC.s} ${FY - MC.y * MC.s}) scale(${MC.s})`);
        place("#poi-home", MAP.pois.site); place("#poi-1", MAP.pois.tropicana); place("#poi-2", MAP.pois.eco); place("#poi-3", MAP.pois.rimbayu);
        for (const k in MAP.hwy) place("#hl-lb-" + k, MAP.hwy[k]);
      };
      const TOWNS = { s: 1.7, x: -13, y: 278 };        // site + three townships
      const WIDE = { s: .72, x: -110, y: -60 };          // site + SKVE/WCE/KESAS/LKSA
      tl.set(MC, { ...TOWNS, s: 1.2, onUpdate: applyCam }, v(44.0))
        .call(applyCam, null, v(44.0))
        .to(MC, { ...TOWNS, duration: 1.4, ease: "power3.out", onUpdate: applyCam }, v(44.0))
        .fromTo("#loc svg.map", { opacity: 0 }, { opacity: 1, duration: .5 }, v(44.0))
        .fromTo("#loc-head", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: .4, ease: "power3.out" }, v(44.15));
      popIn("#poi-home", 44.6, { y: -60 });
      [["#mlk1", "#poi-1", 46.32], ["#mlk2", "#poi-2", 47.5], ["#mlk3", "#poi-3", 48.64]].forEach(([lk, p, t]) => {
        tl.fromTo(lk, { opacity: 0 }, { opacity: 1, duration: .3 }, v(t - .15));
        popIn(p, t, { y: -50 });
      });
      // "Akses pun mudah..." -> pull back to show the highway network
      tl.to(MC, { ...WIDE, duration: 1.3, ease: "power3.inOut", onUpdate: applyCam }, v(49.6))
        .to("#poi-1 .n, #poi-2 .n, #poi-3 .n, .mlink", { opacity: 0, duration: .3 }, v(49.6))
        .fromTo("#hwy-label", { opacity: 0 }, { opacity: 1, duration: .3 }, v(49.83));
      [["skve", "#hw1", 51.17], ["kesas", "#hw2", 52.35], ["wce", "#hw3", 53.29], ["lksa", "#hw4", 54.25]].forEach(([k, h, t]) => {
        tl.fromTo(`#hl-${k}`, { opacity: 0 }, { opacity: 1, duration: .25 }, v(t - .05))
          .fromTo(`#hl-${k} path`, { attr: { "stroke-width": 30 } }, { attr: { "stroke-width": 13 }, duration: .5, ease: "power2.out" }, v(t - .05))
          .fromTo(`#hl-lb-${k}`, { opacity: 0, scale: .6 }, { opacity: 1, scale: 1, duration: .3, ease: "back.out(2)" }, v(t));
        popIn(h, t, { y: 60 });
      });
      tl.fromTo("#loc-note", { opacity: 0 }, { opacity: .55, duration: .3 }, v(46.0));
      tl.to(MC, { s: .66, duration: 1.4, ease: "none", onUpdate: applyCam }, v(53.7));
      outUp("#loc-head, .poi, .hlabel, #hwy, #hwy-label, #loc-note", 55.0);

      /* 9 · PROMO */
      tl.fromTo("#rays", { rotation: 0 }, { rotation: 40, duration: 9.1, ease: "none" }, v(55.25));
      popIn("#promo-head", 55.38, { scale: 1.3, y: 0 });
      popIn("#ticket", 56.36, { y: 80 });
      tl.fromTo("#ticket .v", { scale: .8 }, { scale: 1, duration: .3, ease: "back.out(3)", transformOrigin: "0 50%" }, v(57.16));
      popIn("#fr1", 58.4, { x: -120, y: 0 }); popIn("#fr2", 60.16, { x: -120, y: 0 }); popIn("#fr3", 62.0, { x: -120, y: 0 });
      tl.fromTo("#promo-note", { opacity: 0 }, { opacity: 1, duration: .3 }, v(62.9));
      outUp("#promo-head, #ticket, .free, #promo-note", 64.1);

      /* 10 · CTA */
      tl.fromTo("#cta-pan", { x: -2333, scale: 1.08 }, { x: -600, scale: 1.0, duration: v(VO_LEN_JS) - v(64.35) + 2.6, ease: "power1.out" }, v(64.35));
      popIn("#cta-head", 64.6, { scale: 1.3, y: 0 });
      popIn("#cta-q", 65.3, { x: -80, y: 0 }); popIn("#cta-loan", 66.75, { x: -80, y: 0 });
      popIn("#cta-btn", 68.75, { scale: 1.4, y: 0 });
      tl.to("#cta-btn", { scale: 1.05, duration: .3, yoyo: true, repeat: 3, ease: "sine.inOut" }, v(69.3));
      tl.fromTo(".cunit", { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: .25, stagger: .07, ease: "back.out(2.4)" }, v(69.5));
      tl.fromTo("#cta-scar", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3 }, v(70.0));
      tl.to(".cunit", { opacity: .25, duration: .15, stagger: .06 }, v(71.5));
      outUp("#cta-head, #cta-q, #cta-loan, #cta-btn, #cta-units, #cta-scar", 72.1);
      tl.fromTo("#endcard", { opacity: 0 }, { opacity: 1, duration: .4 }, v(72.35))
        .fromTo("#endcard .logo", { y: 60, opacity: 0, scale: .92 }, { y: 0, opacity: 1, scale: 1, duration: .45, ease: "expo.out" }, v(72.5))
        .fromTo("#endcard .bar", { scaleX: 0 }, { scaleX: 1, duration: .4, ease: "power3.out" }, v(72.7))
        .fromTo("#endcard .sub", { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: .35 }, v(72.8))
        .fromTo("#endcard .btn", { y: 40, opacity: 0, scale: .85 }, { y: 0, opacity: 1, scale: 1, duration: .4, ease: "back.out(2.2)" }, v(73.0));

      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""

html = HTML
for k in SC:
    html = html.replace(f"__SC_{k}__", scene_attrs(k))
html = (html.replace("__FILM__", str(FILM)).replace("__VO_START__", str(VO_START)).replace("__VO_LEN__", str(VO_LEN))
        .replace("VO_LEN_JS", str(VO_LEN)).replace("__SFX__", sfx_tags())
        .replace("__UNITS__", houses("unit", 8, 96)).replace("__CUNITS__", houses("cunit", 8, 70))
        .replace("__PIN90__", PIN.format(w=68, h=90)).replace("__PIN64__", PIN.format(w=48, h=64))
        .replace("__PIN52__", PIN.format(w=40, h=52))
        .replace("__MAPSVG__", map_svg()).replace("__MAPDATA__", map_js_data()))
assert "__" not in html.replace("window.__timelines", ""), "unreplaced placeholder"
open("index.html", "w").write(html)
print("index.html written, film", FILM, "s,", len(SFX), "sfx cues")
