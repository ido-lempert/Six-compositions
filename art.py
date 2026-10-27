"""Six seeded generative compositions, written as SVG. No dependencies. Run: python3 art.py"""
import math, random, os
W = H = 600
def svg(body, bg): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="{bg}"/>{body}</svg>'
def hsl(h, s, l): return f"hsl({h % 360:.0f},{s}%,{l}%)"

def rings(r):
    out = []
    for i in range(40):
        rad = 10 + i * 7; hue = 200 + i * 3
        out.append(f'<circle cx="{W/2 + math.sin(i*.4+r.random())*18:.1f}" cy="{H/2 + math.cos(i*.3)*18:.1f}" r="{rad}" fill="none" stroke="{hsl(hue,60,60)}" stroke-width="2" opacity=".8"/>')
    return svg("".join(out), "#0d1b2a")

def grid(r):
    out = []; n = 12; s = W / n
    for y in range(n):
        for x in range(n):
            if r.random() < .5: out.append(f'<line x1="{x*s}" y1="{y*s}" x2="{(x+1)*s}" y2="{(y+1)*s}" stroke="#222" stroke-width="4"/>')
            else: out.append(f'<line x1="{(x+1)*s}" y1="{y*s}" x2="{x*s}" y2="{(y+1)*s}" stroke="#222" stroke-width="4"/>')
    return svg("".join(out), "#f4efe6")

def spiral(r):
    pts = []; a = 0; rad = 2
    for i in range(900):
        a += .35; rad += .31
        x = W/2 + math.cos(a) * rad; y = H/2 + math.sin(a) * rad
        pts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{1+ i/220:.1f}" fill="{hsl(20+i/4,70,60)}"/>')
    return svg("".join(pts), "#1b1b1b")

def waves(r):
    out = []
    for k in range(26):
        ph = r.random() * 6.28; amp = 10 + k * 1.6
        d = "M0," + str(40 + k * 20) + " " + " ".join(f"L{x},{40 + k*20 + math.sin(x/38 + ph) * amp:.1f}" for x in range(0, W + 1, 10))
        out.append(f'<path d="{d}" fill="none" stroke="{hsl(160+k*4,50,35+k)}" stroke-width="2"/>')
    return svg("".join(out), "#f2f7f5")

def blocks(r):
    out = []
    def split(x, y, w, h, d):
        if d == 0 or w < 50 or h < 50:
            out.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{hsl(r.choice([10,45,210,0]),65,r.randint(40,75))}" stroke="#111" stroke-width="3"/>'); return
        if w > h:
            c = w * r.uniform(.3, .7); split(x, y, c, h, d-1); split(x+c, y, w-c, h, d-1)
        else:
            c = h * r.uniform(.3, .7); split(x, y, w, c, d-1); split(x, y+c, w, h-c, d-1)
    split(0, 0, W, H, 5); return svg("".join(out), "#fff")

def stars(r):
    out = []
    for i in range(160):
        x, y = r.random()*W, r.random()*H; d = math.hypot(x-W/2, y-H/2)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{max(.6, 4 - d/90):.1f}" fill="{hsl(50 + d/6, 80, 75)}" opacity="{max(.25, 1 - d/420):.2f}"/>')
    return svg("".join(out), "#090c1a")

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    for i, f in enumerate([rings, grid, spiral, waves, blocks, stars], 1):
        open(f"out/{i:02d}-{f.__name__}.svg", "w").write(f(random.Random(i)))
    print("wrote 6 files to out/")
