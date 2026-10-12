"""Record transparent seams between five adjacent costume concepts.

This writes crop coordinates only. It leaves the source artwork untouched.
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "design" / "character-variants" / "holiday-wardrobe"
TARGET = Path(__file__).with_name("wardrobe-seams.js")
STEP = 10


def seam(alpha, boundary):
    height, width = alpha.shape
    center = round(width * boundary / 5)
    reach = max(85, round(width / 5 * .2))
    rows = list(range(0, height, STEP))
    if rows[-1] != height - 1:
        rows.append(height - 1)
    values = []
    for y in rows:
        left, right = max(0, center - reach), min(width, center + reach)
        clear = alpha[y, left:right] < 16
        padded = np.concatenate(([False], clear, [False]))
        starts = np.flatnonzero(np.diff(padded.astype(np.int8)) == 1)
        ends = np.flatnonzero(np.diff(padded.astype(np.int8)) == -1)
        runs = [(left + int(start), left + int(end) - 1) for start, end in zip(starts, ends) if end - start >= 3]
        if not runs:
            values.append(None)
            continue
        best = max(runs, key=lambda run: (run[1] - run[0] + 1) * 2 - abs((run[0] + run[1]) / 2 - center))
        values.append(round((best[0] + best[1]) / 2))
    known = [(i, value) for i, value in enumerate(values) if value is not None]
    if not known:
        return [center] * len(rows)
    for i, value in enumerate(values):
        if value is not None:
            continue
        before = max((point for point in known if point[0] < i), default=known[0])
        after = min((point for point in known if point[0] > i), default=known[-1])
        values[i] = round(before[1] + (after[1] - before[1]) * (i - before[0]) / max(1, after[0] - before[0]))
    return values


entries = [None]
for file in sorted(SOURCE.glob("*-five-looks.png")):
    image = np.asarray(Image.open(file).convert("RGBA"))
    height, width, _ = image.shape
    entries.append({"width": width, "height": height, "step": STEP, "edges": [seam(image[:, :, 3], boundary) for boundary in range(1, 5)]})
if len(entries) != 18:
    raise RuntimeError(f"Expected 17 five-look sheets, found {len(entries) - 1}")
TARGET.write_text("window.LLC_WARDROBE_SEAMS=" + json.dumps(entries, separators=(",", ":")) + ";\n", encoding="utf-8")
print(f"Wrote crop seams for {len(entries) - 1} sheets to {TARGET}")
