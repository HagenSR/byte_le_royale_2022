#!/bin/sh

rm *.pyz; 

cp -rf game wrapper/
python3 -m zipapp wrapper -c -p "/usr/bin/env python3" -o launcher.pyz; 
rm -rf wrapper/game
