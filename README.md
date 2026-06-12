# codex-salary-cat

SalaryCat (月薪喵) pet for OpenAI Codex CLI.

It is adapted from [SalaryCat](https://github.com/Einswen/SalaryCat) into the Codex TUI pet spritesheet format. This build uses a smoother Windows-friendly idle loop and PNG as the default spritesheet.

## Install

Copy the generated pet files into your Codex pets directory:

```powershell
mkdir ~/.codex/pets/salary-cat
cp output/spritesheet.png ~/.codex/pets/salary-cat/
cp output/pet.json ~/.codex/pets/salary-cat/
```

Then run `/pets` in Codex and select `SalaryCat 月薪喵`.

On Windows, you can also run:

```powershell
.\deploy.bat
```

## Build

```bash
pip install Pillow
python build_spritesheet.py
```

The build writes:

- `output/spritesheet.png`
- `output/spritesheet.webp`
- `output/pet.json`

## Notes

- Frame grid: `8 x 9`
- Frame size: `192 x 208`
- Default idle animation: extended ping-pong loop using extra unused cells
- Windows Terminal uses Sixel; Kitty-compatible terminals use Kitty graphics

## License

- This project: MIT
- Original SalaryCat: Apache 2.0
- Cat art: from the original SalaryCat project
