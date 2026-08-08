import os ,asyncio ,discord
from discord.ext import commands
from utils.Tools import *
import psutil
import platform

class anti(discord.ui.View):
    def __init__(self, bot,ctx):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.bot = bot
        self.message = None 

    async def on_timeout(self):
        for child in self.children:  
            child.disabled = True
        await self.message.edit(view=self) 
      
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in [926831289649201213]:
            await interaction.response.send_message("Opps , Looks like you are not the author of the command .", ephemeral=True)
            return False
        return True        
    @discord.ui.button(label="General", custom_id='yes', style=discord.ButtonStyle.green,disabled=True)
    async def png(self, interaction, button):
        embed = discord.Embed(color=0x2f3136)
        embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
        textchannel = sum(len(guild.text_channels)for guild in self.bot.guilds)
        voicechannel = sum(len(guild.voice_channels) for guild in self.bot.guilds)
        categorichannel = sum(len(guild.categories) for guild in self.bot.guilds)
        total = textchannel + voicechannel + categorichannel
        embed.add_field(name="** ◇ Bot Information**", value=f"**Total Guilds**: {len(self.bot.guilds)}\n**Users**: {sum(g.member_count for g in self.bot.guilds if g.member_count != None)}\n**Ping**: {round(self.bot.latency * 1000, 2)}ms\n**Shards**: {self.bot.shard_count}\n**Channels**: {total}", inline=False)
        #embed.add_field(name="**__Module Information__**", value=f"**Python Version**: {platform.python_version()}\n**Operating System**: {platform.system()}\n**System Architecture**: {platform.architecture()[0]}\n**discord.py Version**: {discord.__version__}\n**psutil Version**: {psutil.__version__}",inline=False)
      
        for child in self.children:  
          child.disabled = False
          child.style=discord.ButtonStyle.grey
        button.disabled = True
        button.style=discord.ButtonStyle.green
        await interaction.response.edit_message(embed=embed,view=self)


    @discord.ui.button(label="System", custom_id='stop', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction, button):
        embed = discord.Embed(color=0x2f3136)
        embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
        cpu_info = psutil.cpu_freq()
        cpu_free = psutil.cpu_percent(interval=1, percpu=True)
        avg_cpu_free = sum(cpu_free) / len(cpu_free)
        cpu_fr = f"{avg_cpu_free:.2f}%"
        embed.add_field(name="** ◇ CPU Information**", value=f"**Cpu Model**: {platform.processor()}\n**Cpu Speed**: {cpu_info.current} MHz\n**Cpu Core**: {psutil.cpu_count(logical=False)}\n**Cpu Usage**: {psutil.cpu_percent()}%\n**Cpu Free**: {cpu_fr}\n**Available Parallelism**: {psutil.cpu_count()}", inline=False)
        mem = psutil.virtual_memory()
        embed.add_field(name="** ◇ Memory Information**", value=f"**Total Memory**: {mem.total // (1024 ** 3)} GB\n**Used Memory**: {mem.used // (1024 ** 3)} GB\n**Free Memory**: {mem.free // (1024 ** 3)} GB",inline=False)
        for child in self.children:  
          child.disabled = False
          child.style=discord.ButtonStyle.grey
        button.disabled = True
        button.style=discord.ButtonStyle.green
        await interaction.response.edit_message(embed=embed,view=self)
        
    @discord.ui.button(label="Module",style=discord.ButtonStyle.grey)
    async def amanop(self, interaction, button):
      embed = discord.Embed(color=0x2f3136)
      embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
      embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)

  
  

      embed.add_field(name="** ◇ Module Information**", value=f"**Python Version**: {platform.python_version()}\n**Operating System**: {platform.system()}\n**System Architecture**: {platform.architecture()[0]}\n**discord.py Version**: {discord.__version__}\n**psutil Version**: {psutil.__version__}",inline=False)

      
      for child in self.children:
        child.disabled = False
        child.style=discord.ButtonStyle.grey
      button.style=discord.ButtonStyle.green
      button.disabled = True
      await interaction.response.edit_message(embed=embed,view=self)
      
        
      
class Stats(commands.Cog):
    def __init__(self, bot):
      self.bot = bot
      self.client = bot  
    @commands.hybrid_command(name="statistics",aliases=["st", "stats"],usage="stats",with_app_command = True)
    @blacklist_check()
    @ignore_check()
    async def _stats(self, ctx):
      view = anti(self.bot,ctx)
      embed = discord.Embed(color=0x2f3136)
      embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
      embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
      textchannel = sum(len(guild.text_channels)for guild in self.bot.guilds)
      voicechannel = sum(len(guild.voice_channels) for guild in self.bot.guilds)
      categorichannel = sum(len(guild.categories) for guild in self.bot.guilds)
      total = textchannel + voicechannel + categorichannel
      embed.add_field(name="** ◇ Bot Information**", value=f"**Total Guilds**: {len(self.bot.guilds)}\n**Users**: {sum(g.member_count for g in self.bot.guilds if g.member_count != None)}\n**Ping**: {round(self.bot.latency * 1000, 2)}ms\n**Shards**: {self.bot.shard_count}\n**Channels**: {total}", inline=False)
      
      b= await ctx.send(embed=embed,view=view)
      view.message = b
    