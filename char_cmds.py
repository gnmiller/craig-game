from discord.ext import commands
import discord
import character
import os
import pickle


class character_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_class_types(ctx: discord.AutocompleteContext):
        return ['warrior', 'rogue', 'wizard', 'villager', 'paladin', 'trader']

    @commands.slash_command(
            description="Create a new character.",
            help="Create a new character.",
            brief="Create a new character.",
            aliases=["create_char", "new_char"],
            guild_ids=[1136708527797309500]
            )
    async def make_char(self,
                        ctx: discord.ApplicationContext,
                        name: str,
                        c_name: discord.Option(str, description="choose your class", autocomplete=discord.utils.basic_autocomplete(get_class_types))):
        dir_path = f"./characters/{ctx.author.id}/"
        char_file = f"{dir_path}/{name}"
        if get_char_count(dir_path) < 10:
            if get_char_count(dir_path) == 0:
                os.makedirs(dir_path)
            if os.path.isfile(char_file):
                await ctx.respond("That character already exists!")
                with open(char_file, "rb") as f:
                    new_char = pickle.load(f)
                return new_char
            my_class = _get_class(c_name)
            new_char = character.Character(name=name, class_choice=my_class)
            with open(char_file, "w+b") as f:
                pickle.dump(new_char, f)
            f.close()
            await ctx.respond(f"New character named {name} created!\n{str(new_char)}")
            return new_char
        else:
            await ctx.respond("you have too many characters buddy!")
            return None


def setup(bot):
    bot.add_cog(character_Commands(bot))


def get_char_count(user_id: int = 0):
    path = f"./{user_id}/"
    count = 0
    try:
        for p in os.listdir(path):
            if os.path.isfile(os.path.join(path, p)):
                count += 1
        return count
    except FileNotFoundError:
        return 0


def _get_class(name: str) -> character.bt_Class:
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
