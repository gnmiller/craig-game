from discord.ext import commands
from discord import SlashCommandGroup
from collections import Counter
from tabulate import tabulate
import discord
import character
import os
import config
import pickle


class character_Commands(commands.Cog):
    character_command_group = SlashCommandGroup(name='character',
                                                description='Commands for interacting '
                                                'with your character(s).')

    def __init__(self, bot):
        """Construct the character_Commands cog.

        This Cog provides commands for interacting with a user's characters such as
        creating, deleting and setting the current character to use.

        By default this Cog expects that the following directories will exist:
            ./rpg-data
            ./rpg-data/characters/
            ./rpg-data/active/
        These should be created in on_ready() (or before running the bot)
        The values for these directories can be customized in config.py by
        modifying their values in config.data. These are expected to be plain names
        with no OS special characters.
        Ex:
            config.data['data_dir'] = 'rpg-data' GOOD
            config.data['data_dir'] = '/rpg-data' BAD"""
        self.bot = bot

    def get_class_types(ctx: discord.AutocompleteContext):
        return ['warrior', 'rogue', 'wizard', 'villager', 'paladin', 'trader']

    @character_command_group.command(
            description="Create a new character.",
            help="Create a new character.",
            brief="Create a new character.",
            aliases=["make", "new"]
            )
    async def create(self,
                     ctx: discord.ApplicationContext,
                     name: discord.Option(str,
                                          description='Enter a name for your character.',
                                          required=True),
                     c_name: discord.Option(str,
                                            description="choose your class",
                                            autocomplete=discord.utils.basic_autocomplete(get_class_types))):
        """Create a new character

        Attempt to create a new character in the associated file structure.
            By default characters are stored in
            ./rpg-data/characters/<discord user_id>/<character name>.pickle.
            This is customizable in config.data via the data_dir, char_dir, and file_ext options.

        A new `character.Character` object is contructed via `create_char()`
            then passed to `save_char()`.

        The object returned from `create_char()` is sent to the user.

        Paramters
        ---------
        ctx     The discord context object for the command
        name    The character's name
        c_name  The character's class
        """
        try:
            new_char = create_char(user_id=ctx.author.id, name=name, c_name=c_name, )
            await ctx.respond(f"Character created for {ctx.author.mention}!\n```{new_char}```\n")
        except FileNotFoundError:
            await ctx.respond("Failed to create a character. Please try again.")

    @character_command_group.command(
            description="List out all your characters.",
            help="Print a listing of all a user's characters.",
            brief="Print char list."
    )
    async def list(self,
                   ctx: discord.ApplicationContext,
                   user_id: discord.Option(str,
                                           description="check a specific user's characters",
                                           required=False)):
        """List a user's characters.

        Attempt to produce a listing of all character's for a given user. By default assumes
            you want the user that sent the message's characters. A user id may be supplied to
            list characters for another user.

        Parameters
        ----------
        ctx     The discord context object for the command
        user_id The user's discord user id
        """
        try:
            char_list = get_chars(ctx.author.id)
        except FileNotFoundError:
            await ctx.respond("You have no characters!")
            return
        data = []
        headers = ["Name", "Class", "Level"]
        for c in char_list:
            data.append([c.name, c._bt_class.name, str(c.level)])
        out_str = tabulate(data, headers, showindex="always",
                           tablefmt="grid", numalign="right",
                           stralign="left")
        await ctx.respond(f"```{out_str}```")

    @character_command_group.command(
            description="Delete a character.",
            help="Delete a character.",
            brief="Delete a character.",
            aliases=["remove", "del"]
            )
    async def delete(self,
                     ctx: discord.ApplicationContext,
                     name: discord.Option(str, description='Which character do you want to delete?',
                                          required=True)):
        """Delete a character.

        Attempt to delete a character for a given user. By default will look in
        ./rpg-data/characters/ctx.author.id/<name>
        for the character file. If a file with the correct name is found
        it is removed via `del_char()`

        Parameters
        ----------
        ctx     The discord context object for the command
        name    The character name to remove
        """
        try:
            deleted_char = del_char(ctx.author.id, name)
            await ctx.respond(f"Deleted character for {ctx.author.mention}"
                              f" named {deleted_char.name}\n"
                              f"{deleted_char}")
        except FileNotFoundError:
            await ctx.respond("Failed to delete character!")

    @character_command_group.command(
        description="Check which character is active.",
        help="Check which character is active.",
        brief="Get your active character.",
        aliases=["active"]
    )
    async def whoami(self, ctx: discord.ApplicationContext):
        """Print out the current active character.

        Looks in ./rpg-data/active/ for a file with the user's ID (ctx.author.id).
        If none is found a FileNotFoundError will be raised.

        Parameters
        ----------
        ctx The discord context object for the command"""
        try:
            active_char = get_active(ctx.author.id)
            await ctx.respond("```"
                              "Your active character\n"
                              "---------------------\n"
                              f"{active_char}```")
        except FileNotFoundError:
            await ctx.respond("```You don't have any characters!"
                              " Use /character create first```")
        pass

    @character_command_group.command(
        description="Set your active character.",
        help="Set your active character. You can get a "\
             "list of your characters with /character list",
        brief="Set your active character.",
        aliases=["set_active"]
    )
    async def set(self, ctx: discord.ApplicationContext,
                  char: discord.Option(str,
                                       description="Enter the name of the character you wish to swap to.",
                                       required=True)):
        """Set the user's active character.

        Parameters
        ----------
        ctx     The discord context object for the command
        name    The name of the character to make active"""
        try:
            active_char = get_active(ctx.author.id)
            loaded_char = load_char(ctx.author.id, char)
            set_active(ctx.author.id, loaded_char)
            new_active = get_active(ctx.author.id)
            await ctx.respond(f"Changing active character for {ctx.author.mention}\n"
                              f"```Old\n----\n{active_char}\n\nNew\n----\n{new_active}```")
        except Exception as e:
            raise Exception(e)

    @character_command_group.command(
        description="Check your inventory.",
        help="List the contents of your inventory out.",
        brief="What in the bag?"
    )
    async def inventory(self, ctx: discord.ApplicationContext):

        out_str = "```Inventory Contents (item, # held)"\
                  "----------------------------------"\
                  f"{get_inv_contents(ctx.author.id)}"
        await ctx.respond(out_str)


