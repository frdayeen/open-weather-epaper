# open-weather-epaper
Weather dashboard using inky impression 7color epaper display. 
This project was inspired from [this](https://github.com/kotamorishi/weather-impression) and [this](https://github.com/axwax/Open-Meteo-Inky-Pack) projects. The icons were downloaded from flaticons and fonts from Google fonts but feel free to use your own.

## Requirements
- Raspberry pi (I used raspberry pi zero w but any raspberry pi will work).
- [Inky impression 5.7" 7 color display](https://shop.pimoroni.com/en-us/products/inky-impression-5-7).
- MicroSD card.
- 4x5 Picture frame (optional).

## Instruction

1. Download and install Raspberry Pi OS.
2. Install [Pyenv](https://github.com/pyenv/pyenv) or any other python virtual environment and activate it. Raspberry pi OS comes with python, so using a virtual python environment would be useful incase something messed up.
3. Install necessary [packages](https://github.com/pimoroni/inky) for Inky impression.
4. Clone the package files. Edit weather_new.py and update static root, lat (latitude) and lon (longitude), then run it.
5. To update the weather data periodically, go to your terminal and add a cronjob by typing
```
crontab -e
```
To run the file every hour add a line at the bottom of the file
```
0 * * * * /path-to-your-python/environment /path-to/open-weather/weather_new.py
```
6. Enjoy your new weather dashboard.


