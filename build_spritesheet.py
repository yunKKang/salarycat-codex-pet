#!/usr/bin/env python3
"""
Generate a Codex TUI pet spritesheet from SalaryCat's cat.GIF.

Output: spritesheet.webp (1536×1872, 8×9 grid of 192×208 frames)
+ pet.json manifest for ~/.codex/pets/salary-cat/

Codex spritesheet spec:
  - Total: 1536 × 1872 px
  - Grid: 8 columns × 9 rows
  - Frame: 192 × 208 px each
  - Format: WebP (or PNG as fallback)

Row → animation mapping:
  Row 0: idle          (6 frames + 2 padding)
  Row 1: running-right (8 frames)
  Row 2: running-left  (8 frames, mirrored)
  Row 3: waving        (4 frames + 4 padding)
  Row 4: jumping       (5 frames + 3 padding)
  Row 5: failed        (8 frames)
  Row 6: waiting       (6 frames + 2 padding)
  Row 7: running       (8 frames)
  Row 8: review        (6 frames + 2 padding)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageSequence

# ── Constants ────────────────────────────────────────────────────────
FRAME_W = 192
FRAME_H = 208
COLS = 8
ROWS = 9
SHEET_W = FRAME_W * COLS   # 1536
SHEET_H = FRAME_H * ROWS   # 1872

# Source GIF — look in project root or parent directories
GIF_CANDIDATES = ["cat.GIF", "cat.gif", "CAT.GIF"]


def find_gif() -> Path:
    """Find the source cat GIF by searching known locations."""
    script_dir = Path(__file__).parent
    search_dirs = [script_dir, script_dir.parent]
    for d in search_dirs:
        for name in GIF_CANDIDATES:
            p = d / name
            if p.exists():
                return p
    print("ERROR: cat.GIF not found. Place it next to this script or in parent dir.", file=sys.stderr)
    sys.exit(1)


def load_gif_frames(path: Path) -> list[Image.Image]:
    """Load all frames from a GIF as RGBA images."""
    img = Image.open(path)
    frames = []
    for f in ImageSequence.Iterator(img):
        frames.append(f.convert("RGBA").copy())
    print(f"Loaded {len(frames)} frames from {path.name}")
    return frames


def fit_frame(src: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """Scale and center a source frame into the target cell, preserving aspect ratio."""
    src_w, src_h = src.size
    scale = min(target_w / src_w, target_h / src_h)
    new_w = int(src_w * scale)
    new_h = int(src_h * scale)

    resized = src.resize((new_w, new_h), Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    offset_x = (target_w - new_w) // 2
    offset_y = (target_h - new_h) // 2
    canvas.alpha_composite(resized, (offset_x, offset_y))
    return canvas


def mirror_h(img: Image.Image) -> Image.Image:
    """Horizontal mirror of an RGBA image."""
    return img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)


def pick_frames(src_frames: list[Image.Image], indices: list[int]) -> list[Image.Image]:
    """Select frames by index, wrapping around if needed."""
    n = len(src_frames)
    return [src_frames[i % n] for i in indices]


def build_row(
    src_frames: list[Image.Image],
    indices: list[int],
    mirror: bool = False,
) -> list[Image.Image]:
    """Build one row of 8 cells from selected source frames."""
    selected = pick_frames(src_frames, indices)
    if mirror:
        selected = [mirror_h(f) for f in selected]

    # Pad to 8 frames by repeating last
    while len(selected) < COLS:
        selected.append(selected[-1])

    return [fit_frame(f, FRAME_W, FRAME_H) for f in selected[:COLS]]


def build_spritesheet(src_frames: list[Image.Image]) -> Image.Image:
    """Build the full 1536×1872 spritesheet."""
    n = len(src_frames)  # 28

    rows_config = [
        # Row 0: idle — 6 frames from the core reaction cycle
        {"name": "idle", "indices": [0, 2, 4, 6, 8, 10], "mirror": False},
        # Row 1: running-right — 8 frames
        {"name": "running-right", "indices": [0, 3, 6, 9, 12, 15, 18, 21], "mirror": False},
        # Row 2: running-left — same frames, mirrored
        {"name": "running-left", "indices": [0, 3, 6, 9, 12, 15, 18, 21], "mirror": True},
        # Row 3: waving — 4 frames (head-tilt moments)
        {"name": "waving", "indices": [6, 7, 8, 5], "mirror": False},
        # Row 4: jumping — 5 frames (peak reaction moments)
        {"name": "jumping", "indices": [0, 7, 14, 21, 6], "mirror": False},
        # Row 5: failed — 8 frames (looking-down moments)
        {"name": "failed", "indices": [0, 1, 2, 3, 0, 1, 2, 3], "mirror": False},
        # Row 6: waiting — 6 frames (slow idle drift)
        {"name": "waiting", "indices": [0, 4, 8, 12, 16, 20], "mirror": False},
        # Row 7: running — 8 frames (faster subset)
        {"name": "running", "indices": [1, 4, 7, 10, 13, 16, 19, 22], "mirror": False},
        # Row 8: review — 6 frames (studying phone)
        {"name": "review", "indices": [2, 5, 8, 11, 14, 17], "mirror": False},
    ]

    sheet = Image.new("RGBA", (SHEET_W, SHEET_H), (0, 0, 0, 0))

    for row_idx, config in enumerate(rows_config):
        cells = build_row(src_frames, config["indices"], config.get("mirror", False))
        for col_idx, cell in enumerate(cells):
            x = col_idx * FRAME_W
            y = row_idx * FRAME_H
            sheet.alpha_composite(cell, (x, y))
        print(f"  Row {row_idx}: {config['name']:15s} ({len(config['indices'])} source frames)")

    return sheet


def build_manifest() -> dict:
    """Build the pet.json manifest."""
    return {
        "id": "salary-cat",
        "displayName": "SalaryCat 月薪喵",
        "description": "The salary cat from SalaryCat — a kawaii cat that lives on your terminal, powered by Codex.",
        "spritesheetPath": "spritesheet.webp",
        "frame": {
            "width": FRAME_W,
            "height": FRAME_H,
            "columns": COLS,
            "rows": ROWS,
        },
        "animations": {
            "idle": {
                "frames": [0, 1, 2, 3, 4, 5],
                "fps": 8.0,
                "loop": True,
            },
            "move_right": {
                "frames": [8, 9, 10, 11, 12, 13, 14, 15],
                "fps": 12.0,
                "loop": True,
            },
            "move_left": {
                "frames": [16, 17, 18, 19, 20, 21, 22, 23],
                "fps": 12.0,
                "loop": True,
            },
            "waving": {
                "frames": [24, 25, 26, 27],
                "fps": 10.0,
                "loop": False,
                "fallback": "idle",
            },
            "jumping": {
                "frames": [32, 33, 34, 35, 36],
                "fps": 10.0,
                "loop": False,
                "fallback": "idle",
            },
            "failed": {
                "frames": [40, 41, 42, 43, 44, 45, 46, 47],
                "fps": 8.0,
                "loop": True,
            },
            "waiting": {
                "frames": [48, 49, 50, 51, 52, 53],
                "fps": 6.0,
                "loop": True,
            },
            "running": {
                "frames": [56, 57, 58, 59, 60, 61, 62, 63],
                "fps": 15.0,
                "loop": True,
            },
            "review": {
                "frames": [64, 65, 66, 67, 68, 69],
                "fps": 8.0,
                "loop": True,
            },
        },
    }


def main():
    print("=" * 60)
    print("SalaryCat → Codex TUI Pet Spritesheet Generator")
    print("=" * 60)

    gif_path = find_gif()
    src_frames = load_gif_frames(gif_path)

    print("\nBuilding spritesheet...")
    sheet = build_spritesheet(src_frames)

    assert sheet.size == (SHEET_W, SHEET_H), \
        f"Size mismatch: {sheet.size} != ({SHEET_W}, {SHEET_H})"

    out_dir = Path(__file__).parent / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    # WebP (preferred)
    webp_path = out_dir / "spritesheet.webp"
    sheet.save(str(webp_path), "WEBP", quality=90, method=6)
    print(f"\n✓ WebP: {webp_path} ({webp_path.stat().st_size / 1024:.1f} KB)")

    # PNG fallback
    png_path = out_dir / "spritesheet.png"
    sheet.save(str(png_path), "PNG")
    print(f"✓ PNG:  {png_path} ({png_path.stat().st_size / 1024:.1f} KB)")

    # Manifest
    manifest = build_manifest()
    manifest_path = out_dir / "pet.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(f"✓ Manifest: {manifest_path}")

    # Deploy instructions
    pet_dir = "~/.codex/pets/salary-cat/"
    print(f"\n{'=' * 60}")
    print("Deploy to Codex:")
    print(f"  mkdir -p {pet_dir}")
    print(f"  cp output/spritesheet.webp {pet_dir}")
    print(f"  cp output/pet.json {pet_dir}")
    print(f"\nThen in Codex CLI: /pets → select 'SalaryCat 月薪喵'")


if __name__ == "__main__":
    main()
