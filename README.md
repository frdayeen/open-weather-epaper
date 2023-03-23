# open-weather-epaper
Weather dashboard using inky impression 7color epaper display. 


 Most of the weather forcast project uses API from Openweather map. But recently openweather map limited their One call 3.0 API for free use. Open meteo on the other hand is an open source weather API and free for non commercial uses and requires no registration. 


This project was inspired from [this](https://github.com/kotamorishi/weather-impression) and [this](https://github.com/axwax/Open-Meteo-Inky-Pack) projects.  The icons used in this project were downloaded from flaticons and fonts from Google fonts but feel free to use your own.

![eink weather dashboard](/assets/epaper-inky-weather-dashboard.jpeg)


## Requirements
- Raspberry pi (I used raspberry pi zero w but any raspberry pi will work).
- [Inky impression 5.7" 7 color display](https://shop.pimoroni.com/en-us/products/inky-impression-5-7).
- MicroSD card.
- 4x5 Picture frame (optional).

## Instruction

1. Download and install Raspberry Pi OS.
2. Install [Pyenv](https://github.com/pyenv/pyenv) or any other python virtual environment and activate it. Raspberry pi OS comes with python, so using a virtual python environment would be useful incase something messed up.
3. Install necessary [packages](https://github.com/pimoroni/inky) for Inky impression.
4. Clone the project files. Edit weather_new.py and update *static root*
```
#change your root folder
static_root = '/home/path-to-project/open-weather'
```
Then change your lat (latitude) and lon (longitude)* according to where you are. You may also check [documentation](https://open-meteo.com/en/docs) and modify other parameters in the function.

```
    def __init__(self):
        #grab latitute and longitude for your area
        lat = 52.52
        lon = 31.85
        daily_Para = 'weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability_max'
        hourly_para = 'apparent_temperature,precipitation_probability'
        curr_weather_bool = 'true'
        tz = 'Your Timezone'
```

then run it.
5. To update the weather data periodically, go to your terminal and add a cronjob by typing
```
crontab -e
```
Add the line at the bottom of the file- 
```
0 * * * * /path-to-your-python/environment /path-to/open-weather/weather_new.py
```
This will run the file every hour.
6. Enjoy your new weather dashboard.


