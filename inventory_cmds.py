from collections import Counter

import character
import discord
from char_cmds import get_active
from discord import SlashCommandGroup
from discord.ext import commands


class inventoryCommands(commands.Cog):
    """
    Inventory Commands Cog
    ----------------------

    Holds commands for interacting with a user's inventory such as listing,
    selling (NYI), and equipping items (NYI).
    """
    inventory_command_group = SlashCommandGroup(name='inventory',
                                                description="Commands for interacting "
                                                "with your character's bags.")

    def __init__(self, bot):
        """
        Construct the cog for Inventory commands.
        """
        self.bot = bot

    @inventory_command_group.command(
        description="Check your inventory.",
        help="List the contents of your inventory out.",
        brief="What in the bag?"
    )
    async def list(self, ctx: discord.ApplicationContext):
        """
        Print out the contents of the character's inventory.

        Parameters
        ----------
        ctx     The discord context object for the command
        """
        me = get_active(ctx.author.id)
        if me.inventory.is_empty:
            await ctx.respond("```Your inventory is empty!```")
            return
        out_str = "```Inventory Contents (item, # held)\n"\
                  "----------------------------------\n"\
                  f"{get_inv_contents(me)}"
        out_str += "```"
        await ctx.respond(out_str)
        return


def get_inv_contents(c: character.Character) -> str:
    """
    Return a string with inventory contents and the # of each item.

    Inspects the inventory contents for the user's active character and returns
    them as a string 'item name, item count'

    Parameters
    ----------
    user_id     The user's Discord ID (eg ctx.author.id
    """
    count = Counter(c.inventory)
    out_str = ""
    for v in count.keys():
        out_str += f"{v.name}, {count[v]}\n"
    return out_str[0:len(out_str)-1]
