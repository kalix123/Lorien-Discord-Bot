import discord
import asyncio

from async_timeout import timeout
from discord.ext import commands
import os


class Reaction(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.images = {}
        self.emoji = {
            "0": '\u0001f44d',
            "1": "1\u20e3"
        }
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        msg = reaction.message
        message_id = str(msg.id)
        if user.bot:
            return
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.attachments:
            # react_emoji = self.bot.get_emoji("647509460507688971")
            await message.add_reaction(emoji="\N{GLOBE WITH MERIDIANS}")
            await message.add_reaction(emoji="U+20E3")


def setup(bot):
    bot.add_cog(Reaction(bot))
