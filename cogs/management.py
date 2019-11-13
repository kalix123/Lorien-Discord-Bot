"""This is a cog for a discord.py bot.
It will add some management commands to a bot.
Commands:
    load            load an extension / cog
    unload          unload an extension / cog
    reload          reload an extension / cog
    cogs            show currently active extensions / cogs
    error           print the traceback of the last unhandled error to chat
Only users that have an admin role can use the commands.
"""
import subprocess
import json
import traceback
from datetime import datetime
from os import path, listdir, pardir
from discord import Activity, Embed, Member
from discord.ext import commands


class Management(commands.Cog, name='Management'):
    def __init__(self, client):
        self.client = client
        self.reload_config()

    # async def cog_check(self, ctx):
    #     return self.client.user_is_admin(ctx.author)

    @commands.Cog.listener()
    async def on_ready(self):
        loaded = self.client.extensions
        unloaded = [x for x in self.crawl_cogs() if x not in loaded]



    # ----------------------------------------------
    # Error handler
    # ----------------------------------------------
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
            return

        if isinstance(error, commands.MissingRequiredArgument):
            par = str(error.param)
            missing = par.split(": ")[0]
            if ':' in par:
                missing_type = ' (' + str(par).split(": ")[1] + ')'
            else:
                missing_type = ''
            await ctx.send(
                f'Missing parameter: `{missing}{missing_type}`' +
                f'\nIf you are not sure how to use the command, try running ' +
                f'`-help {ctx.command.qualified_name}`'
            )
            return

        if isinstance(error, commands.CheckFailure):
            await ctx.send('Sorry, you are not allowed to run this command.')
            return

        if isinstance(error, commands.CommandNotFound):
            # await ctx.send(f'Sorry, command `{ctx.invoked_with}` not found.')
            return

        if isinstance(error, commands.BadArgument):
            # It's in an embed to prevent mentions from working
            embed = Embed(
                title='Error',
                description=str(error),
                color=0x2ECC71
            )
            await ctx.send(embed=embed)
            return

        # In case of an unhandled error -> Save the error + current datetime
        # so it can be accessed later with the error command
        await ctx.send('Sorry, something went wrong.')
        await self.client.change_presence(
            activity=Activity(name='ERROR encountered', url=None, type=3)
        )

        print(f'Ignoring exception in command {ctx.command}:')
        traceback.print_exception(
            type(error), error, error.__traceback__
        )

    def reload_config(self):
        with open("config.json") as conffile:
            self.client.config = json.load(conffile)


    def crawl_cogs(self, directory='cogs'):
        cogs = []
        for element in listdir(directory):
            if element == 'samples':
                continue
            abs_el = path.join(directory, element)
            if path.isdir(abs_el):
                cogs += self.crawl_cogs(abs_el)
            else:
                filename, ext = path.splitext(element)
                if ext == '.py':
                    dot_dir = directory.replace('\\', '.')
                    dot_dir = dot_dir.replace('/', '.')
                    cogs.append(f'{dot_dir}.' + filename)
        return cogs

    # ----------------------------------------------
    # Function to load extensions
    # ----------------------------------------------
    @commands.command(
        name='load',
        brief='Load bot extension',
        description='Load bot extension\n\nExample: -load cogs.Music',
        hidden=True,
    )
    async def load_extension(self, ctx, extension_name):
        for cog_name in self.crawl_cogs():
            if extension_name in cog_name:
                target_extension = cog_name
                break
        try:
            self.client.load_extension(target_extension)
        except Exception as e:
            self.client.last_errors.append((e, datetime.utcnow(), ctx))
            await ctx.send(f'```py\n{type(e).__name__}: {str(e)}\n```')
            return
        await ctx.send(f'```css\nExtension [{target_extension}] loaded.```')

    # ----------------------------------------------
    # Function to unload extensions
    # ----------------------------------------------
    @commands.command(
        name='unload',
        brief='Unload bot extension',
        description='Unload bot extension\n\nExample: -unload cogs.Music',
        hidden=True,
    )
    async def unload_extension(self, ctx, extension_name):
        for cog_name in self.client.extensions:
            if extension_name in cog_name:
                target_extension = cog_name
                break
        if target_extension.lower() in 'cogs.Management':
            await ctx.send(
                f"```diff\n- {target_extension} can't be unloaded" +
                f"\n+ try -reload {target_extension}!```"
            )
            return
        if self.client.extensions.get(target_extension) is None:
            return
        self.client.unload_extension(target_extension)
        await ctx.send(f'```css\nExtension [{target_extension}] unloaded.```')

    # ----------------------------------------------
    # Function to reload extensions
    # ----------------------------------------------
    @commands.command(
        name='reload',
        brief='Reload bot extension',
        description='Reload bot extension\n\nExample: -reload cogs.Music',
        hidden=True,
        aliases=['re']
    )
    async def reload_extension(self, ctx, extension_name):
        target_extensions = []
        if extension_name == 'all':
            target_extensions = [__name__] + \
                [x for x in self.client.extensions if not x == __name__]
        else:
            for cog_name in self.client.extensions:
                if extension_name in cog_name:
                    target_extensions = [cog_name]
                    break
        if not target_extensions:
            return
        result = []
        for ext in target_extensions:
            try:
                self.client.reload_extension(ext)
                result.append(f'Extension [{ext}] reloaded.')
            except Exception as e:
                self.client.last_errors.append((e, datetime.utcnow(), ctx))
                result.append(f'#ERROR loading [{ext}]')
                continue
        result = '\n'.join(result)
        await ctx.send(f'```css\n{result}```')

    # ----------------------------------------------
    # Function to get bot extensions
    # ----------------------------------------------
    @commands.command(
        name='cogs',
        brief='Get loaded cogs',
        description='Get loaded cogs',
        aliases=['extensions'],
        hidden=True,
    )
    async def print_cogs(self, ctx):
        loaded = self.client.extensions
        unloaded = [x for x in self.crawl_cogs() if x not in loaded]
        response = ['\n[Loaded extensions]'] + ['\n  ' + x for x in loaded]
        response += ['\n[Unloaded extensions]'] + \
            ['\n  ' + x for x in unloaded]
        await ctx.send(f'```css{"".join(response)}```')
        return True


    # ----------------------------------------------
    # Function to get the date a member joined
    # ----------------------------------------------
    @commands.command(
        name='joined',
        hidden=True,
    )
    async def joined(self, ctx, members: commands.Greedy[Member]):
        """Print the date a member joined"""
        if not members:
            raise commands.BadArgument('Please specify at least 1 member')
        await ctx.trigger_typing()
        result = []
        now = datetime.utcnow()
        for member in members:
            join = member.joined_at
            if not join:
                result.append(f'No join date found for {member.name}')
                continue
            difference = now - join
            result.append(
                f'{member.name} joined [{join.isoformat().split(".")[0]}] - '
                f'[{difference.days}] days and '
                f'[{difference.seconds / 3600:.1f}] hours ago'
            )
        if not result:
            return
        await ctx.send('```css\n' + '\n'.join(result) + '\n```')

    @commands.group(
        invoke_without_command=True,
        name='error',
        hidden=True,
        aliases=['errors']
    )
    async def error(self, ctx):
        """Show a concise list of stored errors"""
        error_log = self.client.last_errors

        if not error_log:
            await ctx.send('Error log is empty')
            return

        response = [f'```css\nNumber of stored errors: {len(error_log)}']
        for i, exc_tuple in enumerate(error_log):
            exc, date, error_ctx = exc_tuple
            call_info = (
                f'CMD: {error_ctx.invoked_with}' if error_ctx else 'no command'
            )
            response.append(
                f'{i}: ['
                + date.isoformat().split('.')[0]
                + '] - ['
                + call_info
                + f']\nException: {exc}'
            )
        response.append('```')

        await ctx.send('\n'.join(response))

    @error.command(
        name='clear',
    )
    async def error_clear(self, ctx, n=None):
        """Clear the oldest [n] errors from the error log (0 = all errors)"""
        if not n:
            self.client.last_errors = []
            await ctx.send('Error log cleared')
        else:
            for _ in range(n):
                self.client.last_errors.pop(0)
            await ctx.send(f'Deleted the {n} oldest messages ')

    @error.command(
        name='traceback',
        aliases=['tb'],
    )
    async def error_traceback(self, ctx, n: int = None):
        """Print the traceback of error [n] from the error log"""
        error_log = self.client.last_errors

        if not error_log:
            await ctx.send('Error log is empty')
            return

        if n is None:
            await ctx.send('Please specify an error index')
            await self.client.get_command('error').invoke(ctx)
            return

        if n >= len(error_log) or n < 0:
            await ctx.send('Error index does not exist')
            return

        exc, date, error_ctx = error_log[n]
        delta = (datetime.utcnow() - date).total_seconds()
        hours = int(delta // 3600)
        seconds = int(delta - (hours * 3600))
        delta_str = f'{hours} hours and {seconds} seconds ago'
        tb = ''.join(
            traceback.format_exception(type(exc), exc, exc.__traceback__)
        )
        response = [f'`Error occured {delta_str}`']
        if error_ctx:
            response.append(f'`Command: {error_ctx.invoked_with}`')
            response.append(f'`User: {error_ctx.author.name}`')
            response.append(f'`Channel:{error_ctx.channel.name}`')
        else:
            response.append('`Error happened outside of command`')
        response.append(f'```python\n{tb}```')
        await ctx.send('\n'.join(response))


def setup(client):
    client.add_cog(Management(client))
