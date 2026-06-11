# codex-salary-cat

SalaryCat (月薪喵) — a custom pet for [OpenAI Codex CLI](https://github.com/openai/codex).

Based on the [SalaryCat](https://github.com/Einswen/SalaryCat) terminal animation, adapted to the Codex TUI pet spritesheet format.

## Preview

A kawaii cat that sits in your terminal, reacting to your coding sessions with 9 animation states.

## Animation States

| Animation | Trigger | FPS |
|-----------|---------|-----|
| idle | Default — cat looking at its phone | 8 |
| running-right | Moving right | 12 |
| running-left | Moving left (mirrored) | 12 |
| waving | Greeting | 10 |
| jumping | Excitement | 10 |
| failed | Error / blocked | 8 |
| waiting | Awaiting input | 6 |
| running | Active work | 15 |
| review | Code review / ready | 8 |

## Quick Install

### macOS / Linux

```bash
# Create pet directory
mkdir -p ~/.codex/pets/salary-cat/

# Copy files
cp output/spritesheet.webp ~/.codex/pets/salary-cat/
cp output/pet.json ~/.codex/pets/salary-cat/
```

Or run the deploy script:

```bash
chmod +x deploy.sh
./deploy.sh
```

### Windows

```powershell
# Create pet directory
mkdir -p ~/.codex/pets/salary-cat/

# Copy files
cp output/spritesheet.webp ~/.codex/pets/salary-cat/
cp output/pet.json ~/.codex/pets/salary-cat/
```

Or double-click `deploy.bat`.

### Then in Codex CLI

```
/pets
```

Select **SalaryCat 月薪喵**.

## Terminal Compatibility

| Terminal | Protocol | Status |
|----------|----------|--------|
| Windows Terminal | Sixel | ✅ Supported |
| iTerm2 (≥ 3.6) | Kitty | ✅ Supported |
| Kitty | Kitty | ✅ Supported |
| Ghostty | Kitty | ✅ Supported |
| WezTerm | Kitty | ✅ Supported |
| foot | Sixel | ✅ Supported |
| tmux | — | ❌ Disabled (image corruption) |
| Zellij | — | ❌ Disabled (pane-locality issues) |

## Build from Source

Requirements: Python 3.8+, [Pillow](https://pypi.org/project/Pillow/)

```bash
pip install Pillow
python build_spritesheet.py
```

Output goes to `output/`:

- `spritesheet.webp` — primary spritesheet (329 KB)
- `spritesheet.png` — PNG fallback (845 KB)
- `pet.json` — Codex pet manifest

## Spritesheet Format

Follows the [Codex TUI pet specification](https://github.com/openai/codex/tree/main/codex-rs/tui/src/pets):

| Property | Value |
|----------|-------|
| Total size | 1536 × 1872 px |
| Grid | 8 columns × 9 rows |
| Frame size | 192 × 208 px |
| Format | WebP (PNG fallback) |
| Total frames | 72 |

## Project Structure

```
codex-pet/
├── cat.GIF                # Source animation (from SalaryCat)
├── build_spritesheet.py   # Spritesheet generator
├── deploy.sh              # macOS / Linux deploy script
├── deploy.bat             # Windows deploy script
├── README.md
└── output/
    ├── spritesheet.webp   # 1536×1872 WebP
    ├── spritesheet.png    # 1536×1872 PNG fallback
    └── pet.json           # Codex pet manifest
```

## License

- **This project**: MIT
- **Original SalaryCat**: [Apache 2.0](https://github.com/Einswen/SalaryCat/blob/main/LICENSE)
- **Cat art**: From the SalaryCat project
