import discord
import asyncio

from async_timeout import timeout
from discord.ext import commands
import os


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.my_task = self.bot.loop.create_task(self.bump_server())


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

    async def bump_server(self):
        # await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await asyncio.sleep(7200)
            user = self.bot.get_user(187677490452496394)
            await user.send('SEND THE FUCKING BUMP COMMAND ON THE *PEOPLE THINGS* SEVER')
    def cog_unload(self):
        self.my_task.cancel()

def setup(bot):
    bot.add_cog(Admin(bot))
