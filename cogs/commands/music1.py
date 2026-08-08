import discord
from discord.ext import commands


class music1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Music commands"""
  
    def help_custom(self):
		      emoji = '<:icons_Music:1255056548137406616>'
		      label = "Music"
		      description = "Show You Commands Of Music"
		      return emoji, label, description

    @commands.group()
    async def __Music__(self, ctx: commands.Context):
        """`connect` , `play` , `queue` , `nowplaying` , `stop`, `pause` , `move` , `shuffle` , `resume` , `skip` , `clear` , `disconnect` , `seek` , `pull` , `volume` , `bassboost enable` , `bassboost disable` , `filter` , `filter daycore enable` , `filter daycore disable` , `filter speed enable` , `filter speed disable` , `filter slowmode enable` , `filter slowmode disable` , `filter lofi enable` , `filter lofi disable` , `filter nightcore enable` , `filter nightcore disable` , `filter drunk enable` , `filter drunk disable` , `filter quick enable` , `filter quick disable` , `filter slowmode enable` , `filter slowmode disable` , `filter reset`
        """