import discord
from discord.ext import commands


class logging1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Logging Commands"""
  
    def help_custom(self):
		      emoji = '<:logging:1255056908218400920>'
		      label = "Logging"
		      description = "Show You Commands Of Logging"
		      return emoji, label, description

    @commands.group()
    async def __Logging__(self, ctx: commands.Context):
        """`logging`,`logreset` ,`logconfig` ,`msglog` , `memberlog` , `serverlog` , `channellog` , `rolelog` , `modlog` ,`logall`"""