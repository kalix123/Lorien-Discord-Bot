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
            "x": "❌"
        }

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        msg = reaction.message
        message_id = str(msg.id)
        # print(reaction)
        if msg.attachments:
            if user.bot:
                return
            if reaction.emoji == self.emoji["thumbsup"]:
                print("going up")
                self.images[message_id]["thumbsup"] += 1
            elif reaction.emoji == self.emoji["x"]:
                self.images[message_id]["x"] += 1
            if (self.images[message_id]["x"] >= 3) and (self.images[message_id]["x"] > self.images[message_id]["thumbsup"]):
                await msg.delete()
        # print(f"------------\nthumbsup: {self.images[message_id]['thumbsup']}\nx: {self.images[message_id]['x']}\n------------")
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        msg = reaction.message
        message_id = str(msg.id)
        if msg.attachments:
            if user.bot:
                return
            if reaction.emoji == self.emoji["thumbsup"]:
                self.images[message_id]["thumbsup"] -= 1
            elif reaction.emoji == self.emoji["x"]:
                self.images[message_id]["x"] -= 1

        # print(f"------------\nthumbsup: {self.images[message_id]['thumbsup']}\nx: {self.images[message_id]['x']}\n------------")

    @commands.Cog.listener()
    async def on_message(self,msg):
        if msg.attachments:
            image_msg = msg
            image_id = str(image_msg.id)
            for choice in self.emoji:
                react_emoji = self.emoji[choice]
                await msg.add_reaction(emoji=react_emoji)

            self.images[image_id] = {'thumbsup': self.up_amount, 'x': self.down_amount}


def setup(bot):
    bot.add_cog(Reaction(bot))
