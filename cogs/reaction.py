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
            "thumbsup": "👍",
            "x": '❌'
        }

    @commands.Cog.listener()
    async def on_message(self,msg):
        if msg.attachments:
            print(self.images)
            image_msg = msg
            image_id = str(image_msg.id)
            for choice in self.emoji:
                react_emoji = self.emoji[choice]
                self.images[image_id] = self.images.get(image_id, []) + [react_emoji]
                await msg.add_reaction(emoji=react_emoji)



def setup(bot):
    bot.add_cog(Reaction(bot))
