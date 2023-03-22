#!/usr/bin/env python3
# Weather display using open-meteo API by F.R. Dayeen


import gpiod
import datetime 
import requests
from enum import Enum



from PIL import Image, ImageDraw, ImageFont, ImageFilter
from inky.inky_uc8159 import Inky

saturation = 0.9
canvasSize = (600, 448)

#change your root folder
static_root = '/home/dayeen/epaper/open-weather'
img_folder = static_root + '/weather_jpg/'

weather_Codes = {
    0: 'Clear sky',
    1: 'Mostly clear',
    2: 'Partly cloudy',
    3: 'Cloudy',
    45: 'Fog and depositing rime',
    48: 'Fog',
    51: 'Light drizzle',
    53: 'Moderate drizzle',
    55: 'Dense drizzle',
    56: 'Light freezing drizzle',
    57: 'Dense freezing drizzle',
    61: 'Slight rain',
    63: 'Moderate rain',
    65: 'Heavy rain',
    66: 'Light freezing rain',
    67: 'Heavy freezing rain',
    71: 'Slight snow',
    73: 'Moderate snow',
    75: 'Heavy snow',
    77: 'Snow grains',
    80: 'Slight rain showers',
    81: 'Moderate rain showers',
    82: 'Violent rain showers',
    85: 'Slight snow showers',
    86: 'Heavy snow showers',
    95: 'Thunderstorm',
    96: 'Thunderstorm with slight hail',
    99: 'Thunderstorm with heavy hail'
}

weather_Icons = {
    0: 'clear',
    1: 'mostlyclear',
    2: 'mostlyclear',
    3: 'cloudy',
    45: 'fog',
    48: 'fog',
    51: 'drizzle',
    53: 'drizzle',
    55: 'drizzle',
    56: 'drizzle',
    57: 'drizzle',
    61: 'rain',
    63: 'rain',
    65: 'rain',
    66: 'snow',
    67: 'snow',
    71: 'snow',
    73: 'snow',
    75: 'snow',
    77: 'snow',
    80: 'rain',
    81: 'rain',
    82: 'rain',
    85: 'snow',
    86: 'snow',
    95: 'thunderstorm',
    96: 'thunderstorm',
    99: 'thunderstorm'

}  

class weather_Info(object):
    def __init__(self):
        #grab latitute and longitude for your area
        lat = 41.85
        lon = -87.65
        daily_Para = 'weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability_max'
        hourly_para = 'apparent_temperature,precipitation_probability'
        curr_weather_bool = 'true'
        tz = 'America%2FChicago'

        forecast_api = 'https://api.open-meteo.com/v1/forecast?latitude=' + str(lat) +'&longitude=' + str(lon) + '&hourly=' + hourly_para + '&daily=' + daily_Para + '&current_weather=' + curr_weather_bool + '&timezone=' + tz
        self.jsonFile = requests.get(forecast_api).json()


def cordianl_Direction(deg):
    arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    val=int((deg/22.5)+.5)
    return arr[(val % 16)]

#fonts
class fonts(Enum):
    light =  static_root + "/fonts/PTSerif-Regular.ttf"
    normal = static_root + "/fonts/PTSerif-Bold.ttf"

def display_Fonts(type, fontsize=12):
    return ImageFont.truetype(type.value, fontsize)



