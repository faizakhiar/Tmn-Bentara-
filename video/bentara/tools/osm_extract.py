import osmium, json, sys, math
pbf, out = sys.argv[1], sys.argv[2]
LO0, LO1, LA0, LA1 = 101.40, 101.68, 2.80, 3.10
inb = lambda lon, lat: LO0 <= lon <= LO1 and LA0 <= lat <= LA1
AREA_KEYS = {
  "water": lambda t: t.get("natural") == "water" or t.get("waterway") == "riverbank" or t.get("landuse") in ("reservoir", "basin"),
  "wetland": lambda t: t.get("natural") == "wetland" or t.get("wetland") is not None,
  "park": lambda t: t.get("leisure") in ("park", "golf_course", "garden", "pitch", "playground", "nature_reserve") or t.get("landuse") in ("grass", "recreation_ground", "village_green"),
  "forest": lambda t: t.get("landuse") == "forest" or t.get("natural") in ("wood", "scrub"),
  "farm": lambda t: t.get("landuse") in ("farmland", "orchard", "plantation", "meadow", "farmyard", "aquaculture"),
  "urban": lambda t: t.get("landuse") in ("residential", "commercial", "retail", "industrial", "construction", "education", "institutional"),
  "building": lambda t: "building" in t,
}
class H(osmium.SimpleHandler):
    def __init__(s):
        super().__init__(); s.roads=[]; s.rivers=[]; s.areas=[]; s.places=[]
    def node(s, n):
        t = n.tags
        if "place" in t and "name" in t and t["place"] in ("city","town","suburb","village","neighbourhood","hamlet","quarter") and inb(n.location.lon, n.location.lat):
            s.places.append({"name": t["name"], "type": t["place"], "c": [n.location.lon, n.location.lat]})
    def way(s, w):
        t = w.tags
        hw = t.get("highway"); ww = t.get("waterway")
        if not hw and ww not in ("river","stream","canal","drain"): return
        try: pts = [[nd.location.lon, nd.location.lat] for nd in w.nodes]
        except osmium.InvalidLocationError: return
        if not any(inb(*p) for p in pts): return
        if hw:
            if hw in ("footway","path","steps","cycleway","bridleway","corridor","proposed","platform","elevator"): return
            s.roads.append({"hw": hw, "name": t.get("name",""), "ref": t.get("ref",""), "c": pts})
        else:
            s.rivers.append({"ww": ww, "name": t.get("name",""), "c": pts})
    def area(s, a):
        t = a.tags; kind = next((k for k,f in AREA_KEYS.items() if f(t)), None)
        if not kind: return
        try:
            for outer in a.outer_rings():
                ring = [[n.lon, n.lat] for n in outer]
                if not any(inb(*p) for p in ring): continue
                holes = [[[n.lon, n.lat] for n in inner] for inner in a.inner_rings(outer)]
                s.areas.append({"k": kind, "name": t.get("name",""), "c": ring, "h": holes})
        except Exception: pass
h = H(); h.apply_file(pbf, locations=True, idx="flex_mem")
json.dump({"roads": h.roads, "rivers": h.rivers, "areas": h.areas, "places": h.places}, open(out, "w"))
from collections import Counter
print("roads", len(h.roads), Counter(r["hw"] for r in h.roads).most_common(12))
print("rivers", len(h.rivers), "areas", Counter(a["k"] for a in h.areas), "places", len(h.places))
