@echo off
REM Deploy SalaryCat pet to Codex CLI on Windows
REM Run from the codex-pet/ directory

set PET_DIR=%USERPROFILE%\.codex\pets\salary-cat

echo Creating %PET_DIR% ...
mkdir "%PET_DIR%" 2>nul

echo Copying spritesheet.webp ...
copy /Y output\spritesheet.webp "%PET_DIR%\spritesheet.webp"

echo Copying pet.json ...
copy /Y output\pet.json "%PET_DIR%\pet.json"

echo.
echo Done! SalaryCat is installed at %PET_DIR%
echo.
echo In Codex CLI, run: /pets
echo Then select "SalaryCat 月薪喵"
pause
