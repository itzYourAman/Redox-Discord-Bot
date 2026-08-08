import discord
from discord.ext import commands


class fun1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Fun Commands"""
  
    def help_custom(self):
		      emoji = '<:paint_icons:1255059064644177950>'
		      label = "Fun"
		      description = "Show You Commands Of Fun"
		      return emoji, label, description

    @commands.group()
    async def __Fun__(self, ctx: commands.Context):
        """` tickle` , `kiss` , `hug` , `slap` , `pat` , `feed` , `pet` , `howgay` , `slots` , `meme` , `cat` , `iplookup` , `nitro`, `chess`, `akinator` , `hangman` , `typerace` , `rps` , `reaction` , `tick-tack-toe` , `wordle` , `2048` , `memory-game` , `number-slider` , `battleship` , `country-guesser`"""