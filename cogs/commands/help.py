import discord
from discord.ext import commands
from difflib import get_close_matches
import datetime
from contextlib import suppress
from core.Cog import Cog
from utils.Tools import *
import time
import datetime
from typing import *
from utils import *
import json
from utils import help as vhelp
from utils import Paginator,FieldPagePaginator

from core import Cog, Redox
start_time = time.time()
client = Redox()
color = 0x41eeee


def datetime_to_seconds(thing: datetime.datetime):
    current_time = datetime.datetime.fromtimestamp(time.time())
    return round(
        round(time.time()) +
        (current_time - thing.replace(tzinfo=None)).total_seconds())




class HelpCommand(commands.HelpCommand):


  async def on_help_command_error(self, ctx, error):
    damn = [
      commands.CommandOnCooldown, commands.CommandNotFound,
      discord.HTTPException, commands.CommandInvokeError
    ]
    if not type(error) in damn:
      await self.context.reply(f"Unknown Error Occurred\n{error.original}",
                               mention_author=False)
    else:
      if type(error) == commands.CommandOnCooldown:
        return

        return await super().on_help_command_error(ctx, error)  


  async def command_not_found(self, string: str) -> None:
    with open('data/json/blacklist.json', 'r', encoding="utf-8") as f:
      bled = json.load(f)
    data = getIgnore(self.context.guild.id)
    ch = data["channel"]
    iuser = data["user"]
    buser = data["bypassuser"]
    blsc = discord.Embed(description="You are blacklisted from using my commannds.\nreason could be excessive use or spamming commands\nJoin our [Support Server](https://discord.com/invite/CCYef4Ad4M) to appeal .", color=discord.Colour(0x2f3136))
    embed = discord.Embed(description="This Channel is in ignored channel list try my commands in another channel .", color=discord.Colour(0x2f3136))
    ign = discord.Embed(description=f"You are set as a ignored users for {self.context.guild.name} .\nTry my commands or modules in another guild .", color=discord.Colour(0x2f3136))

    if str(self.context.author.id) in bled["ids"]:
      await self.context.send(embed=blsc,delete_after=10)
      return

    if str(self.context.author.id) in iuser and str(self.context.author.id) not in buser: 
      await self.context.send(embed=ign,delete_after=10)
      return

   # if str(self.context.channel.id) in ch and str(self.context.author.id) not in buser:
    #  await self.context.send(embed=embed,delete_after=10)
     # return
    else:

      if string in ("security", "anti", "antinuke"):
        cog = self.context.bot.get_cog("Antinuke")
        with suppress(discord.HTTPException):
          await self.send_cog_help(cog)
      else:
        msg = f"Command `{string}` is not found...\n"
        hacker = await self.context.bot.fetch_user(246469891761111051)
        cmds = (str(cmd) for cmd in self.context.bot.walk_commands())
        mtchs = get_close_matches(string, cmds)
        if mtchs:
          for okaay, okay in enumerate(mtchs, start=1):
            msg += f"Did You Mean: \n`[{okaay}]` $`{okay}`\n"
        return msg


  async def send_bot_help(self, mapping):
    with open('data/json/blacklist.json', 'r', encoding="utf-8") as f:
      bled = json.load(f)
    data = getIgnore(self.context.guild.id)
    ch = data["channel"]
    iuser = data["user"]
    buser = data["bypassuser"]
    bl = discord.Embed(description="You are blacklisted from using my commannds.\nreason could be excessive use or spamming commands\nJoin our [Support Server](https://discord.com/invite/CCYef4Ad4M) to appeal .", color=discord.Colour(0x2f3136))
    embed = discord.Embed(description="This Channel is in ignored channel list try my commands in another channel .", color=discord.Colour(0x2f3136))
    ign = discord.Embed(description=f"You are set as a ignored users for {self.context.guild.name} .\nTry my commands or modules in another guild .", color=discord.Colour(0x2f3136))

    if str(self.context.author.id) in bled["ids"]:
      await self.context.send(embed=bl,delete_after=10)
      return 

    if str(self.context.author.id) in iuser and str(self.context.author.id) not in buser: 
      await self.context.send(embed=ign,delete_after=10)
      return 

    if str(self.context.channel.id) in ch and str(self.context.author.id) not in buser:
      await self.context.send(embed=embed,delete_after=10)
      return

    data = getConfig(self.context.guild.id)
    prefix = data["prefix"]    
    filtered = await self.filter_commands(self.context.bot.walk_commands(),sort=True)

    embed = discord.Embed(
      title="**Help Command Overview **:",
      description=
      f"**◇ Prefix for this server is `{prefix}`\n◇  Total Commands: {len(set(self.context.bot.walk_commands()))} | Usable by you (here): {len(set(filtered))}\n◇ Type `{prefix}help <command | module>` for more info.**\n```    <> - Required | [] - Optional``` ",
      color= 0x2C2F33)
    embed.set_thumbnail(url=self.context.bot.user.display_avatar.url)

    embed.set_footer(
      text="Made with 💖 by the Redox development team",
      icon_url="https://storage.googleapis.com/replit/images/1697368882447_77d962c64daa5462b2333fa30dc91247.gif")

    embed.add_field(name="◇ **Modules**",
                    value="""**<:antinuke:1255056314212548743> Antinuke\n<:icon_giveaway:1255060336684302337> Giveaway\n<:icons_Music:1255056548137406616> Music\n<:moderation_icon:1255056464825815092> Moderation\n<:icon_ticket:1255056665699422316> Ticket\n<:icon_Extra:1255056804304523354> Extra\n<:icons_boost:1255057209490931823> BoostMsg\n<:logging:1255056908218400920> Logging\n<:icon_welcome:1255057382392856576> Welcome\n<:raidmod:1255059548209811466> Raidmode\n<:icon_dots:1255069606272565310>Server\n<:paint_icons:1255059064644177950> Fun\n<:earth:1255057931318067230> General\n<:icons_voice:1255058141477994560> Voice\n<:merox_vcroles:1138834073884827779> VcRoles**""",#\n<:vanity:1138833902002241547> : Vanity roles""",
                    inline=False)
    embed.add_field(name="**◇ Links**",value="**[Invite Me](https://discord.com/oauth2/authorize?client_id=1126351590064930847&permissions=1239031351480&scope=bot) | [Support Server](https://discord.com/invite/5SUKAB7n93)**",inline=False)
      
    embed.set_author(name=self.context.author.name,
                     icon_url=self.context.author.display_avatar.url)


    invite_button = discord.ui.Button(
        style=discord.ButtonStyle.link,label="Invite Me",url="https://discord.com/oauth2/authorize?client_id=1126351590064930847&permissions=1239031351480&scope=bot")
    support_button = discord.ui.Button(style=discord.ButtonStyle.link,label="Support Server",url="https://discord.com/invite/5SUKAB7n93")
    Vote_button = discord.ui.Button(style=discord.ButtonStyle.link,label="Vote Me",url="https://discord.com/invite/CCYef4Ad4M")    

    view = vhelp.View(mapping=mapping, ctx=self.context, homeembed=embed, ui=0)
    view.add_item(invite_button)
    view.add_item(support_button)
    bo= await self.context.send(embed=embed, mention_author=True, view=view)
    view.message= bo
    view.emb = embed
  async def send_command_help(self, command):
    with open('data/json/blacklist.json', 'r', encoding="utf-8") as f:
      bled = json.load(f)
    data = getIgnore(self.context.guild.id)
    ch = data["channel"]
    iuser = data["user"]
    buser = data["bypassuser"]
    bl = discord.Embed(description="You are blacklisted from using my commannds.\nreason could be excessive use or spamming commands\nJoin our [Support Server](https://discord.com/invite/CCYef4Ad4M) to appeal .", color=discord.Colour(0x2f3136))
    embed = discord.Embed(description="This Channel is in ignored channel list try my commands in another channel .", color=discord.Colour(0x2f3136))
    ign = discord.Embed(description=f"You are set as a ignored users for {self.context.guild.name} .\nTry my commands or modules in another guild .", color=discord.Colour(0x2f3136))

    if str(self.context.author.id) in bled["ids"]:
      await self.context.send(embed=bl,delete_after=10)
      return 

    if str(self.context.author.id) in iuser and str(self.context.author.id) not in buser: 
      await self.context.send(embed=ign,delete_after=10)
      return 

   # if str(self.context.channel.id) in ch and str(self.context.author.id) not in buser:
    #  await self.context.send(embed=embed,delete_after=10)
     # return

    else:
      hacker = f">>> {command.help}" if command.help else '>>> No Help Provided...'
      embed = discord.Embed(
        description=
        f"""```yaml\n- [] = optional argument\n- <> = required argument\n- Do NOT Type These When Using Commands !```\n{hacker}""",
        color=color)
      alias = ' | '.join(command.aliases)

      embed.add_field(name="**Aliases**",
                      value=f"{alias}" if command.aliases else "No Aliases",
                      inline=False)
      embed.add_field(name="**Usage**",
                      value=f"`{self.context.prefix}{command.signature}`\n")
      embed.set_author(name=f"{command.cog.qualified_name.title()}",
                       icon_url=self.context.bot.user.display_avatar.url)
      await self.context.reply(embed=embed, mention_author=False)







  def get_command_signature(self, command: commands.Command) -> str:
    parent = command.full_parent_name
    if len(command.aliases) > 0:
      aliases = ' | '.join(command.aliases)
      fmt = f'[{command.name} | {aliases}]'
      if parent:
        fmt = f'{parent}'
      alias = f'[{command.name} | {aliases}]'
    else:
      alias = command.name if not parent else f'{parent} {command.name}'
    return f'{alias} {command.signature}'

  def common_command_formatting(self, embed_like, command):
    embed_like.title = self.get_command_signature(command)
    if command.description:
      embed_like.description = f'{command.description}\n\n{command.help}'
    else:
      embed_like.description = command.help or 'No help found...'



  async def send_group_help(self, group):
    with open('data/json/blacklist.json', 'r', encoding="utf-8") as f:
      bled = json.load(f)
    data = getIgnore(self.context.guild.id)
    ch = data["channel"]
    iuser = data["user"]
    buser = data["bypassuser"]
    bl = discord.Embed(description="You are blacklisted from using my commannds.\nreason could be excessive use or spamming commands\nJoin our [Support Server](https://discord.com/invite/CCYef4Ad4M) to appeal .", color=discord.Colour(0x2f3136))
    embed = discord.Embed(description="This Channel is in ignored channel list try my commands in another channel .", color=discord.Colour(0x2f3136))
    ign = discord.Embed(description=f"You are set as a ignored users for {self.context.guild.name} .\nTry my commands or modules in another guild .", color=discord.Colour(0x2f3136))

    if str(self.context.author.id) in bled["ids"]:
      await self.context.send(embed=bl,delete_after=10)
      return 

    if str(self.context.author.id) in iuser and str(self.context.author.id) not in buser:
      await self.context.send(embed=ign,delete_after=10)
      return 

   # if str(self.context.channel.id) in ch and str(self.context.author.id) not in buser:
    #  await self.context.send(embed=embed,delete_after=10)
     # return
    else:
      entries = [(
        f"`{self.context.prefix}{cmd.qualified_name}`",
        f"{cmd.short_doc if cmd.short_doc else 'No Description Provided...'}\n\n"
      ) for cmd in group.commands]
    paginator = Paginator(source=FieldPagePaginator(
      entries=entries,
      title=f"{group.qualified_name} Commands",
      description="```yaml\n- [] = optional argument\n- <> = required argument\n- Do NOT Type These When Using Commands !```",
      color=0x00FFCA,
      per_page=10),ctx=self.context)
    await paginator.paginate()       


  async def send_cog_help(self, cog):
    with open('data/json/blacklist.json', 'r', encoding="utf-8") as f:
      bled = json.load(f)
    data = getIgnore(self.context.guild.id)
    ch = data["channel"]
    iuser = data["user"]
    buser = data["bypassuser"]
    bl = discord.Embed(description="You are blacklisted from using my commannds.\nreason could be excessive use or spamming commands\nJoin our [Support Server](https://discord.com/invite/CCYef4Ad4M) to appeal .", color=discord.Colour(0x2f3136))
    embed = discord.Embed(description="This Channel is in ignored channel list try my commands in another channel .", color=discord.Colour(0x2f3136))
    ign = discord.Embed(description=f"You are set as a ignored users for {self.context.guild.name} .\nTry my commands or modules in another guild .", color=discord.Colour(0x2f3136))

    if str(self.context.author.id) in bled["ids"]:
      await self.context.send(embed=bl,delete_after=10)
      return 

    if str(self.context.author.id) in iuser and str(self.context.author.id) not in buser: 
      await self.context.send(embed=ign,delete_after=10)
      return 

   # if str(self.context.channel.id) in ch and str(self.context.author.id) not in buser:
    #  await self.context.send(embed=embed,delete_after=10)
     # return

    entries = [(
      f"`{self.context.prefix}{cmd.qualified_name}`",
      f"{cmd.short_doc if cmd.short_doc else ''}"
      f"\n\n",
    ) for cmd in cog.get_commands()]
    paginator = Paginator(source=FieldPagePaginator(
      entries=entries,
      title=f"{cog.qualified_name.title()} ({len(cog.get_commands())})",
      description="<...> Duty | [...] Optional\n\n",
      color=color,
      per_page=10),
                          ctx=self.context)
    await paginator.paginate()  






class Help(Cog, name="help"):

  def __init__(self, client:Redox):
    self._original_help_command = client.help_command
    attributes = {
      'name':
      "help",
      'aliases': ['h'],
      'cooldown':
      commands.CooldownMapping.from_cooldown(1, 5, commands.BucketType.user),
      'help':
      'Shows help about bot, a command or a category'
    }
    client.help_command = HelpCommand(command_attrs=attributes)
    client.help_command.cog = self

  async def cog_unload(self):
    self.help_command = self._original_help_command