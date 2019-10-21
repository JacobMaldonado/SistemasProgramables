"""
INSTALACIÓN DE ADAFRUIT DHT11
sudo apt-get update
sudo apt-get install build-essential python-dev
git clone https://github.com/
"""

import Adafruit_DHT
sensor = Adafruit_DHT.DHT11
gpio= 2
while True:
    humidity, temperature = Adafruit_DHT.read