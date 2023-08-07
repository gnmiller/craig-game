import discord
import admin
from discord.ext import commands
from dotenv import dotenv_values


config = dotenv_values(".env")

intents = discord.Intents(messages=True, presences=True, guilds=True, 
                          members=True, reactions=True, message_content=True)
bot = commands.Bot(command_prefix="!", intents=intents)


def invite_uri():
    app_id = config['DISCORD_APP_ID']
    perms = config['DISCORD_APP_PERMS']
    scope = "bot%20applications.commands"
    ret = "https://discord.com/api/oauth2/authorize?"\
          f"client_id={app_id}&permissions={perms}&scope={scope}"
    return ret


@bot.event
async def on_ready():
    for g in bot.guilds:
        pass
    cogs = ['char_cmds']
    for c in cogs:
        bot.load_extension(c)
    print(invite_uri())
    return


@bot.event
async def on_guild_join(guild):
    pass

bot.add_cog(admin.admin_Commands(bot))
#  bot.load_extension("char_cmds")
bot.run(config['DISCORD_TOKEN'])
