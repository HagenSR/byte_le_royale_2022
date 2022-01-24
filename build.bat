@echo off
del /q *.pyz

xcopy /s/e/i "game" "wrapper/game"
mkdir "./wrapper/server/"
mkdir "./wrapper/server/certs/"
xcopy /s/e/i "./server/client" "./wrapper/server/client"
xcopy /s/e/i "./server/certs/cert.pem" "./wrapper/server/certs/cert.pem"
python -m zipapp "wrapper" -o "launcher.pyz" -c
del /q/s "wrapper/game"
del /q/s "wrapper/server/client"
del /q/s "wrapper/server/certs"
del /q/s "wrapper/server"