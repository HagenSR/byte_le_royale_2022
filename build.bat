@echo off
del /q *.pyz

xcopy /s/e/i "game" "wrapper/game"
xcopy /s/e/i "game/util/structures" "wrapper/game/util/structures"
python -m zipapp "wrapper" -o "launcher.pyz" -c
del /q/s "wrapper/game"
del /q/s  "wrapper/game/util/structures"