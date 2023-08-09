from discord.ext import commands
import os
import shutil
import config


class admin_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, module):
        """Loads a module."""
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.respond('\N{PISTOL}')
            await ctx.respond('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.respond('\N{OK HAND SIGN}')

    @commands.slash_command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, module):
        """Unloads a module."""
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await ctx.respond('\N{PISTOL}')
            await ctx.respond('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.respond('\N{OK HAND SIGN}')

    @commands.slash_command(name='reload', hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, module):
        """Reloads a module."""
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.respond('\N{PISTOL}')
            await ctx.respond('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.respond('\N{OK HAND SIGN}')

    @commands.slash_command(
        description="Shut the bot down.",
        help="Stop the bot. Owner only.",
        brief="Stop the bot. Owner only.",
        aliases=['quit', 'stop']
    )
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.respond("goodbye")
        await ctx.bot.close()

    @commands.slash_command(
        description="Delete ALL data for the game.",
        help="Purge data for testing.",
        brief="Purge data for testing.",
        hidden=True,
        name='flush'
    )
    @commands.is_owner()
    async def _flush(self, ctx):
        path = f"./{config.data['data_dir']}/"
        try:
            # os.remove(path)
            shutil.rmtree(path)
            await ctx.respond("deleted all data files for game")
        except FileNotFoundError as e:
            await ctx.respond("could not delete files check disk")
            raise FileNotFoundError(f"could not find {path} -- {e}")
