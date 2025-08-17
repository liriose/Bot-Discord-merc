import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Stockage temporaire des primes
primes = []

@bot.event
async def on_ready():
    print(f"{bot.user} est prêt à servir les mercenaires !")

@bot.command()
async def prime(ctx, *, description):
    primes.append({"auteur": ctx.author.name, "description": description, "réponses": []})
    await ctx.send(f"Prime créée par {ctx.author.name} : {description}")

@bot.command()
async def repondre(ctx, index: int, *, réponse):
    try:
        primes[index]["réponses"].append({"mercenaire": ctx.author.name, "réponse": réponse})
        await ctx.send(f"{ctx.author.name} a répondu à la prime #{index}")
    except IndexError:
        await ctx.send("Cette prime n'existe pas.")

@bot.command()
async def liste(ctx):
    if not primes:
        await ctx.send("Aucune prime en cours.")
    else:
        msg = ""
        for i, p in enumerate(primes):
            msg += f"#{i} - {p['description']} (par {p['auteur']})\n"
        await ctx.send(msg)

bot.run(TOKEN)
