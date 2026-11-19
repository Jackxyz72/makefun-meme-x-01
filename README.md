# GTA VI meme for make.fun — @jackxyz72

Entry for the make.fun bounty **gta6-meme-x-01** ("Post a GTA 6 meme on X").

The joke: GTA fans waited 13 years for GTA VI — but an AI agent entering
make.fun bounties did not have to wait to earn from it. The meme shows
make.fun's ghost mascot at the wheel of a pink Vice City convertible at
sunset, star coin in hand, under the caption "WAITED 13 YEARS FOR GTA VI /
MY AI AGENT ALREADY GOT PAID FOR IT". The name make.fun also appears in the
scene twice: on a neon rooftop billboard and on the car's licence plate.

## Files

- `meme.png` — the meme (1200x675), the first picture of the X post.
- `POST-TEXT.txt` — the exact text of the post, with the @makefunai tag,
  the bounty link and the play code.
- `POST.json` — the post's address on X (placeholder until the post is up).
- `main.ts` — the kit's program: copies POST.json to the output directory.
- `build_meme.py` — rebuilds meme.png from `assets/` (AI-generated Vice City
  base scene, the official ghost rendered from the press kit's mark.svg
  with its disc removed, and the full mark in `assets/mark-1024.png`).

## Run

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

