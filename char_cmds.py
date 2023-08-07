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
        if get_char_count(ctx.author.id) < 10:
            if get_char_count(ctx.author.id) == 0:
                os.makedirs(f"/{ctx.author.id}/")
            if os.path.isfile(f"{ctx.author.id}/{name}"):
                await ctx.respond("That character already exists!")
                with open(f"./{ctx.author.id}/{name}", "rb") as f:
                    new_char = pickle.load(f)
                print(new_char)
                return new_char
            my_class = _get_class(c_name)
            new_char = character.Character(name=name, class_choice=my_class)
            file_name = f"{ctx.author.id}/{name}"
            with open(f"./{file_name}", "w+b") as f:
                pickle.dump(new_char, f)
            f.close()
            await ctx.respond(str(new_char))
            print(new_char)
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
