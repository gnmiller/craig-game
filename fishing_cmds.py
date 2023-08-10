import discord
from discord.ext import commands
from discord import SlashCommandGroup


class Fishing(commands.Cog):
    fishing_command_group = SlashCommandGroup(name='fishing',
                                              description="The greatest of all hobbies.")

    def __init__(self, bot):
        self.bot = bot