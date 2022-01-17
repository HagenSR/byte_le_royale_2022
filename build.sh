set echo off
rm -f *.pyz
cp -r ./game ./wrapper/game
mkdir ./wrapper/server/
mkdir ./wrapper/server/certs/
cp -r  ./server/client ./wrapper/server/client
cp  ./server/certs/cert.pem ./wrapper/server/certs/cert.pem
python3 -m zipapp  ./wrapper -o ./launcher.pyz -c
rm -rf ./wrapper/game
rm -rf ./wrapper/server/client
rm -rf ./wrapper/server/certs
rm -rf ./wrapper/server
