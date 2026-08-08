import contextlib
import json
from traceback import format_exception
import discord
from discord.ext import commands
import io
import textwrap
import datetime
import sys
from discord.ui import Button, View
import psutil
import time
import datetime
import platform
from utils.Tools import *
import os
import logging
from discord.ext import commands
import motor.motor_asyncio
from pymongo import MongoClient
from discord.ext.commands import BucketType, cooldown
import requests
from typing import *
from utils import *
from discord import Embed, Member
from discord.ext.commands import Context
from discord import Spotify
from core import Context
from typing import Optional
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


start_time = time.time()


def datetime_to_seconds(thing: datetime.datetime):
  current_time = datetime.datetime. me(time.time())
  return round(
    round(time.time()) +
    (current_time - thing.replace(tzinfo=None)).total_seconds())


def getBDG(userid):
    with open("data/json/bdg.json", "r", encoding="utf-8") as config:
        data = json.load(config)
    if str(userid) not in data["users"]:
        defaultConfig = {
            "owner": False,
            "developer": False,
            "staff": False,
            "early": False,
            "partner": False,
            "vip": False,
            "friends": False,
            "bug": False,
            "sponsors": False,
            "family": True 
            
        }
        updateBDG(userid, defaultConfig)
        return defaultConfig
    return data["users"][str(userid)]


