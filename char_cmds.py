from discord.ext import commands
from discord import SlashCommandGroup
import discord
import character
import os
import config
import pickle


class character_Commands(commands.Cog):
    character_command_group = SlashCommandGroup('character',
                                                'Commands for interacting '
                                                'with your character(s).')

    def __init__(self, bot):
        self.bot = bot

    def get_class_types(ctx: discord.AutocompleteContext):
        return ['warrior', 'rogue', 'wizard', 'villager', 'paladin', 'trader']

    @commands.slash_command(
            description="Create a new character.",
            help="Create a new character.",
            brief="Create a new character.",
            aliases=["make", "new"],
            guild_ids=[1136708527797309500]
            )
    async def create(self,
                     ctx: discord.ApplicationContext,
                     name: discord.Option(str, description='Enter a name for your character.', required=True),
                     c_name: discord.Option(str, description="choose your class",
                                            autocomplete=discord.utils.basic_autocomplete(get_class_types))):
        try:
            new_char = create_char(ctx.author.id, name, c_name)
            saved_char = save_char(new_char)
        except FileNotFoundError:
            await ctx.respond("Failed to create a character. Please try again.")
        assert new_char == saved_char


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
            with open(char_file, 'rb') as f:
                return pickle.load(f)
        else:
            import pdb
            pdb.set_trace()
            class_choice = get_class(c_name)
            ret = character.Character(name=name, class_choice=class_choice)
            print(ret)
            return ret
    except FileNotFoundError:
        raise FileNotFoundError("file problem on character creation")
    except Exception:
        raise Exception("problem in character creation")
    finally:
        if f is not None:
            f.close()


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
    finally:
        if file is not None:
            file.close()


def save_char(char: character.Character, user_id: str):
    _, char_file = get_paths(user_id, char.name)
    try:
        with open(char_file, 'wb') as f:
            pickle.dump(char, f)
    except FileNotFoundError:
        raise FileNotFoundError("file problem on character save")
    finally:
        f.close()


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
    if len(get_chars(user_id) == 0):
        output_data = ((0, c.name, user_id))
        active_file = f"./config.data['active_dir']/{user_id}"
        try:
            with open(active_file, 'wb+') as f:
                pickle.dump(output_data, f)
        except FileExistsError:
            raise FileExistsError("could not set active character")
        finally:
            f.close()
    if isinstance(choice, int):
        # logic for if user sends an int
        pass
    if isinstance(choice, str):
        # logic for if user sends an it
        pass
    if isinstance(choice, character.Character):
        # internal use
        pass
    raise TypeError("invalid type passed for set active")


def get_active(user_id: str) -> character.Character:
    path = f"./{config.config['data_dir']}/{config.config['active_dir']}"
    active_path = f"{path}/{user_id}.{config.data['file_ext']}"
    try:
        if os.isfile(active_path):
            with open(active_path, 'rb') as f:
                active_char = pickle.load(f)
            return active_char
        else:
            raise FileNotFoundError("no active character!")
    except FileNotFoundError:
        raise FileNotFoundError("could not get active character")


def setup(bot):
    bot.add_cog(character_Commands(bot))


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


def get_paths(user_id: str, name: str):
    dir_path = f"./{config.data['data_dir']}/{config.data['char_dir']}/{user_id}/"
    char_file = f"{dir_path}/{name}.{config.data['file_ext']}"
    return (dir_path, char_file)
