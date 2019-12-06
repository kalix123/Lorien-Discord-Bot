import discord
import asyncio

from async_timeout import timeout
from discord.ext import commands
import os


# dicts_from_file now contains the dictionaries created from the text file
with open('cogs/countries.txt','r') as inf:
    dict_from_file = eval(inf.read())
country_definitions = dict_from_file
country_backup = open('cogs/active_countries.txt','r').read().splitlines()



class Countries(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.full_message = "Countries:\n\n"
        for country in country_backup:
            for key,value in country_definitions.items():
                if value == country:
                    self.full_message = self.full_message + country + ": " + key + "\n"

        self.countries = []
        self.active_post = 0
        self.announcment_channel = None

    @commands.command(name='send', hidden=True)
    @commands.has_permissions(manage_guild=True)
    async def send(self,message, channel_id : int):
        self.announcment_channel = self.bot.get_channel(channel_id)
        await self.announcment_channel.send(self.full_message)

    @commands.command(name='clear_countries', hidden=True)
    @commands.has_permissions(manage_guild=True)
    async def clear_countries(self,message):
        with open('cogs/active_countries.txt', 'w') as file:
            file.write('')
        self.countries = []
        await message.send("all countries cleared from list and text file")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        msg = reaction.message
        message_id = str(msg.id)
        if user.bot:
            return
        if reaction.emoji not in self.countries:
            if reaction.emoji in country_definitions:
                self.countries.append(reaction.emoji)
                with open('cogs/active_countries.txt', 'a+') as file:
                    file.write(f"{country_definitions[reaction.emoji]}\n")
                self.full_message = self.full_message + country_definitions[reaction.emoji] + ": " + reaction.emoji + "\n"
                await reaction.message.edit(content = self.full_message)
            else:
                await reaction.remove(user)



def setup(bot):
    bot.add_cog(Countries(bot))
