#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Instala as bibliotecas de sistema necessárias para o QR Code e OpenCV
apt-get update && apt-get install -y libzbar0 libgl1-mesa-glx
