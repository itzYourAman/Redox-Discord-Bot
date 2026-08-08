import discord
from discord.ext import commands


class ticket1(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  """Ticket commands"""

  def help_custom(self):
    emoji = '<:icon_ticket:1255056665699422316>'
    label = "Ticket"
    description = "Show You Ticket Commands"
    return emoji, label, description

  @commands.group()
  async def __Ticket__(self, ctx: commands.Context):
    """`ticket` , `ticket setup` , `ticket delete`, `ticket edit`, `ticket info`, `ticket reopen`
"""
