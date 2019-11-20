import discord
from async_timeout import timeout
from discord.ext import commands
import os

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='clear', pass_context = True, hidden=True)
    @commands.has_permissions(manage_guild=True)
    async def clear(self, ctx, number):
        """An admin command for deleteing lots of messages"""
        mgs = [] #Empty list to put all the messages in the log
        number = int(number) #Converting the amount of messages to delete to an integer
        async for x in ctx.message.channel.history(limit=number):
            mgs.append(x)
        await ctx.message.channel.delete_messages(mgs)
        await ctx.send(f"I deleted {number} messages in this channel",delete_after=4)
    # 
    # async def bump_server(self,ctx):
    #     channel_t = ctx.message.get
    #     await asyncio.sleep(10)
    #     ctx.send("!d bump")


def setup(bot):
    bot.add_cog(Admin(bot))
