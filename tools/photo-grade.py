"""HD Events house photo style: consistent, 'shot by a photographer' grade for every website photo.

Steps: neutral white balance -> exposure normalised to a target -> filmic S-curve with lifted blacks
-> cool-teal shadows / clean warm highlights (matches the cyan/purple brand) -> vibrance -> local
clarity -> soft vignette -> sharpen -> crop to a standard ratio -> resize & compress for the web.

Usage: python3 grade.py SRC OUT [--ratio 16:9|3:2|4:3|1:1|4:5|none] [--width 2000]
                         [--crop x0,y0,x1,y1] [--focus 0.5,0.5] [--exposure +0.1] [--wb 0..1]
"""
import argparse
import numpy as np
from PIL import Image, ImageFilter, ImageOps

p = argparse.ArgumentParser()
p.add_argument('src'); p.add_argument('out')
p.add_argument('--ratio', default='none')
p.add_argument('--width', type=int, default=2000)
p.add_argument('--crop', default=None, help='manual crop x0,y0,x1,y1 in source pixels (before ratio crop)')
p.add_argument('--focus', default='0.5,0.5', help='where to keep when cropping to the ratio')
p.add_argument('--exposure', type=float, default=0.0, help='extra exposure in stops')
p.add_argument('--wb', type=float, default=0.6, help='white-balance correction strength 0..1')
p.add_argument('--target', type=float, default=0.42, help='target mid-tone brightness 0..1')
a = p.parse_args()

im = ImageOps.exif_transpose(Image.open(a.src)).convert('RGB')
if a.crop:
    im = im.crop(tuple(int(v) for v in a.crop.split(',')))

# Crop to a standard ratio around the focus point.
if a.ratio != 'none':
    rw, rh = (float(v) for v in a.ratio.split(':'))
    fx, fy = (float(v) for v in a.focus.split(','))
    W, H = im.size
    if W / H > rw / rh:
        nw = round(H * rw / rh); x0 = min(max(0, round(fx * W - nw / 2)), W - nw); im = im.crop((x0, 0, x0 + nw, H))
    else:
        nh = round(W * rh / rw); y0 = min(max(0, round(fy * H - nh / 2)), H - nh); im = im.crop((0, y0, W, y0 + nh))
if im.width > a.width:
    im = im.resize((a.width, round(im.height * a.width / im.width)), Image.LANCZOS)

x = np.asarray(im).astype(np.float32) / 255.0
lin = x ** 2.2

# 1. Neutral white balance (grey-world on mid-tones, partially applied so stage colour survives).
lum = lin @ np.array([.2126, .7152, .0722], np.float32)
mask = (lum > .02) & (lum < .6)
if mask.sum() > 1000:
    means = lin[mask].mean(axis=0)
    gains = means.mean() / np.maximum(means, 1e-4)
    gains = 1 + (gains - 1) * a.wb
    lin = lin * gains
# 2. Exposure: bring the median brightness towards a common target, within limits.
lum = lin @ np.array([.2126, .7152, .0722], np.float32)
med = float(np.median(lum)) ** (1 / 2.2)
stops = np.clip(np.log2(max(a.target, 1e-3) / max(med, 1e-3)) * 1.3, -0.7, 1.3) + a.exposure
lin = lin * (2 ** stops)
x = np.clip(lin, 0, None) ** (1 / 2.2)
# Highlight roll-off so brightened lights don't clip harshly.
x = np.where(x > .8, .8 + (1 - np.exp(-(x - .8) / .2)) * .2, x)

# 3. Filmic S-curve with lifted blacks and soft whites.
def curve(v):
    s = v * v * (3 - 2 * v)              # smoothstep contrast
    v = v * .55 + s * .45
    return .035 + v * (.975 - .035)       # lifted black point, soft white point
x = curve(np.clip(x, 0, 1))

# 4. Split tone: cool teal in the shadows, clean slightly warm highlights.
lum = x @ np.array([.2126, .7152, .0722], np.float32)
sh = np.clip(1 - lum / .45, 0, 1)[..., None] ** 1.5
hi = np.clip((lum - .6) / .4, 0, 1)[..., None]
x = x + sh * np.array([-.012, .012, .03], np.float32) + hi * np.array([.012, .005, -.008], np.float32)

# 5. Vibrance: lift muted colours more than already-saturated ones.
mean = x.mean(axis=2, keepdims=True)
sat = x.max(axis=2, keepdims=True) - x.min(axis=2, keepdims=True)
x = mean + (x - mean) * (1 + .28 * (1 - np.clip(sat * 2, 0, 1)))

x = np.clip(x, 0, 1)
im = Image.fromarray((x * 255 + .5).astype(np.uint8))
# Brightened low-light shots get gentle noise reduction so grain doesn't show.
if stops > .6:
    im = Image.blend(im, im.filter(ImageFilter.MedianFilter(3)), min(.8, (stops - .6) * 1.2))

# 6. Clarity (large-radius local contrast) and a soft vignette.
im = im.filter(ImageFilter.UnsharpMask(radius=max(20, im.width // 60), percent=8, threshold=4))
W, H = im.size
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
vig = 1 - .22 * np.clip((d - .55) / .85, 0, 1) ** 1.6
x = np.asarray(im).astype(np.float32) * vig[..., None]
im = Image.fromarray(np.clip(x, 0, 255).astype(np.uint8))

# 7. Output sharpening for the web, then save.
im = im.filter(ImageFilter.UnsharpMask(radius=1.0, percent=55, threshold=4))
im.save(a.out, 'JPEG', quality=82, optimize=True, progressive=True, subsampling='4:2:0')
print(f'{a.out}: {im.size[0]}x{im.size[1]}, exposure {stops:+.2f} stops')
