import discord
from discord.ext import commands


class mod1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Moderation Commands"""
  
    def help_custom(self):
		      emoji = '<:moderation_icon:1255056464825815092>'
		      label = "Moderation"
		      description = "Show You Commands Of Moderation"
		      return emoji, label, description

    @commands.group()
    async def __Moderation__(self, ctx: commands.Context):
        """`mute` , `unmute` , `kick` , `warn` , `ban` , `unban` , `unbanall` , `clone` , `nick` , `slowmode` ,  `unslowmode` , `clear` , `clear all` , `clear bots` , `clear embeds` , `clear files` , `clear mentions` , `clear images` , `clear contains` , `clear reactions` , `clear user` , `clear emoji` , `nuke` , `lock` , `unlock` , `hide` , `unhide` , `hideall` , `unhideall` , `audit` , `role` , `role temp` , `role remove` , `role delete` , `role create` , `role rename` , `role humans` , `role bots` , `role all` , `role status` , `role cancel` , `removerole humans` , `removerole bots` , `removerole all` , `removerole status` , `removerole cancel` , `enlarge` , `Gban add` , `gban remove` , `gban show` , `gban role` , `gban reset` , `roleicon`, `steal` , `deleteemoji` , `deletesticker` , `addsticker`"""