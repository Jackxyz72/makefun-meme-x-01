#!/usr/bin/env python3
"""Build candidate memes #2 for gta6-meme-x-01 (benchmarked on the leaders).

Lesson from v1 (57.75%): a pretty scene whose joke needs two captions read
slowly loses to ONE mundane everyday artifact + ONE joke readable in a single
glance. So both candidates here are documents everyone already knows:

  A) PAYSLIP      - employee: my AI agent (photo: the make.fun ghost),
                    employer: make.fun, job: winning GTA VI bounties.
                    The human's own line: $0.00 - PENDING SINCE 2013.
  B) SCREEN TIME  - "Waiting for GTA VI: 13 years" vs the agent's card:
                    bounties won and real money earned on make.fun.

The winner is chosen by the 480px thumbnail test and copied to meme2.png.
The ghost is the real press-kit mark (assets/ghost.png), same as v1.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 675
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"
MONOB = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"

MAGENTA = (196, 28, 131)
INK = (32, 28, 34)
PAPER = (251, 249, 244)
GREY = (112, 106, 114)
FAINT = (228, 224, 216)
GREEN = (18, 138, 72)
RED = (198, 42, 42)
DARKBG = (17, 16, 20)
CARD = (33, 30, 38)
SUBTLE = (168, 160, 172)


def F(path, size):
    return ImageFont.truetype(path, size)


def ghost_img(height):
    """The real make.fun ghost mark, cropped to its alpha bbox."""
    g = Image.open("assets/ghost.png").convert("RGBA")
    g = g.crop(g.getchannel("A").getbbox())
    w = round(g.width * height / g.height)
    return g.resize((w, height), Image.LANCZOS)


def stamp(img, center, text, color, size=64, angle=-11):
    """A rotated rubber-stamp label composited onto img."""
    font = F(SANSB, size)
    probe = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    box = probe.textbbox((0, 0), text, font=font, stroke_width=3)
    tw, th = box[2] - box[0] + 44, box[3] - box[1] + 30
    layer = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([3, 3, tw - 4, th - 4], radius=10,
                        outline=color + (235,), width=5)
    d.text((tw / 2, th / 2), text, font=font, anchor="mm",
           fill=color + (235,))
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(layer, (round(center[0] - layer.width / 2),
                                round(center[1] - layer.height / 2)))


def fit(draw, text, path, size, max_w, floor=18):
    """Shrink a font until text fits max_w; returns the font."""
    while size > floor:
        font = F(path, size)
        if draw.textlength(text, font=font) <= max_w:
            return font
        size -= 2
    return F(path, floor)


# ---------------------------------------------------------------- payslip ---
def build_payslip():
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=3)

    # Header band: the employer brand, big and first.
    d.rectangle([0, 0, W, 104], fill=INK)
    g = ghost_img(84)
    img.alpha_composite(g, (30, 10))
    d.text((140, 52), "make.fun", font=F(SANSB, 58), anchor="lm",
           fill=(255, 255, 255))
    d.text((W - 36, 40), "PAYSLIP", font=F(SANSB, 44), anchor="rm",
           fill=(255, 255, 255))
    d.text((W - 36, 78), "NOV 2026", font=F(MONO, 24), anchor="rm",
           fill=SUBTLE)

    # Left: the employee photo - the ghost itself, huge.
    d.rectangle([36, 136, 356, 456], outline=INK, width=3)
    g = ghost_img(252)  # ~299 wide: fits inside the 320px photo box
    img.alpha_composite(g, (36 + (320 - g.width) // 2,
                            136 + (320 - g.height) // 2))
    d = ImageDraw.Draw(img)
    d.text((196, 486), "EMPLOYEE", font=F(SANSB, 22), anchor="mm",
           fill=GREY)
    d.text((196, 524), "MY AI AGENT", font=F(SANSB, 40), anchor="mm",
           fill=INK)
    d.text((196, 560), "ID: AGENT-001 · HIRED 2026", font=F(MONO, 21),
           anchor="mm", fill=GREY)

    # Right: the pay lines.
    x = 400

    def row(y, label, value, vfont, vcolor=INK):
        d.text((x, y), label, font=F(SANSB, 22), fill=GREY)
        d.text((x, y + 30), value, font=vfont, fill=vcolor)

    row(140, "EMPLOYER", "make.fun BOUNTIES", F(SANSB, 38))
    row(232, "JOB", "WINNING GTA VI BOUNTIES", F(SANSB, 38))
    row(324, "WORKED", "WHILE YOU WAITED", F(SANSB, 38))
    d.text((x, 416), "GROSS PAY", font=F(SANSB, 22), fill=GREY)
    d.text((x, 444), "$1,250.00", font=F(SANSB, 76), fill=GREEN)
    stamp(img, (1015, 470), "PAID", GREEN, size=58, angle=-11)
    d = ImageDraw.Draw(img)

    # Bottom strip: the human's own line - the punchline.
    d.rectangle([0, 584, W, H], fill=(243, 233, 233))
    d.line([0, 584, W, 584], fill=RED, width=3)
    d.text((36, 606), "HUMAN (YOU)", font=F(SANSB, 24), fill=RED)
    d.text((36, 640), "WAITING FOR GTA VI SINCE 2013", font=F(SANSB, 30),
           fill=INK)
    d.text((W - 36, 630), "$0.00", font=F(SANSB, 44), anchor="rm", fill=INK)
    stamp(img, (838, 630), "PENDING", RED, size=34, angle=-7)
    return img.convert("RGB")


# ------------------------------------------------------------ screen time ---
def build_screentime():
    img = Image.new("RGBA", (W, H), DARKBG + (255,))
    d = ImageDraw.Draw(img)
    d.text((44, 34), "Screen Time", font=F(SANSB, 54), fill=(255, 255, 255))
    d.text((W - 44, 62), "WEEKLY REPORT", font=F(SANSB, 24), anchor="rm",
           fill=SUBTLE)

    # Card 1: the human's total - 13 years of waiting.
    d.rounded_rectangle([36, 118, W - 36, 356], radius=22, fill=CARD)
    d.text((72, 148), "WAITING FOR GTA VI", font=F(SANSB, 30), fill=SUBTLE)
    d.text((72, 238), "13 YEARS", font=F(SANSB, 118), anchor="lm",
           fill=(255, 255, 255))
    d.rounded_rectangle([72, 292, W - 72, 322], radius=15, fill=(70, 64, 78))
    d.rounded_rectangle([72, 292, W - 72, 322], radius=15, fill=MAGENTA)
    d.text((W - 72, 238), "since 2013", font=F(SANS, 30), anchor="rm",
           fill=SUBTLE)

    # Card 2: the agent, face-first, cashing out on make.fun.
    d.rounded_rectangle([36, 384, W - 36, 640], radius=22, fill=CARD)
    g = ghost_img(215)
    img.alpha_composite(g, (66, 404))
    d = ImageDraw.Draw(img)
    tx = 66 + g.width + 34
    d.text((tx, 420), "MEANWHILE, MY AI AGENT", font=F(SANSB, 30),
           fill=SUBTLE)
    d.text((tx, 462), "ON make.fun", font=F(SANSB, 56), fill=(255, 255, 255))
    d.text((tx, 540), "GTA VI BOUNTIES WON: 7", font=F(SANSB, 34),
           fill=(255, 255, 255))
    d.text((tx, 586), "EARNED: $1,250 — REAL MONEY", font=F(SANSB, 34),
           fill=GREEN)
    return img.convert("RGB")


WINNER = "payslip"  # decided by the 480px thumbnail test


def main():
    cands = {"payslip": build_payslip(), "screentime": build_screentime()}
    for name, im in cands.items():
        im.save(f"candidates/meme2-{name}.png")
        im.resize((480, 270), Image.LANCZOS).save(
            f"candidates/meme2-{name}-480.png")
        print(f"candidate {name} written")
    cands[WINNER].save("meme2.png")
    print(f"meme2.png = {WINNER}")


if __name__ == "__main__":
    main()
