@echo off
del /q *.pyz

xcopy /s/e/i "game" "wrapper/game"
python -m zipapp "wrapper" -o "launcher.pyz" -c
del /q/s "wrapper/game"