def create_char(user_id: str, name: str, c_name: str) -> character.Character:
    dir_path, char_file = get_paths(user_id, name)
    f = None
    try:
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
    except FileExistsError:
        raise FileExistsError("tried to create active and failed")
    char_count = len(get_chars(user_id))
    if char_count >= config.data['max_characters']:
        raise ValueError("Too many characters!")
    try:
        if os.path.isfile(char_file):
            print("loaded char")
            with open(char_file, 'rb') as f:
                loaded_char = pickle.load(f)
                f.close()
                return loaded_char
        else:
            class_choice = get_class(c_name)
            ret = character.Character(name=name, class_choice=class_choice)
            save_char(user_id, ret)
            if char_count == 0:
                set_active(user_id, ret)
            return ret
    except FileNotFoundError as e:
        raise FileNotFoundError(f"file problem on character creation {e}")
    except Exception:
        raise Exception("problem in character creation")


def get_chars(user_id: str):
    dir_path, _ = get_paths(user_id, None)
    chars = []
    file = None
    try:
        files = os.listdir(dir_path)
        for file_name in files:
            file_path = os.path.join(dir_path, file_name)
            if os.path.isfile(file_path) and file_name.endswith(config.data['file_ext']):
                with open(file_path, 'rb') as file:
                    loaded_data = pickle.load(file)
                    chars.append(loaded_data)
                    file.close()
        return chars
    except FileNotFoundError:
        raise FileNotFoundError("problem checking char list")


def save_char(user_id: str, char: character.Character):
    _, char_file = get_paths(user_id, char.name)
    f = None
    try:  # this can probably be one block
        if not os.path.isfile(char_file):
            with open(char_file, 'w+b') as f:
                pickle.dump(char, f)
                f.close()
        else:
            with open(char_file, 'wb') as f:
                pickle.dump(char, f)
                f.close()
    except FileNotFoundError:
        raise FileNotFoundError("file problem on character save")


def del_char(user_id: str, char: str) -> character.Character:
    if isinstance(char, character.Character):
        name = char.name
    else:
        name = char
    _, char_file = get_paths(user_id, name)
    try:
        loaded = load_char(user_id, name)
        os.remove(char_file)
        return loaded
    except FileNotFoundError as e:
        raise FileNotFoundError(f"could not remove character file {char_file} ({e})")


def load_char(user_id: str, name: str) -> character.Character:
    _, char_file = get_paths(user_id, name)
    try:
        with open(char_file, 'rb') as f:
            loaded_char = pickle.load(f)
            f.close()
        return loaded_char
    except FileNotFoundError:
        raise FileNotFoundError("Character not found!")


def set_active(user_id: str, c: character.Character, choice: int = -1):
    active_c = None
    f = None
    active_file = f"./{config.data['data_dir']}/" \
                  f"{config.data['active_dir']}/" \
                  f"{user_id}.{config.data['file_ext']}"
    output_data = ((0, c.name, user_id))

    try:
        active_c = get_active(user_id)
    except FileNotFoundError:
        active_c = None
    try:
        with open(active_file, 'w+b') as f:
            pickle.dump(output_data, f)
            f.close()
    except FileExistsError:
        raise FileExistsError("could not set active character")
    return active_c


def get_active(user_id: str) -> character.Character:
    path = f"./{config.data['data_dir']}/{config.data['active_dir']}"
    active_path = f"{path}/{user_id}.{config.data['file_ext']}"
    try:
        if os.path.isfile(active_path):
            with open(active_path, 'rb') as f:
                active_char = pickle.load(f)
                c = load_char(user_id, active_char[1])
                return c
        else:
            raise FileNotFoundError("no active character!")
    except FileNotFoundError:
        raise FileNotFoundError("could not get active character")


def get_char_count(user_id: int = 0):
    return len(get_chars(user_id))


def get_class(name: str) -> character.bt_Class:
    match name:
        case 'warrior':
            return character.Warrior()
        case 'rogue':
            return character.Rogue()
        case 'wizard':
            return character.Wizard()
        case 'trader':
            return character.Trader()
        case 'paladin':
            return character.Paladin()
        case 'villager':
            return character.Villager()
        case _:
            raise TypeError("invalid class")


def get_inv_contents(user_id: str) -> str:
    """Return a string with inventory contents and the # of each item."""
    active_char = get_active(user_id)
    count = Counter(active_char.inventory)
    out_str = ""
    for v in count.keys():
        out_str += f"{v.name}, {count[v]}\n"
    return out_str[0:len(out_str)-1]


def get_paths(user_id: str, name: str):
    dir_path = f"./{config.data['data_dir']}/{config.data['char_dir']}/{user_id}"
    char_file = f"{dir_path}/{name}.{config.data['file_ext']}"
    return (dir_path, char_file)


def setup(bot):
    bot.add_cog(character_Commands(bot))
