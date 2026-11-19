#!/usr/bin/env python3
"""Build the gta6-meme-x-01 meme: Vice City sunset scene + make.fun ghost driver.

Composites the official make.fun ghost mark (assets/ghost.png, rendered from
the press kit's mark.svg with the magenta disc removed) into an AI-generated
Vice City street scene (assets/base.webp), adds a neon make.fun billboard,
a make.fun licence plate, and the two-line caption. Output: meme.png.
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1200, 675
FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
MAGENTA = (196, 28, 131)
DARK = (25, 20, 25)


def cover(img, w, h):
    """Resize + centre-crop img to exactly w x h."""
    scale = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)),
                     Image.LANCZOS)
    x = (img.width - w) // 2
    y = (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))


def gradient_band(img, top, height, max_alpha, flip=False):
    """Vertical black gradient for caption legibility."""
    band = Image.new("L", (1, height))
    for i in range(height):
        t = i / max(1, height - 1)
        a = int(max_alpha * (t if flip else 1 - t))
        band.putpixel((0, i), a)
    band = band.resize((img.width, height))
    black = Image.new("RGBA", (img.width, height), (0, 0, 0, 255))
    img.paste(black, (0, top), band)


def main():
    base = Image.open("assets/base.webp").convert("RGB")
    img = cover(base, W, H).convert("RGBA")
    gradient_band(img, 0, 120, 165)            # top caption shade
    gradient_band(img, H - 150, 150, 175, flip=True)  # bottom caption shade
    draw = ImageDraw.Draw(img, "RGBA")

    # --- Neon billboard on the right-hand rooftop: the name in the scene ---
    bx0, by0, bx1, by1 = 838, 122, 1082, 184
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=10,
                           fill=(16, 10, 22, 235), outline=MAGENTA, width=4)
    sign_font = ImageFont.truetype(FONT, 40)
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.text(((bx0 + bx1) / 2, (by0 + by1) / 2), "make.fun",
            font=sign_font, anchor="mm", fill=MAGENTA + (255,))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(7)))
    draw = ImageDraw.Draw(img, "RGBA")
    draw.text(((bx0 + bx1) / 2, (by0 + by1) / 2), "make.fun",
              font=sign_font, anchor="mm", fill=(255, 255, 255, 255))

    # --- Licence plate on the convertible's front bumper ---
    px, py = 516, 508
    draw.rounded_rectangle([px - 68, py - 19, px + 68, py + 19], radius=6,
                           fill=(245, 245, 245, 255), outline=DARK, width=3)
    plate_font = ImageFont.truetype(FONT, 24)
    draw.text((px, py), "make.fun", font=plate_font, anchor="mm",
              fill=DARK + (255,))
    # --- The ghost itself, in the driver's seat, coin in hand ---
    ghost = Image.open("assets/ghost.png").convert("RGBA")
    bbox = ghost.getchannel("A").getbbox()
    ghost = ghost.crop(bbox)
    gh = 300
    gw = round(ghost.width * gh / ghost.height)
    ghost = ghost.resize((gw, gh), Image.LANCZOS)
    gx = round(0.55 * W) - gw // 2
    gy = round(0.635 * H) - gh
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.bitmap((gx + 7, gy + 9), ghost.getchannel("A"), fill=(0, 0, 0, 110))
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(5)))
    img.alpha_composite(ghost, (gx, gy))

    # --- Captions: big, bold, outlined, nothing cut off ---
    draw = ImageDraw.Draw(img, "RGBA")

    def caption(text, y, size):
        font = ImageFont.truetype(FONT, size)
        while draw.textlength(text, font=font) > W - 48 and size > 20:
            size -= 2
            font = ImageFont.truetype(FONT, size)
        draw.text((W / 2, y), text, font=font, anchor="mm",
                  fill=(255, 255, 255, 255), stroke_width=5,
                  stroke_fill=(0, 0, 0, 255))

    caption("WAITED 13 YEARS FOR GTA VI", 46, 60)
    caption("MY AI AGENT ALREADY GOT PAID FOR IT", H - 44, 54)
    img.convert("RGB").save("meme.png")
    print("meme.png written")


if __name__ == "__main__":
    main()
