import discord
from discord.ext import commands
import requests
import json
import time


class Weather(commands.Cog):
    def __init__(self,client):
        self.client = client


    async def get_emoji(id):
        dict_id8xx = {800:":sunny:",801:":white_sun_small_cloud:",802:":partly_sunny:",803:":white_sun_cloud:",804:":cloud:"}
        if id > 799:
            return dict_id8xx[id]
        elif id > 699:
            return ":fog:"
        elif id > 599:
            return ":cloud_snow:"
        elif id > 501:
            return ":cloud_rain:"
        elif id > 299:
            return ":white_sun_rain_cloud:"
        elif id > 229:
            return ":thunder_cloud_rain:"
        elif id > 209:
            return ":cloud_lightning:"
        elif id > 199:
            return ":thunder_cloud_rain:"
        else:
            return ""

    @commands.command()
    async def weather(self,ctx,*words):
        town = " ".join(words)
        r = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?q={town}&appid=81dbde26c5fa0de299d648d847fecdc9&lang=fr&units=metric")
        data=r.json()

    #    emoji_weather = await get_emoji(data["list"][0]["weather"][0]["id"])

    #    emoji2color = {}

        id_weather = data["list"][0]["weather"][0]["id"]
        color_weather = 0xfffffe
        if id_weather > 799:
            emoji_weather = dict_id8xx[id_weather]
            if id_weather < 803:
                color_weather = 0xffac33
        elif id_weather > 699:
            emoji_weather = ":fog:"
        elif id_weather > 599:
            emoji_weather = ":cloud_snow:"
        elif id_weather > 501:
            emoji_weather = ":cloud_rain:"
            color_weather = 0x5dadec                    #Bleu clair
        elif id_weather > 299:
            emoji_weather = ":white_sun_rain_cloud:"
            color_weather = 0x5dadec                    #Bleu clair
        elif id_weather > 229:
            emoji_weather = ":thunder_cloud_rain:"
            color_weather = 0x343c42
        elif id_weather > 209:
            emoji_weather = ":cloud_lightning:"
            color_weather = 0x343c42
        elif id_weather > 199:
            emoji_weather = ":thunder_cloud_rain:"
            color_weather = 0x343c42
        else:
            pass
        weather = data["list"][0]["weather"][0]["description"]  #Temps

        temp = round(data["list"][0]["main"]["temp"],1)         #Température
        felt_temp = data["list"][0]["main"]["feels_like"]       #Température ressentie

        icon = data["list"][0]["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"

        city = data["city"]["name"]                             #Ville
        flag = data["city"]["country"].lower()                  #Code pays

        tz_sec = data["city"]["timezone"]
        time_zone = tz_sec/3600
        try:
            time_zone = int(time_zone)
        except ValueError:
            pass
        time_zone = str(time_zone)
        if time_zone.startswith("-"):
            pass
        else:
            time_zone = "+" + time_zone
        local_date = time.strftime("%d.%m.%Y",time.gmtime(data["list"][0]["dt"]+tz_sec))        #Heure locale
        local_time = time.strftime(f"%Hh%M (UTC{time_zone}/local)",time.gmtime(data["list"][0]["dt"]+tz_sec))
        local_hmod12 = int(time.strftime("%H",time.gmtime(data["list"][0]["dt"]+tz_sec)))%12
        if local_hmod12 == 0:
            local_hmod12 = 12
        else:
            pass

        sunrise_time = time.strftime("%Hh%M",time.gmtime(data["city"]["sunrise"]+tz_sec))       #Heure du lever
        sunset_time = time.strftime("%Hh%M",time.gmtime(data["city"]["sunset"]+tz_sec))         #Heure du coucher
        cloudiness = data["list"][0]["clouds"]["all"]                                           #Couverture nuageuse

        humidity = data["list"][0]["main"]["humidity"]                                          #Humidité
        pressure = data["list"][0]["main"]["pressure"]                                          #QNH
        wind_speed = data["list"][0]["wind"]["speed"]                                   #Vitesse vent
        wind_deg = data["list"][0]["wind"]["deg"]                                       #Direction vent
        visibility = data["list"][0]["visibility"]
        if visibility == 10000:
            visibility = ">" + str(visibility)
        else:
            pass
        proba = data["list"][0]["pop"]


        embed = discord.Embed(title="Bulletin météo : {}".format(city), description = "Prévisions météorologiques pour :\n - {} :flag_{}:\n - {} :date:\n - {} :clock{}:".format(city,flag,local_date,local_time,local_hmod12), color=color_weather)
        embed.add_field(name="__**Général**__",value=f"{emoji_weather} **Temps :** {weather}\n:thermometer: **Température :** {temp}°C",inline=False)
        embed.add_field(name="__**Ensoleillement**__",value=f":city_sunrise: **Lever du soleil :** {sunrise_time}\n:night_with_stars: **Coucher du soleil :** {sunset_time}\n:cloud: **Couverture nuageuse :** {cloudiness}%\n:high_brightness: **Indice UV :** on s'en blc",inline=False)
        embed.add_field(name="__**Détails**__",value=f":droplet: **Humidité :** {humidity}%\n:compression: **Pression :** {pressure} hPa\n:leaves: **Vent :** {int(round(wind_speed*3.6,1))} km/h, {wind_deg}°\n:eye: **Visibilité :** {visibility} m\n:cloud_rain: **Probabilité de précipitation :** {int(round(proba*100,0))}%",inline=False)
        embed.set_footer(text="Source : OpenWeatherMap")
        embed.set_thumbnail(url=icon_url)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Weather(client))
