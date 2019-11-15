# import Music
# import Simpleton
import json
import os
import discord
import youtube_dl
from async_timeout import timeout
from discord.ext import commands

with open('config.json') as conffile:
    config = json.load(conffile)

bot = commands.Bot('-', description='Lorien is god of all things')
welcome_channel = bot.get_channel(642518190626177024)
rules_channel = bot.get_channel(642528338287656990)
meet_channel = bot.get_channel(643342309899108352)

STARTUP_EXTENSIONS = []

for file in os.listdir(os.path.join(os.path.dirname(__file__), 'cogs/')):
    filename, ext = os.path.splitext(file)
    if '.py' in ext:
        STARTUP_EXTENSIONS.append(f'cogs.{filename}')

for cog in STARTUP_EXTENSIONS:
    try:
        bot.load_extension(cog)
        print(cog + " loaded")
    except Exception as e:
        print(e)

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="person")
    await member.add_roles(role)
    await welcome_channel.send(f"Hello {member.mention}. Welcome to **People Things**! Enjoy your stay and be sure to read {rules_channel.mention} before introducing yourself in {meet_channel.mention}")


@bot.event
async def on_ready():
    print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))

bot.run(config["bot_key"])
