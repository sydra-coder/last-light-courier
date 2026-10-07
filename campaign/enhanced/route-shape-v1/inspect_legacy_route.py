"""Print a compact map with the archived route for one legacy level."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
level = int(sys.argv[1]) if len(sys.argv) > 1 else 932
if not 1 <= level <= 1000:
    raise SystemExit("Expected a level from 1 to 1000")
record = json.loads((ROOT / "design/map-solutions-1000.json").read_text(encoding="utf-8"))["levels"][level - 1]
game_map = record["map"]
route = [tuple(state["p"]) for state in record["solutions"][0]["route"]]
size = game_map["grid"]
canvas = [["." for _ in range(size)] for _ in range(size)]
for wall in game_map["walls"]:
    x, y = map(int, wall.split(","))
    canvas[y][x] = "#"
for x, y in route:
    canvas[y][x] = "*"
for house in game_map["homes"]:
    x, y = house["p"]
    canvas[y][x] = "H"
x, y = game_map["depot"]
canvas[y][x] = "D"
print(f"Level {level}: {size}x{size}, {len(game_map['homes'])} houses, {len(route)-1} recorded steps")
print("D depot, H house, * recorded route, # wall, . open road")
for y, row in enumerate(canvas):
    print(f"{y:02d} " + "".join(row))
