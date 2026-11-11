import sys
sys.path.insert(0, '.')
import motion as M
from PIL import Image
ep = M.load(sys.argv[1]); out = sys.argv[2]; mode = sys.argv[3] if len(sys.argv) > 3 else "h"
W, H = (1920, 1080) if mode == "h" else (1080, 1920)
scs = ep.SCENES + ([ep.END] if getattr(ep, "END", None) else [])
tw, th = (480, 270) if mode == "h" else (270, 480)
cols = 6 if mode == "h" else 6
rows = (len(scs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * tw, rows * th))
for i, sc in enumerate(scs):
    st = lambda at: at * 4.0
    nsteps = (sc["ids"][1] - sc["ids"][0] + 1) if "ids" in sc else 1
    im, _ = M.frame(sc, W, H, nsteps * 4.0 + 4, st)
    sheet.paste(im.resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
sheet.save(out); print(len(scs))
