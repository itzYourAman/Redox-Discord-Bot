from __future__ import annotations
import discord
import asyncio
import os
import logging
from discord.ext import commands
from utils.Tools import *
from discord.ext.commands import Context
from discord import app_commands
import time
import datetime
import re
from typing import *
from time import strftime
from core import Cog, Redox, Context
from discord.ext import commands

logging.basicConfig(
    level=logging.INFO,
    format=
    "\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)


class Welcomer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot



    @commands.group(name="joindm",
                    aliases=['joinDM'],
                    invoke_without_command=True)
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def joindm(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)


    @_greet.command(name="enable", help="Enables Joindm embed module .")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def enable(self, ctx):
        self.bot.add_listener(self.on_member_join, 'on_member_join')
        msg = discord.Embed(
        color=0x2f3136,
        description=
          f"<:Prime_Tick:1167811945492123799> | Successfully Enabled The JoinDM Module .")
        await ctx.send(embed=msg)

    @_greet.command(name="disable", help="disable Joindm embed module .")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx):
        self.bot.remove_listener(self.on_member_join)
        msg = discord.Embed(
        color=0x2f3136,
        description=
          f"<:Prime_Tick:1167811945492123799> | Successfully Disabled The JoinDM Module .")
        await ctx.send(embed=msg)


  
    @joindm.command(name="message", help="Setups joindm embed message .")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def joindm_message(self, ctx: commands.Context):
        data = getdm(ctx.guild.id)

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            msg = discord.Embed(
                color=0x2f3136,
                description=
                """Here are some keywords, which you can use in your welcome message.\n\nSend your joinDm message in this channel now.\n\n\n```xml\n<<server.member_count>> = server member count\n<<server.name>> = server name\n<<user.name>> = username of new member\n<<user.mention>> = mention of the new user\n<<user.created_at>> = creation time of account of user\n<<user.joined_at>> = joining time of the user.\n```"""
            )
            await ctx.send(embed=msg)
            try:
                dmmsg = await self.bot.wait_for('message',
                                                  check=check,
                                                  timeout=30.0)
            except asyncio.TimeoutError:
                await ctx.send("Oops, too late. bye")
                return
            else:
                data["message"] = dmmsg.content
                updatedm(ctx.guild.id, data)
                hacker = discord.Embed(
                    color=0x2f3136,
                    description=
                    f"<a:tickkk:1130730211382661171> | Successfully updated the welcome message .",
                    timestamp=ctx.message.created_at)
                hacker.set_author(name=f"{ctx.author.name}",
                                  icon_url=f"{ctx.author.avatar}")
                await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(description="""```diff
 - You must have Administrator permission. - Your top role should be above my top role. 
```""",
                                    color=0x2f3136)
            hacker5.set_author(name=f"{ctx.author.name}",
                               icon_url=f"{ctx.author.avatar}")

            await ctx.send(embed=hacker5)

    @_greet.command(name="title", help="Setups Joindm embed title .")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def joindm_title(self, ctx, *, title):
        data = getdm(ctx.guild.id)
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            data['title'] = title
            updatedm(ctx.guild.id, data)
            hacker = discord.Embed(
                color=self.color,
                description=
                f"<:Prime_Tick:1167811945492123799> | Successfully updated the joinDM title .")
            hacker.set_author(name=ctx.author,
                          icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(description="""```diff
- You must have Administrator permission. - Your top role should be above my top role. 
```""",
                                    color=self.color)
            hacker5.set_author(name=ctx.author,
                           icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)

    @_greet.command(name="title", help="Setups Joindm embed title .")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def test(self, ctx):
     # Send a test join DM to the author of the command
      guild_id = str(ctx.guild.id)
      if guild_id in self.joindm_messages:
          message = self.joindm_messages[guild_id]
          server_name = ctx.guild.name
          join_dm_message = f"{message}\n\n ``Sent from {server_name} `` "
          await ctx.send("<a:Cosy_girl_shy:1138852464033013790> Test Sent To Your Dm")
         await ctx.message.add_reaction("<a:blobpart:1138731079977668618>")
         await ctx.author.send(join_dm_message)
     else:
         await ctx.send("**<a:crossss:1131829269509709875> |No custom join DM message has been set for this server.**")