def updateBDG(userid, data):
    with open("data/json/bdg.json", "r", encoding="utf-8") as config:
        config = json.load(config)
    config["users"][str(userid)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("data/json/bdg.json", "w", encoding="utf-8") as config:
        config.write(newdata)


class Utility(commands.Cog):

  def __init__(self, bot):
    self.client = bot
    self.bot = bot


               
    
  @commands.hybrid_command(name="badges",help="Check what premium badges a user have.",aliases=["badge", "profile", "pr"],usage="Badges [user]",with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def profile(self,ctx, mem: discord.Member = None):
      if mem is None:
          mem = ctx.author
      message = await ctx.send(embed=discord.Embed(description="**<a:loadingcool:1177972703429394553> | Loading user info**"))
      background_image = Image.open("data/pictures/default.png").convert("RGBA")
      font = ImageFont.truetype('data/fonts/amanop.ttf', 40)
      draw = ImageDraw.Draw(background_image)
      draw.text((60, 510), f"{mem.name}", font=font)
      avatar_url = mem.avatar.url if mem.avatar else mem.default_avatar.url
      response = requests.get(avatar_url)
      avatar_image = Image.open(BytesIO(response.content)).convert("RGBA")
      avatar_image = avatar_image.resize((340, 340)) 
      background_image.paste(avatar_image, (50, 70), avatar_image) 
      data = getBDG(mem.id) 
      selected_images = []
      text=[]
 
      cord=[(560,125), (1000, 125), (560, 260), (1000, 260), (560, 390), (1000, 390), (560, 530),(1000,530),(560,665),(1000,665)]
      if data["owner"] ==True:
        selected_images+=["https://cdn.discordapp.com/emojis/1253658307806236722.jpg?v=1&size=48"]
        text+=["Owner"]
      if data["developer"] ==True:
        selected_images+=["https://cdn.discordapp.com/emojis/1253658492808593518.jpg?v=1&size=48"]
        text+=["Developer"]
      if data["early"] ==True:
        selected_images+=["https://cdn.discordapp.com/emojis/1253662457621250058.jpg?v=1&size=48"]
        text+=["Early Supporter"]
      if data["staff"] ==True:
        selected_images+=["https://cdn.discordapp.com/emojis/1253658901556101180.jpg?v=1&size=48"]
        text+=["Staff"]
      if data["bug"] ==True:
        selected_images+=["https://cdn.discordapp.com/emojis/1253661201674801182.jpg?v=1&size=48"]
        text+=["Bug Hunter"]
      if data["vip"] ==True:
        selected_images+=["https://cdn.discordapp.com/emojis/1253663009050726411.jpg?v=1&size=48"]
        text+=["VIP"]
      if data["sponsors"] ==True:
        selected_images+=["https://cdn.discordapp.com/emojis/1253658645829517323.jpg?v=1&size=48"]
        text+=["Sponsors"]
      if data["partner"] ==True:
        selected_images+=["https://cdn.discordapp.com/emojis/1253659491413659699.jpg?v=1&size=48"]
        text+=["Partner"]
      if data["friends"] ==True:
        selected_images+=["https://cdn.discordapp.com/emojis/1253658530628636672.jpg?v=1&size=48"]
        text+=["Friends"]
      if data["family"] ==True:
        selected_images+=["https://cdn.discordapp.com/emojis/1253658414211403808.jpg?v=1&size=48"]
        text+=["Family"]
      locations = [(430, 105), (870, 105), (430, 240), (870, 240), (430, 370), (870, 370), (430, 510),(870,510),(430,645),(870,645)]
      
      for i, image_url in enumerate(selected_images):
	      response = requests.get(image_url)
	      img = Image.open(BytesIO(response.content));img = img.resize((90, 90));background_image.paste(img, locations[i])
    
      for lol, coordinates in zip(text, cord):
        draw.text(coordinates, f"{lol}", font=font)
      badges = ""
      if mem.public_flags.hypesquad:
        badges += "** ◇ Hypesquad**\n"
      elif mem.public_flags.hypesquad_balance:
        badges += "** ◇ <:hypesquad_balance:1125036381845073930> HypeSquad Balance**\n"

      elif mem.public_flags.hypesquad_bravery:
        badges += "** ◇ <:hypesquad_bravery:1125036563131277355> HypeSquad Bravery**\n"
      elif mem.public_flags.hypesquad_brilliance:
        badges += "** ◇ <:hypesquad_brilliance:1125036584941662299> Hypesquad Brilliance**\n"
      if mem.public_flags.early_supporter:
        badges += "** ◇ <:early:1125036703288135721> Early Supporter**\n"
      elif mem.public_flags.verified_bot_developer:
        badges += "** ◇ <:verified_bot_dev:1125036917155692585> Verified Bot Developer**\n"
      elif mem.public_flags.active_developer:
        badges += "** ◇ <:icons_activedevbadge:1125036888219193484> Active Developer**\n"
      if badges == "":
        badges = "None"
      embed2 = discord.Embed(title=f"** ◇ {mem.name}'s Profile**",color=mem.color)
      embed2.add_field(
        name="**__Account Info__**",
        value=f"** ◇ Account Created at **: <t:{round(mem.created_at.timestamp())}:R>\n** ◇ Joined at : <t:{round(mem.joined_at.timestamp())}:R>**",
        inline=False)
      embed2.add_field(name="**User Badges:**",
                       value=f"{badges}",
                       inline=False)
      embed2.add_field(
        name="**Bot Badges:**",
        value="**Here**",
        inline=False)
      embed2.set_thumbnail(
        url=mem.avatar.url if mem.avatar else mem.default_avatar.url)
     
      buffer = BytesIO()
      background_image.save(buffer, format="PNG")
      buffer.seek(0)
      file = discord.File(buffer, filename="itz_your_aman_op.png")
      embed2.set_image(url="attachment://itz_your_aman_op.png")
      await message.edit(embed=embed2, attachments=[file])

     


  @commands.group(name="bdg", invoke_without_command=True)
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @blacklist_check()
  @ignore_check()
  async def _autorole(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    
  @_autorole.command(name="remove")
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.is_owner()
  @blacklist_check()
  @ignore_check()
  async def bdg_remove(self,ctx, user: discord.Member,*, badge: str):
      userid= user.id
      data = getBDG(user.id)
      badge = badge.lower()
      tick_emoji = "<a:tickkk:1223594613961523281>"
      if badge in ["dev", "developer", "devp"]:
        data["developer"] = False
        updateBDG(user.id, data)
        embed = discord.Embed(description=f"{tick_emoji} | Successfully removed `developer` badge from {user.mention}")
        await ctx.send(embed=embed)
      elif badge in ["owner"]:
        data["owner"] = False
        updateBDG(user.id, data)
        embed = discord.Embed(description=f"{tick_emoji} | Successfully removed `owner` badge from {user.mention}")
        await ctx.send(embed=embed)
      elif badge in ["staff"]:
        data["staff"] = False
        updateBDG(userid, data)
        embed = discord.Embed(description=f"{tick_emoji} | Successfully removed `staff` badge from {user.mention}")
        await ctx.send(embed=embed)
      elif badge in ["sponsors", "sponsor"]:
        data["sponsors"] = False
        updateBDG(userid, data)
        embed = discord.Embed(description=f"{tick_emoji} | Successfully removed `sponsor` badge from {user.mention}")
        await ctx.send(embed=embed)
      elif badge in ["friend", "friends"]:
        data["friends"] = False
        updateBDG(userid, data)
        embed = discord.Embed(description=f"{tick_emoji} | Successfully removed `friend` badge from {user.mention}")
        await ctx.send(embed=embed)
      elif badge in ["bug", "hunter"]:
        data["bug"] = False
        updateBDG(userid, data)
        embed = discord.Embed(description=f"{tick_emoji} | Successfully removed `bug hunter` badge from {user.mention}")
        await ctx.send(embed=embed)
      elif badge in ["vip"]:
        data["vip"] = False
        updateBDG(userid, data)
        embed = discord.Embed(description=f"{tick_emoji} | Successfully removed `vip` badge from {user.mention}")
        await ctx.send(embed=embed)
      elif badge in ["early"]:
        data["early"] = False
        updateBDG(userid, data)
        embed = discord.Embed(description=f"{tick_emoji} | Successfully removed `early` badge from {user.mention}")
        await ctx.send(embed=embed)
      elif badge in ["partner"]:
        data["partner"] = False
        updateBDG(userid, data)
        embed = discord.Embed(description=f"{tick_emoji} | Successfully removed `partner` badge from {user.mention}")
        await ctx.send(embed=embed)
      elif badge in ["all"]:
        data["developer"] = False
        data["owner"] = False
        data["staff"] = False
        data["sponsors"] = False
        data["friends"] = False
        data["bug"] = False
        data["vip"] = False
        data["early"] = False
        data["partner"] = False
        updateBDG(user.id, data)
        embed = discord.Embed(description=f"{tick_emoji} | Successfully removed all badges from {user.mention}")
        await ctx.send(embed=embed)
      else:
        embed = discord.Embed(description="<a:crossss:1174609979932684328>** | No badge found!**")
        await ctx.send(embed=embed)


  @_autorole.command(name="add")
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.is_owner()
  @blacklist_check()
  @ignore_check()
  async def bdg_add(self,ctx, user: discord.Member, badge: str):
      userid = user.id
      data = getBDG(userid)
      badge = badge.lower()
      tick_emoji = "<a:tickkk:1223594613961523281>"
      if badge in ["dev", "developer", "devp"]:
        data["developer"] = True
        updateBDG(userid, data)
        embed = discord.Embed(description=f"{tick_emoji} | Successfully added `developer` badge to {user.mention}")
        await ctx.send(embed=embed)
      elif badge in ["owner"]:
        data["owner"] = True
        updateBDG(userid, data)
        embed = discord.Embed(description=f"{tick_emoji} | Successfully added `owner` badge to {user.mention}")
        await ctx.send(embed=embed)
      elif badge in ["staff"]:
        data["staff"] = True
        updateBDG(userid, data)
        embed = discord.Embed(description=f"{tick_emoji} | Successfully added `staff` badge to {user.mention}")
        await ctx.send(embed=embed)
      elif badge in ["sponsors", "sponsor"]:
        data["sponsors"] = True
        updateBDG(userid, data)
        embed = discord.Embed(description=f"{tick_emoji} | Successfully added `sponsor` badge to {user.mention}")
        await ctx.send(embed=embed)
      elif badge in ["friend", "friends"]:
        data["friends"] = True
        updateBDG(userid, data)
        embed = discord.Embed(description=f"{tick_emoji} | Successfully added `friend` badge to {user.mention}")
        await ctx.send(embed=embed)
      elif badge in ["bug", "hunter"]:
        data["bug"] = True
        updateBDG(userid, data)
        embed = discord.Embed(description=f"{tick_emoji} | Successfully added `bug hunter` badge to {user.mention}")
        await ctx.send(embed=embed)
      elif badge in ["vip"]:
        data["vip"] = True
        updateBDG(userid, data)
        embed = discord.Embed(description=f"{tick_emoji} | Successfully added `vip` badge to {user.mention}")
        await ctx.send(embed=embed)
      elif badge in ["early"]:
        data["early"] = True
        updateBDG(userid, data)
        embed = discord.Embed(description=f"{tick_emoji} | Successfully added `early` badge to {user.mention}")
        await ctx.send(embed=embed)
      elif badge in ["partner"]:
        data["partner"] = True
        updateBDG(userid, data)
        embed = discord.Embed(description=f"{tick_emoji} | Successfully added `partner` badge to {user.mention}")
        await ctx.send(embed=embed)
      elif badge in ["all"]:
        data["developer"] = True
        data["owner"] = True
        data["staff"] = True
        data["sponsors"] = True
        data["friends"] = True
        data["bug"] = True
        data["vip"] = True
        data["early"] = True
        data["partner"] = True
        updateBDG(userid, data)
        embed = discord.Embed(description=f"{tick_emoji} | Successfully added all badges to {user.mention}")
        await ctx.send(embed=embed)
      else:
        embed = discord.Embed(description="<a:crossss:1174609979932684328> **| No badge found!**")
        await ctx.send(embed=embed)
     
  # Stop
        
  @commands.group(name="banner")
  async def banner(self, ctx):
    if ctx.invoked_subcommand is None:
      await ctx.send_help(ctx.command)

  @banner.command(name="server")
  async def server(self, ctx):
    if not ctx.guild.banner:
      await ctx.reply("This server does not have a banner.")
    else:
      webp = ctx.guild.banner.replace(format='webp')
      jpg = ctx.guild.banner.replace(format='jpg')
      png = ctx.guild.banner.replace(format='png')
      embed = discord.Embed(
        color=0x00FFCA,
        description=f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp})"
        if not ctx.guild.banner.is_animated() else
        f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp}) | [`GIF`]({ctx.guild.banner.replace(format='gif')})"
      )
      embed.set_image(url=ctx.guild.banner)
      embed.set_author(name=ctx.guild.name,
                       icon_url=ctx.guild.icon.url
                       if ctx.guild.icon else ctx.guild.default_icon.url)
      embed.set_footer(text=f"Requested By {ctx.author}",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
      await ctx.reply(embed=embed)

  @blacklist_check()
  @ignore_check()
  @banner.command(name="user")
  @commands.cooldown(1, 2, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def _user(self,
                  ctx,
                  member: Optional[Union[discord.Member,
                                         discord.User]] = None):
    if member == None or member == "":
      member = ctx.author
    bannerUser = await self.bot.fetch_user(member.id)
    if not bannerUser.banner:
      await ctx.reply("{} does not have a banner.".format(member))
    else:
      webp = bannerUser.banner.replace(format='webp')
      jpg = bannerUser.banner.replace(format='jpg')
      png = bannerUser.banner.replace(format='png')
      embed = discord.Embed(
        color=0x00FFCA,
        description=f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp})"
        if not bannerUser.banner.is_animated() else
        f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp}) | [`GIF`]({bannerUser.banner.replace(format='gif')})"
      )
      embed.set_author(name=f"{member}",
                       icon_url=member.avatar.url
                       if member.avatar else member.default_avatar.url)
      embed.set_image(url=bannerUser.banner)
      embed.set_footer(text=f"Requested By {ctx.author}",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

      await ctx.send(embed=embed)

  @commands.hybrid_command(name="invite", aliases=['inv'],help="Invite me to your server")
  @blacklist_check()
  @ignore_check()
  async def invite(self, ctx: commands.Context):
    embed = discord.Embed(
      title=
      "** <a:999:1157951733486592072> Redox's Invite**<a:999:1157951733486592072> ",
      description=
      "> • **[Invite Me ](https://discord.com/oauth2/authorize?client_id=1126351590064930847&permissions=1239031351480&scope=bot)\n> • [Support Server](https://discord.com/invite/5SUKAB7n93)**",
      color=0xff0000)
    buttons = [
            Button(style=discord.ButtonStyle.link, label='Invite Redox', url='https://discord.com/oauth2/authorize?client_id=1126351590064930847&permissions=1239031351480&scope=bot'),
            Button(style=discord.ButtonStyle.link, label='Join Support Server', url='https://discord.com/invite/5SUKAB7n93')
    ]
    view = View()
    view.add_item(buttons[0])
    view.add_item(buttons[1])
    embed.set_thumbnail(url=self.bot.user.avatar.url)
    await ctx.send(embed=embed,view= view)

  #@commands.hybrid_command(name="vote",
                           #aliases=['dbl'],
                           #description="Vote Me and Support Us")
 # @commands.cooldown(1, 3, commands.BucketType.user)
 # @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  #@commands.guild_only()
 # @blacklist_check()
 # @ignore_check()
 # async def _vote(self, ctx):
   # button = Button(label="Vote", url="https://discord.com/invite/5SUKAB7n93")

   # embed = discord.Embed(
      #color=discord.Colour(0x0d0d13),
     # description=
    ##  "**[Click Here](https://discord.com/invite/5SUKAB7n93)** To Vote Me.")
   # view = View()
  #  view.add_item(button)
  #  embed.set_author(name='Vote Redox',
  #                   icon_url=self.bot.user.display_avatar.url)
   # await ctx.send(embed=embed, view=view)

  @commands.hybrid_command(name="botinfo",
                           aliases=['bi'],
                           help="Get info about me!",
                           with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def botinfo(self, ctx: commands.Context):
    users = sum(g.member_count for g in self.bot.guilds
                if g.member_count != None)
    channel = len(set(self.bot.get_all_channels()))
    embed = discord.Embed(color=0x0d0d13,
                          title="Redox's Information",
                          description=f"""
**Bot's Mention:** {self.bot.user.mention}
**Bot's Username:** {self.bot.user}
**Total Guilds:** {len(self.bot.guilds)}
**Total Users:** {users}
**Total Channels:** {channel}
**Total Commands: **{len(set(self.bot.walk_commands()))}
**Total Shards:** {len(self.bot.shards)}
**Uptime:** {str(datetime.timedelta(seconds=int(round(time.time()-start_time))))}
**CPU usage:** {round(psutil.cpu_percent())}%
**Memory usage:** {int((psutil.virtual_memory().total - psutil.virtual_memory().available)
 / 1024 / 1024)} MB
**My Websocket Latency:** {int(self.bot.latency * 1000)} ms
**Python Version:** {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}
**Discord.py Version:** {discord.__version__}
""")
    sum_us = sum(g.member_count for g in self.bot.guilds if g.member_count != None)
    button = Button(label="Guilds: "+str(len(self.bot.guilds)), style=discord.ButtonStyle.red, disabled=True)
    button1 = Button(label="Users: "+f"{sum_us}", style=discord.ButtonStyle.green, disabled=True)
    button2 = Button(label=f"Ping : {int(self.bot.latency * 1000)} ms", style=discord.ButtonStyle.green, disabled=True)
    view = View()
    view.add_item(button)
    view.add_item(button1)
    view.add_item(button2)
    embed.set_footer(text=f"Requested By {ctx.author}",
                     icon_url=ctx.author.avatar.url
                     if ctx.author.avatar else ctx.author.default_avatar.url)
    embed.set_thumbnail(url=self.bot.user.display_avatar.url)
    await ctx.send(embed=embed,view=view)

  @blacklist_check()
  @ignore_check()
  @commands.hybrid_command(name="userinfo",help="Show you all information about the user.",
                           aliases=["whois", "ui"],
                           usage="Userinfo [user]",
                           with_app_command=True)
  @commands.cooldown(1, 2, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  async def _userinfo(self,
                      ctx,
                      member: Optional[Union[discord.Member,
                                             discord.User]] = None):
    if member == None or member == "":
      member = ctx.author
    elif member not in ctx.guild.members:
      member = await self.bot.fetch_user(member.id)

    badges = ""
    if member.public_flags.hypesquad:
      badges += "<:Hypesquad:1125037578110914630> "
    if member.public_flags.hypesquad_balance:
      badges += "<:hypesquad_balance:1125036381845073930> "
    if member.public_flags.hypesquad_bravery:
      badges += "<:hypesquad_bravery:1125036563131277355> "
    if member.public_flags.hypesquad_brilliance:
      badges += "<:hypesquad_brilliance:1125036584941662299> "
    if member.public_flags.early_supporter:
      badges += "<:early:1125036703288135721> "
    if member.public_flags.active_developer:
      badges += "<:icons_activedevbadge:1125036888219193484> "
    if member.public_flags.verified_bot_developer:
      badges += "<:verified_bot_dev:1125036917155692585> "
    if member.public_flags.discord_certified_moderator:
      badges += "<:icons_mod:1124694792140509206> "
    if member.public_flags.staff:
      badges += "<:staff_icons:1125037091810709625> "
    if member.public_flags.partner:
      badges += "<:icons_partner:1125037151306907748> "
    if badges == None or badges == "":
      badges += "None"

    if member in ctx.guild.members:
      nickk = f"{member.nick if member.nick else 'None'}"
      joinedat = f"<t:{round(member.joined_at.timestamp())}:R>"
    else:
      nickk = "None"
      joinedat = "None"

    kp = ""
    if member in ctx.guild.members:
      if member.guild_permissions.kick_members:
        kp += " , Kick Members"
      if member.guild_permissions.ban_members:
        kp += " , Ban Members"
      if member.guild_permissions.administrator:
        kp += " , Administrator"
      if member.guild_permissions.manage_channels:
        kp += " , Manage Channels"


#    if  member.guild_permissions.manage_server:
#        kp = "Manage Server"
      if member.guild_permissions.manage_messages:
        kp += " , Manage Messages"
      if member.guild_permissions.mention_everyone:
        kp += " , Mention Everyone"
      if member.guild_permissions.manage_nicknames:
        kp += " , Manage Nicknames"
      if member.guild_permissions.manage_roles:
        kp += " , Manage Roles"
      if member.guild_permissions.manage_webhooks:
        kp += " , Manage Webhooks"
      if member.guild_permissions.manage_emojis:
        kp += " , Manage Emojis"

      if kp is None or kp == "":
        kp = "None"

    if member in ctx.guild.members:
      if member == ctx.guild.owner:
        aklm = "Server Owner"
      elif member.guild_permissions.administrator:
        aklm = "Server Admin"
      elif member.guild_permissions.ban_members or member.guild_permissions.kick_members:
        aklm = "Server Moderator"
      else:
        aklm = "Server Member"

    bannerUser = await self.bot.fetch_user(member.id)
    embed = discord.Embed(color=0x0d0d13)
    embed.timestamp = discord.utils.utcnow()
    if not bannerUser.banner:
      pass
    else:
      embed.set_image(url=bannerUser.banner)
    embed.set_author(name=f"{member.name}'s Information",
                     icon_url=member.avatar.url
                     if member.avatar else member.default_avatar.url)
    embed.set_thumbnail(
      url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.add_field(name="__General Information__",
                    value=f"""
**Name:** {member}
**ID:** {member.id}
**Nickname:** {nickk}
**Bot?:** {'<:tick_icons:1124596979813580801> Yes' if member.bot else '<:icons_cross:1124690918893690920> No'}
**Badges:** {badges}
**Account Created:** <t:{round(member.created_at.timestamp())}:R>
**Server Joined:** {joinedat}
            """,
                    inline=False)
    if member in ctx.guild.members:
      r = (', '.join(role.mention for role in member.roles[1:][::-1])
           if len(member.roles) > 1 else 'None.')
      embed.add_field(name="__Role Info__",
                      value=f"""
**Highest Role:** {member.top_role.mention if len(member.roles) > 1 else 'None'}
**Roles [{f'{len(member.roles) - 1}' if member.roles else '0'}]:** {r if len(r) <= 1024 else r[0:1006] + ' and more...'}
**Color:** {member.color if member.color else '000000'}
                """,
                      inline=False)
    if member in ctx.guild.members:
      embed.add_field(
        name="__Extra__",
        value=
        f"**Boosting:** {f'<t:{round(member.premium_since.timestamp())}:R>' if member in ctx.guild.premium_subscribers else 'None'}\n**Voice <:icons_mic:1124695914397827224>:** {'None' if not member.voice else member.voice.channel.mention}",
        inline=False)
    if member in ctx.guild.members:
      embed.add_field(name="__Key Permissions__",
                      value=", ".join([kp]),
                      inline=False)
    if member in ctx.guild.members:
      embed.add_field(name="__Acknowledgement__",
                      value=f"{aklm}",
                      inline=False)
    if member in ctx.guild.members:
      embed.set_footer(text=f"Requested by {ctx.author}",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
    else:
      if member not in ctx.guild.members:
        embed.set_footer(text=f"{member.name} not in this this server.",
                         icon_url=ctx.author.avatar.url if ctx.author.avatar
                         else ctx.author.default_avatar.url)
    await ctx.send(embed=embed)

  @blacklist_check()
  @ignore_check()
  @commands.command(name="status",
                    description="Shows users status",
                    usage="status <member>",
                    with_app_command=True)
  async def status(self, ctx, member: discord.Member = None):
    if member == None:
      member = ctx.author

    status = member.status
    if status == discord.Status.offline:
      status_location = "Not Applicable"
    elif member.mobile_status != discord.Status.offline:
      status_location = "Mobile"
    elif member.web_status != discord.Status.offline:
      status_location = "Browser"
    elif member.desktop_status != discord.Status.offline:
      status_location = "Desktop"
    else:
      status_location = "Not Applicable"
    await ctx.send(embed=discord.Embed(
      title="**<a:randi_dance:1138852908436299907> | status**",
      description="`%s`: `%s`" % (status_location, status),
      color=0x0d0d13))

  @commands.command(name="emoji",
                    help="Shows emoji syntax",
                    usage="emoji <emoji>")
  @blacklist_check()
  @ignore_check()
  async def emoji(self, ctx, emoji: discord.Emoji):
    return await ctx.send(embed=discord.Embed(
      title="**<:icons_emojis:1125038543094431764> | emoji**",
      description="emoji: %s\nid: **`%s`**" % (emoji, emoji.id),
      color=0x41eeee))

  @commands.command(name="user",
                    help="Shows user syntax",
                    usage="user [user]",
                    with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def user(self, ctx, user: discord.Member = None):
    return await ctx.send(
      embed=discord.Embed(title="user",
                          description="user: %s\nid: **`%s`**" %
                          (user.mention, user.id),
                          color=0x0d0d13))

  @commands.command(name="channel",
                    help="Shows channel syntax",
                    usage="channel <channel>")
  @blacklist_check()
  @ignore_check()
  async def channel(self, ctx, channel: discord.TextChannel):
    return await ctx.send(
      embed=discord.Embed(title="channel",
                          description="channel: %s\nid: **`%s`**" %
                          (channel.mention, channel.id),
                          color=0x00FFCA))

  @commands.hybrid_command(name="steal",
                           help="Adds a emoji",
                           usage="steal <emoji>",
                           aliases=["eadd"],
                           with_app_command=True)
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_emojis=True)
  async def steal(self, ctx, emote):
    try:
      if emote[0] == '<':
        name = emote.split(':')[1]
        emoji_name = emote.split(':')[2][:-1]
        anim = emote.split(':')[0]
        if anim == '<a':
          url = f'https://cdn.discordapp.com/emojis/{emoji_name}.gif'
        else:
          url = f'https://cdn.discordapp.com/emojis/{emoji_name}.png'
        try:
          response = requests.get(url)
          img = response.content
          emote = await ctx.guild.create_custom_emoji(name=name, image=img)
          return await ctx.send(
            embed=discord.Embed(title="emoji-add",
                                description="added \"**`%s`**\"!" % (emote),
                                color=0x41eeee))
        except Exception:
          return await ctx.send(
            embed=discord.Embed(title="emoji-add",
                                description=f"failed to add emoji",
                                color=0x00FFCA))
      else:
        return await ctx.send(embed=discord.Embed(
          title="emoji-add", description=f"invalid emoji", color=0x41eeee))
    except Exception:
      return await ctx.send(embed=discord.Embed(
        title="emoji-add", description=f"failed to add emoji", color=0x41eeee))

  @commands.hybrid_command(name="removeemoji",
                           help="Deletes the emoji from the server",
                           usage="removeemoji <emoji>")
  @blacklist_check()
  @ignore_check()
  @commands.has_permissions(manage_emojis=False)
  async def removeemoji(self, ctx, emoji: discord.Emoji):
    await emoji.delete()
    await ctx.send("**<a:tickkk:1130730211382661171> emoji has been deleted.**"
                   )

  @commands.hybrid_command(name="unbanall",
                           help="Unbans Everyone In The Guild!",
                           aliases=['massunban'],
                           usage="Unbanall",
                           with_app_command=True)
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 30, commands.BucketType.user)
  @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
  @commands.guild_only()
  @commands.has_permissions(ban_members=True)
  async def unbanall(self, ctx):
    button = Button(label="Yes",
                    style=discord.ButtonStyle.green,
                    emoji="<a:tickkk:1130730211382661171>")
    button1 = Button(label="No",
                     style=discord.ButtonStyle.red,
                     emoji="<a:crossss:1131829269509709875>")

    async def button_callback(interaction: discord.Interaction):
      a = 0
      if interaction.user == ctx.author:
        if interaction.guild.me.guild_permissions.ban_members:
          await interaction.response.edit_message(
            content="Unbanning All Banned Member(s)", embed=None, view=None)
          async for idk in interaction.guild.bans(limit=None):
            await interaction.guild.unban(
              user=idk.user,
              reason="Unbanall Command Executed By: {}".format(ctx.author))
            a += 1
          await interaction.channel.send(
            content=f"Successfully Unbanned {a} Member(s)")
        else:
          await interaction.response.edit_message(
            content=
            "I am missing ban members permission.\ntry giving me permissions and retry",
            embed=None,
            view=None)
      else:
        await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)

    async def button1_callback(interaction: discord.Interaction):
      if interaction.user == ctx.author:
        await interaction.response.edit_message(
          content="Ok I will Not unban anyone.", embed=None, view=None)
      else:
        await interaction.response.send_message("This Is Not For You Dummy!",
                                                embed=None,
                                                view=None,
                                                ephemeral=True)

    embed = discord.Embed(
      color=0x41eeee,
      description='**Are you sure you want to unban everyone in this guild?**')

    view = View()
    button.callback = button_callback
    button1.callback = button1_callback
    view.add_item(button)
    view.add_item(button1)
    await ctx.reply(embed=embed, view=view, mention_author=False)

  @commands.command(name="joined-at",
                    help="Shows when a user joined",
                    usage="joined-at [user]",
                    with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def joined_at(self, ctx):
    joined = ctx.author.joined_at.strftime("%a, %d %b %Y %I:%M %p")
    await ctx.send(embed=discord.Embed(
      title="joined-at", description="**`%s`**" % (joined), color=0x41eeee))

  @commands.command(name="github", usage="github [search]")
  @blacklist_check()
  @ignore_check()
  async def github(self, ctx, *, search_query):
    json = requests.get(
      f"https://api.github.com/search/repositories?q={search_query}").json()

    if json["total_count"] == 0:
      await ctx.send("No matching repositories found")
    else:
      await ctx.send(
        f"First result for '{search_query}':\n{json['items'][0]['html_url']}")

  @commands.hybrid_command(name="vcinfo",
                           help="get info about voice channel",
                           usage="Vcinfo <VoiceChannel>",
                           with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def vcinfo(self, ctx: Context, vc: discord.VoiceChannel):
    e = discord.Embed(title='VC Information', color=0x00FFCA)
    e.add_field(name='VC name', value=vc.name, inline=False)
    e.add_field(name='VC ID', value=vc.id, inline=False)
    e.add_field(name='VC bitrate', value=vc.bitrate, inline=False)
    e.add_field(name='Mention', value=vc.mention, inline=False)
    e.add_field(name='Category name', value=vc.category.name, inline=False)
    await ctx.send(embed=e)

  @commands.hybrid_command(name="channelinfo",
                           help="shows info about channel",
                           aliases=['channeli', 'cinfo', 'ci'],
                           pass_context=False,
                           no_pm=False,
                           usage="Channelinfo [channel]",
                           with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def channelinfo(self, ctx, *, channel: int = None):
    """Shows channel information"""
    if not channel:
      channel = ctx.message.channel
    else:
      channel = self.bot.get_channel(channel)
    data = discord.Embed()
    if hasattr(channel, 'mention'):
      data.description = "**Information about Channel:** " + channel.mention
    if hasattr(channel, 'changed_roles'):
      if len(channel.changed_roles) > 0:
        data.color = 0x00FFCA if channel.changed_roles[
          0].permissions.read_messages else 0x00FFCA
    if isinstance(channel, discord.TextChannel):
      _type = "Text"
    elif isinstance(channel, discord.VoiceChannel):
      _type = "Voice"
    else:
      _type = "Unknown"
    data.add_field(name="Type", value=_type)
    data.add_field(name="ID", value=channel.id, inline=False)
    if hasattr(channel, 'position'):
      data.add_field(name="Position", value=channel.position)
    if isinstance(channel, discord.VoiceChannel):
      if channel.user_limit != 0:
        data.add_field(name="User Number",
                       value="{}/{}".format(len(channel.voice_members),
                                            channel.user_limit))
      else:
        data.add_field(name="User Number",
                       value="{}".format(len(channel.voice_members)))
      userlist = [r.display_name for r in channel.members]
      if not userlist:
        userlist = "None"
      else:
        userlist = "\n".join(userlist)
      data.add_field(name="Users", value=userlist)
      data.add_field(name="Bitrate", value=channel.bitrate)
    elif isinstance(channel, discord.TextChannel):
      try:
        pins = await channel.pins()
        data.add_field(name="Pins", value=len(pins), inline=False)
      except discord.Forbidden:
        pass
      data.add_field(name="Members", value="%s" % len(channel.members))
      if channel.topic:
        data.add_field(name="Topic", value=channel.topic, inline=False)
      hidden = []
      allowed = []
      for role in channel.changed_roles:
        if role.permissions.read_messages is False:
          if role.name != "@everyone":
            allowed.append(role.mention)
        elif role.permissions.read_messages is False:
          if role.name != "@everyone":
            hidden.append(role.mention)
      if len(allowed) > 0:
        data.add_field(name='Allowed Roles ({})'.format(len(allowed)),
                       value=', '.join(allowed),
                       inline=False)
      if len(hidden) > 0:
        data.add_field(name='Restricted Roles ({})'.format(len(hidden)),
                       value=', '.join(hidden),
                       inline=False)
    if channel.created_at:
      data.set_footer(text=("Created on {} ({} days ago)".format(
        channel.created_at.strftime("%d %b %Y %H:%M"), (
          ctx.message.created_at - channel.created_at).days)))
    await ctx.send(embed=data)

  @commands.command(name="note",
                    help="Creates a note for you",
                    usage="Note <message>")
  @cooldown(1, 10, BucketType.user)
  @blacklist_check()
  @ignore_check()
  async def note(self, ctx, *, message):
    message = str(message)
    print(message)
    stats = await notedb.find_one({"id": ctx.author.id})
    if len(message) <= 50:
      #
      if stats is None:
        newuser = {"id": ctx.author.id, "note": message}
        await notedb.insert_one(newuser)
        await ctx.send("**Your note has been stored**")
        await ctx.message.delete()

      else:
        x = notedb.find({"id": ctx.author.id})
        z = 0
        async for i in x:
          z += 1
        if z > 2:
          await ctx.send("**You cannot add more than 3 notes**")
        else:
          newuser = {"id": ctx.author.id, "note": message}
          await notedb.insert_one(newuser)
          await ctx.send("**Yout note has been stored**")
          await ctx.message.delete()

    else:
      await ctx.send("**Message cannot be greater then 50 characters**")

  @commands.command(name="notes", help="Shows your note", usage="Notes")
  @blacklist_check()
  @ignore_check()
  async def notes(self, ctx):
    stats = await notedb.find_one({"id": ctx.author.id})
    if stats is None:
      embed = discord.Embed(
        timestamp=ctx.message.created_at,
        title="Notes",
        description=f"{ctx.author.mention} has no notes",
        color=0x00FFCA,
      )
      await ctx.send(embed=embed)

    else:
      embed = discord.Embed(title="Notes",
                            description=f"Here are your notes",
                            color=0x00FFCA)
      x = notedb.find({"id": ctx.author.id})
      z = 1
      async for i in x:
        msg = i["note"]
        embed.add_field(name=f"Note {z}", value=f"{msg}", inline=False)
        z += 1
      await ctx.send(embed=embed)
    #  await ctx.send("**Please check your private messages to see your notes**")

  @commands.command(name="trashnotes",
                    help="Delete the notes , it's a good practice",
                    usage="Trashnotes",
                    with_app_command=True)
  @blacklist_check()
  @ignore_check()
  async def trashnotes(self, ctx):
    try:
      await notedb.delete_many({"id": ctx.author.id})
      await ctx.send("**Your notes have been deleted , thank you**")
    except:
      await ctx.send("**You have no record**")

                             
    
      



  @commands.hybrid_command(name="ping",help="Check bot's latency.",
                           aliases=["latency"],
                           usage="Checks the bot latency .",
                           with_app_command=True)
  @ignore_check()
  @blacklist_check()
  async def ping(self, ctx):
    embed = discord.Embed(color=0x2C2F33)
    embed.set_author(
        name=f"🏓 |...pong! In {int(self.bot.latency * 1000)} ms ",
        icon_url=ctx.author.display_avatar.url)

    await ctx.reply(embed=embed)



  

  @commands.command(usage="Spotify [user]")
  @blacklist_check()
  @ignore_check()
  async def spotify(self, ctx: Context, user: Member = None):
        '''Tells you what song a user is listening to.'''
        user = user or ctx.author

        if user.activities:
            for activity in user.activities:
                if isinstance(activity, Spotify):
                    embed = Embed(
                        title=f"{user.name}'s Spotify",
                        description=f"Listening to **{activity.title}**",
                        color=activity.color.value if activity.color else 0x1DB954,  # Default color for Spotify
                    )
                    embed.set_image(url=activity.album_cover_url)
                    embed.add_field(name="Artist", value=activity.artist)
                    embed.add_field(name="Album", value=activity.album)
                    embed.add_field(name="Duration", value=f"{activity.duration.total_seconds()//60:.0f} minutes")
                    embed.set_footer(text=f"Started at {activity.created_at.strftime('%H:%M')} UTC")
                    await ctx.send(embed=embed)
                    return  # Stop after finding the first Spotify activity

        # If no Spotify activity is found
        await ctx.send(f"{user.name} is not currently listening to Spotify.")


  @commands.command(usage="Say <message>")
  @blacklist_check()
  @ignore_check()
  async def say(self, ctx, *, message=None):
        '''Make the bot say something.'''
        if message is None:
            await ctx.send("**Please provide a message to say.**")
            return

        await ctx.send(message)

        try:
            await ctx.message.delete()
        except:
            return