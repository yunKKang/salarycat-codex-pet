#!/bin/bash
# Deploy SalaryCat pet to Codex CLI (macOS / Linux)
# Run from the codex-pet/ directory

PET_DIR="$HOME/.codex/pets/salary-cat"

echo "Creating $PET_DIR ..."
mkdir -p "$PET_DIR"

echo "Copying spritesheet.webp ..."
cp -f output/spritesheet.webp "$PET_DIR/spritesheet.webp"

echo "Copying pet.json ..."
cp -f output/pet.json "$PET_DIR/pet.json"

echo ""
echo "Done! SalaryCat is installed at $PET_DIR"
echo ""
echo "In Codex CLI, run: /pets"
echo "Then select \"SalaryCat 月薪喵\""
