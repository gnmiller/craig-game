import os

import admin
import char_cmds
import config
import discord
import fishing_cmds
import inventory_cmds
from discord.ext import commands

# from dotenv import dotenv_values

intents = discord.Intents(messages=True, presences=True, guilds=True,
                          members=True, reactions=True, message_content=True)
bot = commands.Bot(command_prefix="!",
                   intents=intents,
                   debug_guilds=config.data['debug_guilds'])


def invite_uri():
    app_id = config.data['envs']['DISCORD_APP_ID']
    perms = config.data['envs']['DISCORD_APP_PERMS']
    scope = "bot%20applications.commands"
    ret = "https://discord.com/api/oauth2/authorize?"\
          f"client_id={app_id}&permissions={perms}&scope={scope}"
    return ret


@bot.event
async def on_ready():
    data_dir = f"./{config.data['data_dir']}"
    try:
        if not os.path.isdir(data_dir):
            os.makedirs(data_dir)
        char_files_dir = f"{data_dir}/{config.data['char_dir']}"
        if not os.path.isdir(char_files_dir):
            os.makedirs(char_files_dir)
        active_files_dir = f"{data_dir}/{config.data['active_dir']}"
        if not os.path.isdir(active_files_dir):
            os.makedirs(active_files_dir)
    except FileExistsError:
        raise FileExistsError("could not initialize bot files")
    for g in bot.guilds:
        pass
    # cogs = ['char_cmds']
    # for c in cogs:
    #     bot.load_extension(c)
    print(invite_uri())
    return


@bot.event
async def on_guild_join(guild):
    pass

bot.add_cog(admin.adminCommands(bot))
bot.add_cog(char_cmds.characterCommands(bot))
bot.add_cog(inventory_cmds.inventoryCommands(bot))
bot.add_cog(fishing_cmds.Fishing(bot))
bot.run(config.data['envs']['DISCORD_TOKEN'])
