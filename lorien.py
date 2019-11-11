# import Music
# import Simpleton

import discord
import youtube_dl
from async_timeout import timeout
from discord.ext import commands


bot = commands.Bot('-', description='Yet another music bot.')

STARTUP_EXTENSIONS = ['cogs.Music','cogs.Admin']

for cog in STARTUP_EXTENSIONS:
    try:
        bot.load_extension(cog)
        print(cog + " loaded")
    except:
        print("there was an error loading " + cog)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(642518190626177024)
    role = discord.utils.get(member.guild.roles, name="person")
    await member.add_roles(role)
    await channel.send(f"Hello {member.mention}. Welcome to **People Things**! Enjoy your stay and be sure to read #rules before introducing yourself in #meet-and-greet")

# @bot.event
# async def on_message():
#     if me
@bot.event
async def on_ready():
    print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))

bot.run('NjQyNDUyNzQ5ODYyMDQzNjUz.Xcix5g.EEvemrtG5b8Cs-NjP4k2pXEy-Sk')
