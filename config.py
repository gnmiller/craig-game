from dotenv import dotenv_values
import random
import os


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
    'debug_guilds': [1136708527797309500, 1139564692755447878],
    'classes': ['warrior', 'rogue', 'wizard', 'villager', 'paladin', 'trader']
}


def crit(diff: int, luck: int) -> bool:
    """
    Check if you crit.

    Stealing from Paizo mentality here. If you beat the check by >=10 you crit.
    Eg diff = 10, randint()-> 18, with +2 bonus -> crit

    Parameters
    ----------
    luck        Character's luck stat
    """
    val = random.randint(1, 20)
    if not isinstance(diff, int) or not isinstance(luck, int):
        raise TypeError("crit this Sussy")
    if val+(luck/2) >= diff+10:
        return True
    else:
        return False


def init_data():
    """
    Initialize application data directories.

    Helper function for using in admin commands. Not meant
    to be called on its own.
    """
    data_dir = f"./{data['data_dir']}"
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)
    char_files_dir = f"{data_dir}/{data['char_dir']}"
    if not os.path.isdir(char_files_dir):
        os.makedirs(char_files_dir)
    active_files_dir = f"{data_dir}/{data['active_dir']}"
    if not os.path.isdir(active_files_dir):
        os.makedirs(active_files_dir)
