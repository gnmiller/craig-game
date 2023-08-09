from dotenv import dotenv_values

max_characters = 10
"""
Provide a centralized dictionary of commonly used parameters for the bot.

Parameters
----------
data_dir        The location for file storage for the application. Serves as a
                    prefix for other file paths. (default = 'rpg-data')
char_dir        The location to store character files. (default = 'character')
active_dir      The location to store a user's active character. (default = 'active')
file_ext        The file extension to use for all files. (default = 'pickle')
envs            Environment variables for the application. DISCORD_TOKEN should be set here.
                    DISCORD_APP_ID and DISCORD_PERMS should also be set here if you want the
                    application to print a valid invite URL for you.
max_characters  The maximum number of characters a user may create
debug_guilds    A list of guilds used for debugging. Should be removed in production.
classes         A list of currently supported classes for the application
"""
data = {
    'data_dir': 'rpg-data',
    'char_dir': 'character',
    'active_dir': 'active',
    'file_ext': 'pickle',
    'envs': dotenv_values(".env"),
    'max_characters': 10,
    'debug_guilds': [1136708527797309500],
    'classes': ['warrior', 'rogue', 'wizard', 'villager', 'paladin', 'trader']
}