def weather_Display(winfo, canvas):   
    draw = ImageDraw.Draw(canvas)
    width, height = canvas.size

    #current weather
    curr_temp = int(winfo.jsonFile['current_weather']['temperature'])
    curr_wind = winfo.jsonFile['current_weather']['windspeed']
    wind_direct = winfo.jsonFile['current_weather']['winddirection']
    curr_weather = winfo.jsonFile['current_weather']['weathercode']
    curr_time = winfo.jsonFile['current_weather']['time']

    #hourly data
    hourly_time = winfo.jsonFile['hourly']['time']
    feelslike_temp = winfo.jsonFile['hourly']['apparent_temperature']
    chance_of_rain = winfo.jsonFile['hourly']['precipitation_probability']
    
    #daily data
    daily_time = winfo.jsonFile['daily']['time']    
    daily_weather = winfo.jsonFile['daily']['weathercode']
    daily_temp_max = winfo.jsonFile['daily']['temperature_2m_max']
    daily_temp_min = winfo.jsonFile['daily']['temperature_2m_min']
    daily_precipitation = winfo.jsonFile['daily']['precipitation_probability_max']
    
    
  
    #generate strings to display
    #current temp
    celsius_txt = str(curr_temp)
    fahrenheit_txt = str(int((curr_temp * 1.8) + 32))
    curr_wind_txt = str(int(curr_wind))
    curr_wind_txt_Mph = str(int(curr_wind/1.609344))
    wind_direct_text = cordianl_Direction(wind_direct)
    weather_txt = weather_Codes[curr_weather]

    #today's time and date
    time_txt = datetime.datetime.strptime(curr_time, '%Y-%m-%dT%H:%M')
    date = time_txt.strftime("%d")
    month = time_txt.strftime("%b")
    day = time_txt.strftime("%A")
    update_time = time_txt.strftime("%H:%M")
  
    #daily time-->  0: today, 1: tomorrow, 2: day after tomorrow
    next_day1 = datetime.datetime.strptime(daily_time[1], '%Y-%m-%d')
    next_day1_txt = next_day1.strftime("%A")
    next_day2 = datetime.datetime.strptime(daily_time[2], '%Y-%m-%d')
    next_day2_txt = next_day2.strftime("%A")
    next_day3 = datetime.datetime.strptime(daily_time[3], '%Y-%m-%d')
    next_day3_txt = next_day3.strftime("%A")

    #daily weather-->  0: today, 1: tomorrow, 2: day after tomorrow
    next_day1_weather_txt = weather_Codes[daily_weather[1]]
    next_day2_weather_txt = weather_Codes[daily_weather[2]]
    next_day3_weather_txt = weather_Codes[daily_weather[3]]

    #feels like temp
    curr_time_txt = str(curr_time)
    currtime_index = hourly_time.index(curr_time_txt)
    celsius_feelslike = str(int(feelslike_temp[currtime_index]))
    fahrenheit_feelslike = str(int((feelslike_temp[currtime_index] * 1.8) + 32))
    

    #probable temp tomorrow
    next_day1_temp_max = str(int(daily_temp_max[1])) 
    next_day1_temp_min = str(int(daily_temp_min[1]))
    #probable temp day after tomorrow
    next_day2_temp_max = str(int(daily_temp_max[2])) 
    next_day2_temp_min = str(int(daily_temp_min[2]))
    #probable day 3
    next_day3_temp_max = str(int(daily_temp_max[3])) 
    next_day3_temp_min = str(int(daily_temp_min[3]))

    #chance of rain-->  0: today, 1: tomorrow, 2: day after tomorrow
    precipitation_chance_12hrs = str(max(chance_of_rain[currtime_index:currtime_index+12]))
    precipitation_chance_today = str(daily_precipitation[0])
    precipitation_chance_next_day1 = str(daily_precipitation[1])
    precipitation_chance_next_day2 = str(daily_precipitation[2])
    precipitation_chance_next_day3 = str(daily_precipitation[3])

