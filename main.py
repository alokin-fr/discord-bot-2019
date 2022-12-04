import discord
from discord import Webhook, RequestsWebhookAdapter
from discord.ext import commands
from random import randint
import time


prefix = "&"
client = commands.Bot(command_prefix=prefix)
client.remove_command("help")


@client.event       #Vérifier si le bot est en ligne
async def on_ready():
    await client.change_presence(status=discord.Status.online,  activity=discord.Game(f"{prefix}help"))
    global start_time
    start_time = time.strftime("%d.%m.%Y, %H:%M:%S(UTC+1)")
    print("Bot online. <{}>\a".format(start_time))


@client.command()       #Commande "ping" donnant le ping du bot
async def ping(ctx):
    t1 = time.monotonic()
    await ctx.send('Test ping en cours...')
    t2 = time.monotonic()
    await ctx.send("Latence : `{}` ms :hourglass:".format(int((t2-t1)*1000)))


@client.command()       #Commande "funfact"
async def funfact(ctx):
    file = open("txt_files/funfacts.txt","r",encoding="utf8")
    lines = file.readlines()
    file.close()
    max = int((len(lines)+1)/3)
    x = randint(0,max-1)
    fact = str(lines[3*x])
    img = str(lines[3*x+1])
    embed = discord.Embed(title="Fun Fact :bulb:", description=fact.format(n="\n"),color=0x318ec4)
    embed.set_image(url=img)
    await ctx.send(embed=embed)


@client.command()
async def avatar(ctx, mention: discord.Member):
    embed = discord.Embed(title=f"{mention.name} - Image de profil",color=0xfffffe)
    embed.set_image(url=mention.avatar_url)
    await ctx.send(embed=embed)


client.load_extension("cog_quiz")
client.load_extension("cog_minecraft")
client.load_extension("cog_weather")
client.run(token)
