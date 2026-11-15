# usage: python crop.py grid.png outDir name1 name2 name3 name4   ("-" skips a panel)
import sys, os
from PIL import Image, ImageChops
g, out, names = sys.argv[1], sys.argv[2], sys.argv[3:]
im = Image.open(g).convert("RGB"); W, H = im.size
os.makedirs(out, exist_ok=True)
px = im.load()
def white_col(x): return sum(1 for y in range(0, H, 4) if min(px[x, y]) > 235)
def white_row(y): return sum(1 for x in range(0, W, 4) if min(px[x, y]) > 235)
cx = max(range(int(W*.4), int(W*.6)), key=white_col)
cy = max(range(int(H*.4), int(H*.6)), key=white_row)
boxes = [(0, 0, cx, cy), (cx, 0, W, cy), (0, cy, cx, H), (cx, cy, W, H)]
for n, b in zip(names, boxes):
    if n == "-": continue
    p = im.crop((b[0] + 8, b[1] + 8, b[2] - 8, b[3] - 8))
    diff = ImageChops.difference(p, Image.new("RGB", p.size, (255, 255, 255))).convert("L").point(lambda v: 255 if v > 30 else 0)
    bb = diff.getbbox() or (0, 0) + p.size
    p = p.crop(bb)
    s = max(p.size) + 24
    sq = Image.new("RGB", (s, s), (255, 255, 255)); sq.paste(p, ((s - p.size[0]) // 2, (s - p.size[1]) // 2))
    sq.resize((400, 400), Image.LANCZOS).save(os.path.join(out, n + ".jpg"), quality=84)
    print(n, os.path.getsize(os.path.join(out, n + ".jpg")))
