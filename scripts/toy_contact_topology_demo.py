import json
import math
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)

# Toy 2D contact task:
# A finger moves from left to right around a circular object.
# Topology is represented by whether the path goes above or below the object.
# Smoothness is path length / curvature proxy.

start = (-2.0, 0.0)
goal = (2.0, 0.0)
waypoints = [(-1.0, 0.0), (0.0, 0.0), (1.0, 0.0)]
alts = [-1.0, 1.0]

def path_from_bits(bits):
    pts = [start]
    for x, b in zip([-1.0, 0.0, 1.0], bits):
        y = 1.0 if b > 0 else -1.0
        pts.append((x, y))
    pts.append(goal)
    return pts

def length(path):
    s = 0.0
    for (x1, y1), (x2, y2) in zip(path, path[1:]):
        s += math.hypot(x2 - x1, y2 - y1)
    return s

def topology(path):
    # Sign of the middle waypoint above/below the object center
    signs = tuple(1 if y > 0 else -1 for _, y in path[1:-1])
    # Collapse to coarse contact topology: all above, all below, or mixed
    if all(s > 0 for s in signs):
        return "upper_arc"
    if all(s < 0 for s in signs):
        return "lower_arc"
    return "switching_arc"

def topology_distance(a, b):
    return 0 if a == b else 1

target = "upper_arc"
records = []
for bits in product(alts, repeat=3):
    path = path_from_bits(bits)
    topo = topology(path)
    smooth = length(path)
    topo_penalty = topology_distance(topo, target)
    records.append({
        "bits": bits,
        "topology": topo,
        "length": round(smooth, 4),
        "topology_penalty": topo_penalty,
    })

best_smooth = min(records, key=lambda r: (r["length"], r["topology_penalty"]))
best_topo = min(records, key=lambda r: (r["topology_penalty"], r["length"]))

out = {
    "target_topology": target,
    "records": records,
    "best_smooth": best_smooth,
    "best_topology": best_topo,
    "takeaway": "Equal-smoothness paths can realize different contact topologies, so action smoothness alone cannot identify the desired contact class.",
}

upper = [r for r in records if r["topology"] == "upper_arc"]
lower = [r for r in records if r["topology"] == "lower_arc"]
if upper and lower:
    out["equally_smooth_pair"] = {
        "upper": upper[0],
        "lower": lower[0],
    }

with open(DOCS / "toy_contact_topology_results.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)

print(json.dumps(out, indent=2))
