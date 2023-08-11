from collections import Counter

import discord
import fish
from char_cmds import get_active
from char_cmds import save_char
from discord import SlashCommandGroup
from discord.ext import commands


class Fishing(commands.Cog):
    fishing_command_group = SlashCommandGroup(name='fishing',
                                              description="The greatest of all hobbies.")

    def __init__(self, bot):
        """
        Constructs the Fishing cog for all fishing related commands.

        This cog interacts with the file structure defined in config.data and
        utilizes the save/load functionality defined in `char_cmds`.
        """
        self.bot = bot

    def get_fishing_holes(ctx: discord.AutocompleteContext):
        """
        Return a list of valid fishing pools based on the data available in `fish`

        Checks the fish.fishing_pools list for FishingPool objects, grabs
        their name, and constructs a list from the found objects. Used in
        the `catch` command for auto-filling the possible options.

        Parameters
        ----------
        ctx     Context object provided by py-cord.
        """
        out = []
        for n in fish.fishing_pools:
            out.append(f"{n.name}")
        return out

    @fishing_command_group.command(
        description="Go fishin'",
        help="Catch some fishies"
    )
    @commands.cooldown(
        rate=1,
        per=15,
        type=discord.ext.commands.BucketType.user
    )
    async def catch(self,
                    ctx: discord.ApplicationContext,
                    where: discord.Option(str,
                                          description="Where do you want to go fishing?",
                                          autocomplete=discord.utils.basic_autocomplete(get_fishing_holes))):
        """
        Go fishing!

        Attempt to catch some Fish from a FishingPool. The number of fish
        caught is dependent on the character's Luck stat currently. Fishing
        rod's and other bonuses NYI. Calls the `go_fishing()` function to
        generate what fish and how many were caught. Value of each fish is
        summed and then used to determine how much experience the character
        receives.

        Parameters
        ----------
        ctx     The discord context object for the command

        where   Which FishingPool you want to fish in.
        """
        pool = None
        for n in fish.fishing_pools:
            if where == n.name:
                pool = n
                break
        if pool is None:
            raise ValueError("no fishing pool!")
        me = get_active(ctx.author.id)
        if me.level < n.min_level:
            await ctx.respond("You are too low level for this area. Try"
                              " somewhere easier first.")
            return
        feesh = pool.go_fishing(me.luck, None)
        feesh_d = Counter(feesh)
        exp_gained = 0
        out_str = "```You caught\n--------\n"
        for k, v in feesh_d.items():
            out_str += f"{k.name} x{feesh_d[k]} ({k.value*feesh_d[k]} 💰)\n"
            exp_gained += k.value*feesh_d[k]
        for f in feesh:
            me.inventory.add_item(f)
        out_str += f"You gained {int(exp_gained/10)} experience!\n"
        me.gain_exp(int(exp_gained/6.5))
        save_char(ctx.author.id, me)
        await ctx.respond(f"{out_str}```")

    @fishing_command_group.command(
        description="Sell your fish.",
    )
    @commands.cooldown(rate=3, per=10,
                       type=discord.ext.commands.BucketType.user)
    async def sell(self,
                   ctx: discord.ApplicationContext,
                   what: str = "all"):
        """
        Sell off the fish you caught.

        Inspects the character's backpack and looks for Fish items. Any that
        are found are added to a list. Items in that list are then iterated
        over and passed into `Inventory.del_item()` to remove them from the
        inventory.

        This function may be better suited within `character.Inventory`
        and would then become something like
            /inventory sell fish or /inventory sell fish all

        Parameters
        ----------
        ctx     The discord context object for the command

        what    NYI -- Eventually a selector for certain objects to sell.
        """
        me = get_active(ctx.author.id)
        to_sell = []
        for f in me.inventory:
            if isinstance(f, fish.Fish):
                to_sell.append(f)
        gold_gained = 0
        fish_sold = 0
        for s in to_sell:
            fish_sold += 1
            gold_gained += s.value
        for s in to_sell:
            me.inventory.del_item(s)
        me.inventory.change_gold(gold_gained)
        save_char(ctx.author.id, me)
        out_str = f"```You sold {fish_sold} fish and"\
                  f" gained {gold_gained} gold!```"
        await ctx.respond(out_str)

    @fishing_command_group.command(
        description="Check where you can fish."
    )
    @commands.cooldown(rate=1, per=120,
                       type=discord.ext.commands.BucketType.channel)
    async def holes(self, ctx):
        """
        Produce a list of valid FishingPools a user could fish in.
        """
        out_str = "```Available Fishing Holes\n"\
                  "-----------------------\n"
        for n in fish.fishing_pools:
            out_str += f"{n.name} (Lv. {n.min_level})\n"
        out_str = out_str[0:len(out_str)-1]+"```"
        await ctx.respond(out_str)

    @catch.error
    async def catch_error(self, ctx, error):
        """
        Catch and report errors within the Fishing commands.
        """
        if isinstance(error, commands.CommandOnCooldown):
            msg = "```You cannot go use that command again so soon.\n"\
                  f"Please wait {error.retry_after:.2f} more seconds.```"
            await ctx.respond(msg)
            return
        if isinstance(error, discord.errors.ApplicationCommandInvokeError):
            if "no fishing pool" in str(error):
                msg = "```That is not a valid fishing pool choice!```"
                await ctx.respond(msg)
        else:
            raise error