# WHITE = #ffffff
# BLACK = #000000
# RED = #ff0000
# GREEN = #008000
# BLUE = #0000ff
# YELLOW = #ffff00
# ORANGE = #ffa500
    #draw.text((Xoffset , Yoffset), text/string, color,font=display_Fonts(fonts.normal,fontsize=34))
    # date 
    draw.text((15 , 5), day, fill='#000000',font=display_Fonts(fonts.light, fontsize=50))
    draw.text((width - 75, 5), month, fill='#0000ff', anchor="ra", font =display_Fonts(fonts.normal, fontsize=50))
    draw.text((width - 10, 5), date, fill='#ffa500', anchor="ra",font=display_Fonts(fonts.normal, fontsize=50))
    draw.text((width - 10, 80), 'As of: ' + update_time + ' CST', fill='#000000', anchor="ra",font=display_Fonts(fonts.light, fontsize=12))
   

    #current temp
    draw.text((15, 60), weather_txt, fill='#008000',font=display_Fonts(fonts.normal,fontsize=35))
    draw.text((width - 10, 140), '/' + fahrenheit_txt + u'\xb0F', fill='#000000', anchor="ra",font =display_Fonts(fonts.light, fontsize=45))
    currtempText_width = draw.textlength(fahrenheit_txt + u'\xb0F', font =display_Fonts(fonts.normal, fontsize=45))
    draw.text((width - currtempText_width - 25, 95), celsius_txt  + u'\xb0C', fill='#ff0000', anchor="ra",font =display_Fonts(fonts.normal, fontsize=90))
   
    
    
    #feels like 
    draw.text((width - 15, 220), 'Feels like' , fill='#000000', anchor="ra",font =display_Fonts(fonts.normal,fontsize=25))
    draw.text((width - 15, 245), '/' + fahrenheit_feelslike + u'\xb0F', fill='#000000', anchor="ra", font =display_Fonts(fonts.light, fontsize=30))
    feelslikeText_width = draw.textlength(fahrenheit_feelslike + u'\xb0F', font =display_Fonts(fonts.normal, fontsize=30))
    draw.text((width - feelslikeText_width - 25, 245), celsius_feelslike + u'\xb0C', fill='#ff0000', anchor="ra", font =display_Fonts(fonts.light, fontsize=30))
   
    
    

    #current weather icon
    weather_icon = Image.open(img_folder + weather_Icons[curr_weather]+'.jpg').convert("RGBA")
    weather_icon_resize = weather_icon.resize((120,120))
    canvas.paste(weather_icon_resize, (15, 105), weather_icon_resize)
    weather_icon_next_day1 = Image.open(img_folder + weather_Icons[daily_weather[1]]+'.jpg').convert("RGBA")
    new_weather_icon_next_day1 = weather_icon_next_day1.resize((60,60))
    weather_icon_next_day2 = Image.open(img_folder+ weather_Icons[daily_weather[2]]+'.jpg').convert("RGBA")
    new_weather_icon_next_day2 = weather_icon_next_day2.resize((60,60))
    weather_icon_next_day3 = Image.open(img_folder+weather_Icons[daily_weather[3]]+'.jpg').convert("RGBA")
    new_weather_icon_next_day3 = weather_icon_next_day3.resize((60,60))
    # draw current weather icon
    # draw.text((15, 90), weather_Icons[curr_weather], fill='#ffff00',font=display_Fonts(fonts.weathericon, fontsize=130))



    # chance of rain        
    draw.text((15, 220), 'Precipitation', fill='#000000', font =display_Fonts(fonts.normal,fontsize=25))
    draw.text((15, 245),  precipitation_chance_12hrs + '%' , fill='#008000', font =display_Fonts(fonts.light, fontsize=30))
    PrecipitationText_width = draw.textlength(precipitation_chance_12hrs + '%', font =display_Fonts(fonts.light, fontsize=30))
    draw.text((PrecipitationText_width +25, 250), 'chance' , fill='#000000', font =display_Fonts(fonts.light, fontsize=25))

    #Wind
    draw.text((220, 220), 'Wind' , fill='#000000', font =display_Fonts(fonts.normal,fontsize=25))
    wind_icon = Image.open(img_folder + 'wind.jpg').convert("RGBA")
    wind_icon_resize = wind_icon.resize((35,35))
    canvas.paste(wind_icon_resize, (285, 218), wind_icon_resize)
    draw.text((320  , 218), '(' + wind_direct_text + ')', fill='#008000', font =display_Fonts(fonts.normal,fontsize=25))
    draw.text((220, 245), curr_wind_txt + 'Kph', fill='#ff0000', font =display_Fonts(fonts.light, fontsize=30))
    WindText_width =  draw.textlength(curr_wind_txt + 'Kph', font =display_Fonts(fonts.normal, fontsize=30))
    draw.text((220 + WindText_width, 245), '/'+ curr_wind_txt_Mph + 'Mph' , fill='#000000', font =display_Fonts(fonts.light, fontsize=30))
    

    # weather of next few days
    #tomorrow
    draw.text((15, 290), next_day1_txt, fill='#000000', anchor="la", font =display_Fonts(fonts.normal,fontsize=25))
    draw.text((15, 320), next_day1_weather_txt, fill='#000000', anchor="la",font =display_Fonts(fonts.light,fontsize=18))
    canvas.paste(new_weather_icon_next_day1, (10, 350), new_weather_icon_next_day1)
    # draw.text((15, 350), weather_Icons[daily_weather[1]], fill='#ffa500', anchor="la", font=display_Fonts(fonts.weathericon, fontsize=45))
    draw.text((75, 355), next_day1_temp_max + u'\xb0C' + '/' +  next_day1_temp_min + u'\xb0C', fill='#ff0000', anchor="la",font =display_Fonts(fonts.normal,fontsize=20))
    draw.text((75, 375), precipitation_chance_next_day1 + '% chance', fill='#000000', anchor="la", font =display_Fonts(fonts.light,fontsize=20))

    #day after tomorrow
    draw.text((220, 290),  next_day2_txt , fill='#000000', anchor="la",font =display_Fonts(fonts.normal,fontsize=25))
    draw.text((220, 320), next_day2_weather_txt, fill='#000000', anchor="la",font =display_Fonts(fonts.light,fontsize=18))
    canvas.paste(new_weather_icon_next_day2, (215, 350), new_weather_icon_next_day2)
    # draw.text((220, 350), weather_Icons[daily_weather[2]], fill='#ffa500', anchor="la",font=display_Fonts(fonts.weathericon, fontsize=45))
    draw.text((280, 355), next_day2_temp_max + u'\xb0C' + '/' +  next_day2_temp_min + u'\xb0C', fill='#ff0000', anchor="la",font =display_Fonts(fonts.normal,fontsize=20))
    draw.text((280, 375), precipitation_chance_next_day2 + '% chance', fill='#000000', anchor="la",font =display_Fonts(fonts.light,fontsize=20))

    #next of day after tomorrow
    draw.text((420, 290),  next_day3_txt , fill='#000000', anchor="la",font =display_Fonts(fonts.normal,fontsize=25))
    draw.text((420, 320), next_day3_weather_txt, fill='#000000', anchor="la",font =display_Fonts(fonts.light,fontsize=18))
    canvas.paste(new_weather_icon_next_day3, (415, 350), new_weather_icon_next_day3)
    # draw.text((420, 350), weather_Icons[daily_weather[3]], fill='#ffa500', anchor="la",font=display_Fonts(fonts.weathericon, fontsize=45))
    draw.text((480, 355), next_day3_temp_max + u'\xb0C' + '/' +  next_day3_temp_min + u'\xb0C', fill='#ff0000', anchor="la",font =display_Fonts(fonts.normal,fontsize=20))
    draw.text((480, 375),  precipitation_chance_next_day3 + '% chance', fill='#000000', anchor="la",font =display_Fonts(fonts.light,fontsize=20))


    # print(currtime_index,'\n',chance_of_rain,'\n',precipitation_chance_12hrs)
   


def initGPIO():
    chip = gpiod.chip(0) # 0 chip 
    pin = 4
    gpiod_pin = chip.get_line(pin)
    config = gpiod.line_request()
    config.consumer = "Blink"
    config.request_type = gpiod.line_request.DIRECTION_OUTPUT
    gpiod_pin.request(config)
    return gpiod_pin

def setUpdateStatus(gpiod_pin, busy):
    if busy == True:
        gpiod_pin.set_value(1)
    else:
        gpiod_pin.set_value(0)

def update_epaper():
    gpio_pin = initGPIO()
    setUpdateStatus(gpio_pin, True)
    winfo = weather_Info()
    canvas = Image.new("RGB", canvasSize, (255, 255, 255))
    weather_Display(winfo, canvas)
    inky = Inky()
    inky.set_image(canvas, saturation=saturation)
    inky.show()
    setUpdateStatus(gpio_pin, False)

if __name__ == "__main__":
    update_epaper()
   
