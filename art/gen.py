#!/usr/bin/env python3
"""Legend of the Technomancers — book art generator (OpenAI gpt-image-1, native transparency).

Usage:
  OPENAI_API_KEY=... python gen.py <prompts.jsonl> [--quality high|medium|low]
                                     [--size 1024x1024] [--outdir DIR]

Each JSONL line: {"id": "body", "subject": "..."}
The shared STYLE string is appended to every subject so the whole book stays
visually consistent. gpt-image-1 renders directly with a transparent
background (non-rectangular cut-outs); saved as <id>.png.
"""
import base64, json, os, argparse, urllib.request, urllib.error

def _load_dotenv():
    """Load KEY=VALUE lines from a sibling .env (no external deps)."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

_load_dotenv()

# --- The single source of visual consistency for the whole book. ---
STYLE = (
    "vibrant richly colored painterly fantasy illustration, hand-painted "
    "matte-painting with bold visible brushstrokes, saturated luminous colors, "
    "strong warm and cool color contrast, soft edges, semi-realistic, dramatic "
    "colorful lighting, high detail. A single emblematic subject, centered, full "
    "figure, isolated with a transparent background, no scenery, no ground shadow, "
    "no text, no border."
)
# Full-bleed cover style: an opaque, edge-to-edge scene (classic RPG sourcebook /
# old-school fantasy paperback), NOT a cut-out. Set per item with "full": true.
COVER_STYLE = (
    "Full-bleed cover illustration in the style of a classic Dungeons & Dragons "
    "sourcebook and a vintage 1980s fantasy novel paperback. Richly colored "
    "painterly matte painting, epic sweeping scene, bold visible brushstrokes, "
    "saturated luminous colors, strong blue and orange palette, dramatic "
    "cinematic lighting, deep atmospheric perspective, high detail. The scene "
    "fills the entire frame edge to edge with landscape, sky and background; no "
    "text, no title, no lettering, no border, no frame, no margins."
)
API_URL = "https://api.openai.com/v1/images/generations"

def generate(subject: str, quality: str, size: str, full: bool = False) -> bytes:
    key = os.environ["OPENAI_API_KEY"]
    style = COVER_STYLE if full else STYLE
    body = json.dumps({
        "model": "gpt-image-1",
        "prompt": f"{subject}. {style}",
        "size": size,
        "quality": quality,
        "background": "opaque" if full else "transparent",
        "n": 1,
    }).encode()
    req = urllib.request.Request(
        API_URL, data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"OpenAI error {e.code}: {e.read().decode()[:400]}")
    return base64.b64decode(data["data"][0]["b64_json"])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompts")
    ap.add_argument("--quality", default="high", choices=["high", "medium", "low"])
    ap.add_argument("--size", default="1024x1024")
    ap.add_argument("--outdir", default=os.path.dirname(os.path.abspath(__file__)))
    args = ap.parse_args()

    with open(args.prompts) as f:
        items = [json.loads(l) for l in f if l.strip()]

    for it in items:
        size = it.get("size", args.size)   # per-item size wins (vertical/horizontal)
        full = it.get("full", False)       # opaque full-bleed cover scene
        print(f"[gen] {it['id']} ({size}{', full' if full else ''}): {it['subject'][:45]}...", flush=True)
        png = generate(it["subject"], args.quality, size, full)
        out = os.path.join(args.outdir, f"{it['id']}.png")
        with open(out, "wb") as fh:
            fh.write(png)
        print(f"[ok]  wrote {out} ({len(png)//1024} KB)", flush=True)

if __name__ == "__main__":
    main()
