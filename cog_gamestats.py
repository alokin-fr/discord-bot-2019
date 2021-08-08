################################################################################################################################################################################
### This script is currently not working. TRN website has suspended their Rocket League Statistics API since June 2021, due to an update of Psyonix policies regarding APIs. ###
################################################################################################################################################################################

import discord
from discord.ext import commands
import json
import requests

def arrondir(x):    #For text formatting purposes.
    if x==round(x):
        return round(x)
    else:
        return x

token = ""

class Gamestats(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def rlstats(self,ctx,*words):
        name = " ".join(words)
        headers = {"TRN-Api-Key":token}

        r = requests.get(f"https://public-api.tracker.gg/v2/rocket-league/standard/profile/epic/{name}"", headers=headers)

        if str(r)=="<Response [404]>":
            return await ctx.send("Player not found.")

        data = r.json()

        ranktoemoji = {     #Dictionary which associates an emoji with a rank.
            "Bronze I":"<:Bronze1:>",
            "Bronze II":"<:Bronze2:>",
            "Bronze III":"<:Bronze3:>",
            "Silver I":"<:Silver1:>",
            "Silver II":"<:Silver2:>",
            "Silver III":"<:Silver3:>",
            "Gold I":"<:Gold1:>",
            "Gold II":"<:Gold2:>",
            "Gold III":"<:Gold3:>",
            "Platinum I":"<:Platinum1:>",
            "Platinum II":"<:Platinum2:>",
            "Platinum III":"<:Platinum3:>",
            "Diamond I":"<:Diamond1:>",
            "Diamond II":"<:Diamond2:>",
            "Diamond III":"<:Diamond3:>",
            "Champion I":"<:Champion1:>",
            "Champion II":"<:Champion2:>",
            "Champion III":"<:Champion3:>",
            "Grand Champion I":"<:GrandChampion1:>",
            "Grand Champion II":"<:GrandChampion2:>",
            "Grand Champion III":"<:GrandChampion3:>",
            "Supersonic Legend":"<:SupersonicLegend:>",
            "Unranked":"<:Unranked:>"
            }

        name = data["data"]["platformInfo"]["platformUserHandle"]

        modes = ["Ranked Duel 1v1","Ranked Doubles 2v2","Ranked Standard 3v3","Hoops","Rumble","Dropshot","Snowday","Tournament Matches"]
        values = []
        for j in range(8):  #Seek stats for each of these 8 modes. If no stats found, display "Unranked".
            try:
                for i in range(10):
                    if data["data"]["segments"][i]["metadata"]["name"] == modes[j]:
                        mmr = data["data"]["segments"][i]["stats"]["rating"]["value"]
                        perc = arrondir(data["data"]["segments"][i]["stats"]["rating"]["percentile"])
                        rank = data["data"]["segments"][i]["stats"]["tier"]["metadata"]["name"]
                        emoji = ranktoemoji[rank]
                        if rank == "Unranked":
                            values.append(f"{emoji}— {mmr} ᴍᴍʀ\nUnranked")
                        elif rank == "Supersonic Legend":
                            values.append(f"{emoji}— {mmr} ᴍᴍʀ\n{rank}\n*\> `{perc}`%*")
                        else:
                            rank = rank.split(" ")[0]+" "+str(rank.count("I"))
                            div = data["data"]["segments"][2]["stats"]["division"]["metadata"]["name"]
                            values.append(f"{emoji}— {mmr} ᴍᴍʀ\n{rank}\n{div}\n*\> `{perc}`%*")
                        break
                    elif i==9:
                        values.append(f"{ranktoemoji["Unranked"]}— 600 ᴍᴍʀ\nUnranked")
            except IndexError:
                values.append(f"{ranktoemoji["Unranked"]}— 600 ᴍᴍʀ\nUnranked")

        mmr_cas = data["data"]["segments"][1]["stats"]["rating"]["value"]   #Casual stats.
        perc_cas = arrondir(data["data"]["segments"][1]["stats"]["rating"]["percentile"])

        reward_level = data["data"]["segments"][0]["stats"]["seasonRewardLevel"]["metadata"]["rankName"]    #Reward stats.
        reward_matches = data["data"]["segments"][0]["stats"]["seasonRewardWins"]["value"]
        reward_perc = data["data"]["segments"][0]["stats"]["seasonRewardLevel"]["percentile"]
        if reward_level == "None":
            reward_level = "Unranked"
            reward_emoji = ranktoemoji["Unranked"]
            reward_perc = 0
        elif reward_level != "Supersonic Legend":
            reward_emoji = ranktoemoji[str(reward_level)+" I"]
        else:
            reward_emoji = ranktoemoji["Supersonic Legend"]
            reward_matches = 10
        description = f"**Season Reward Level**  — {reward_emoji} {reward_level} ({reward_matches}/10 wins) *(> `{arrondir(reward_perc)}`%)*"

        name = data["data"]["platformInfo"]["platformUserHandle"]

        if data["data"]["userInfo"]["countryCode"]:     #If the country of the player is specified, display its flag.
            flag = f':flag_{data["data"]["userInfo"]["countryCode"].lower()}:'
        else:
            flag = ""

        embed = discord.Embed(title=f"{name} {flag}", description=description, color=0x318ec4)
        embed.add_field(name=f"{chr(173)}\n**Ranked 1v1**",value=values[0],inline=True)
        embed.add_field(name=f"{chr(173)}\n**Ranked 2v2**",value=values[1],inline=True)
        embed.add_field(name=f"{chr(173)}\n**Ranked 3v3**",value=values[2],inline=True)
        embed.add_field(name=f"{chr(173)}\n**Rumble**",value=values[4],inline=True)
        embed.add_field(name=f"{chr(173)}\n**Dropshot**",value=values[5],inline=True)
        embed.add_field(name=f"{chr(173)}\n**Hoops**",value=values[3],inline=True)
        embed.add_field(name=f"{chr(173)}\n**Snowday**",value=values[6],inline=True)
        embed.add_field(name=f"{chr(173)}\n**Tournaments**",value=values[7],inline=True)
        embed.add_field(name=f"{chr(173)}\n**Casual**",value=f"— {mmr_cas} ᴍᴍʀ\n",inline=True)
        embed.set_author(name="Rocket League Stats", url=f"https://rocketleague.tracker.network/rocket-league/profile/epic/{name}/overview", icon_url="https://cdn2.iconfinder.com/data/icons/popular-games-1/50/rocketleague_squircle-512.png")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Gamestats(client))
