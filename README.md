# dishwasher-lights

## neopixel library
[rpi_ws281x](https://github.com/jgarff/rpi_ws281x)
install by following [this](https://learn.adafruit.com/neopixels-on-raspberry-pi/software)

## AWS IoT instructions
```bash
pip install -r requirements.txt
```
```bash
python basicPubSub.py -e a1pvj7wfkdfs64.iot.ap-southeast-2.amazonaws.com -r root-CA.crt -c macos.cert.pem -k macos.private.key
```