import os
import shutil

import char_cmds
import config
import discord
from discord.ext import commands


class adminCommands(commands.Cog):
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
        """Stop the application (gracefully)."""
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
        """
        Purge the game data directory for testing purposes.

        This will delete ALL data files without any check or confirmation.
        Use at your own risk.

        Parameters
        ----------
        ctx:     The discord context object for the command
        """
        path = f"./{config.data['data_dir']}/"
        try:
            # os.remove(path)
            shutil.rmtree(path)
            await ctx.respond("```Dleted all data files for game.```")
        except FileNotFoundError as e:
            await ctx.respond("could not delete files check disk")
            raise FileNotFoundError(f"could not find {path} -- {e}")

    @commands.slash_command(
        description="Initialize the data directory for the game.",
        help="Init game data dir for testing.",
        brief="Init game data dir for testing.",
        hidden=True,
        name='reset'
    )
    @commands.is_owner()
    async def _reset(self, ctx):
        """
        Recreate the game data dirs for testing.

        This will attempt to create the top-level and sub-directories
        specified in config.data for the game. Raises FileExistsError
        if any of the files exists already.

        Parameters
        ----------
        ctx:     The discord context object for the command
        """
        try:
            data_dir = f"./{config.data['data_dir']}"
            if not os.path.isdir(data_dir):
                os.makedirs(data_dir)
            char_files_dir = f"{data_dir}/{config.data['char_dir']}"
            if not os.path.isdir(char_files_dir):
                os.makedirs(char_files_dir)
            active_files_dir = f"{data_dir}/{config.data['active_dir']}"
            if not os.path.isdir(active_files_dir):
                os.makedirs(active_files_dir)
            await ctx.respond("```Initialized game data.```")
        except FileExistsError as e:
            raise FileExistsError(f"```Failed to initialize game data files. {e}```")

    @commands.slash_command()
    @commands.is_owner()
    async def set_coins(self, ctx,
                        name, value,
                        user: discord.Option(str,
                                             description="Mention a user",
                                             required=False)):
        """
        Set a user's coin count.

        Explicitly set the amount of gold a user has.
        """
        user_id = ""
        try:
            for m in ctx.mentions:
                user_id = m.id
                break
        except Exception:
            user_id = ctx.author.id
        try:
            me = char_cmds.load_char(user_id, name)
            me.inventory.set_gold(value)
            char_cmds.save_char(user_id, me)
        except Exception:
            await ctx.respond("```failed```")
            return
        await ctx.respond(f"```Set gold value for {me.name} to {value}.```")

    @commands.slash_command()
    @commands.is_owner()
    async def set_exp(self, ctx,
                      name, value,
                      user: discord.Option(str,
                                           description="Mention a user",
                                           required=False)):
        """
        Set a user's coin count.

        Explicitly set the amount of exp a user has.
        """
        user_id = ""
        try:
            for m in ctx.mentions:
                user_id = m.id
                break
        except Exception:
            user_id = ctx.author.id
        try:
            me = char_cmds.load_char(user_id, name)
            me.experience = int(value)
            char_cmds.save_char(user_id, me)
        except Exception as e:
            await ctx.respond(f"```failed {e}```")
            return
        await ctx.respond(f"```Set exp value for {me.name} to {value}.```")
