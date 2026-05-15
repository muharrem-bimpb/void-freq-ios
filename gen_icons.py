from PIL import Image, ImageDraw, ImageFilter
import math, os

BG = (4, 8, 15)
CYAN = (0, 238, 255)
PURPLE = (119, 85, 255)

def make_icon(size):
    img = Image.new("RGBA", (size, size), BG + (255,))
    d = ImageDraw.Draw(img)
    cx = cy = size / 2

    # Outer glow ring
    for i in range(6, 0, -1):
        r = size * 0.38 + i * (size * 0.012)
        alpha = int(30 - i * 4)
        overlay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.ellipse([cx - r, cy - r, cx + r, cy + r],
                   outline=CYAN + (alpha,), width=max(1, size // 80))
        img = Image.alpha_composite(img, overlay)

    # FFT bars radiating outward
    bars = 48
    for i in range(bars):
        angle = (i / bars) * math.pi * 2
        heights = [0.08, 0.14, 0.22, 0.11, 0.18, 0.09, 0.25, 0.13,
                   0.07, 0.20, 0.16, 0.10, 0.28, 0.12, 0.08, 0.19,
                   0.24, 0.10, 0.15, 0.21, 0.09, 0.17, 0.13, 0.22,
                   0.08, 0.14, 0.22, 0.11, 0.18, 0.09, 0.25, 0.13,
                   0.07, 0.20, 0.16, 0.10, 0.28, 0.12, 0.08, 0.19,
                   0.24, 0.10, 0.15, 0.21, 0.09, 0.17, 0.13, 0.22]
        h = heights[i % len(heights)] * size * 0.28
        inner_r = size * 0.38
        outer_r = inner_r + h
        x1 = cx + math.cos(angle) * inner_r
        y1 = cy + math.sin(angle) * inner_r
        x2 = cx + math.cos(angle) * outer_r
        y2 = cy + math.sin(angle) * outer_r
        # Color gradient cyan→purple around circle
        t = i / bars
        r = int(CYAN[0] * (1 - t) + PURPLE[0] * t)
        g = int(CYAN[1] * (1 - t) + PURPLE[1] * t)
        b = int(CYAN[2] * (1 - t) + PURPLE[2] * t)
        w = max(1, size // 120)
        overlay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.line([x1, y1, x2, y2], fill=(r, g, b, 220), width=w)
        img = Image.alpha_composite(img, overlay)

    # Inner circle fill
    d = ImageDraw.Draw(img)
    ir = size * 0.34
    d.ellipse([cx - ir, cy - ir, cx + ir, cy + ir], fill=BG + (255,))

    # Inner ring
    d.ellipse([cx - ir, cy - ir, cx + ir, cy + ir],
              outline=CYAN + (180,), width=max(1, size // 100))

    # Center dot
    cr = size * 0.04
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=CYAN + (255,))

    # "VF" text for larger icons
    if size >= 120:
        from PIL import ImageFont
        try:
            font_size = max(8, size // 8)
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        except:
            font = ImageFont.load_default()
        text = "VF"
        bbox = d.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        d.text((cx - tw / 2, cy - th / 2), text, fill=CYAN + (255,), font=font)

    return img.convert("RGB")

sizes = [1024, 180, 120, 167, 152, 76, 80, 60, 58, 40, 29, 20]
out_dir = "/Users/besonnet.kl2/void-freq-ios/icons"
os.makedirs(out_dir, exist_ok=True)

for s in sizes:
    img = make_icon(s)
    path = f"{out_dir}/icon_{s}.png"
    img.save(path, "PNG")
    print(f"✓ {s}x{s} → {path}")

print("\nAll icons generated.")
