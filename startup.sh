#!/usr/bin/env bash

cd /home/pi/key-mime-pi
. venv/bin/activate
PORT=8000 ./app/main.py