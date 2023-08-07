from discord.ext import commands


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
