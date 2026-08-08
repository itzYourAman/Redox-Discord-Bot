import discord
import json
from discord.ext import commands
from core import Redox, Cog, Context
from utils.Tools import *


class Errors(Cog):
    def __init__(self, client: Redox):
        self.client = client
        with open('data/json/blacklist.json', 'r', encoding="utf-8") as f:
            self.blacklist_data = json.load(f)
        self.web = "https://discord.com/api/webhooks/1218189207575593071/jfyR4pMHeXWB00EmNKdOMbm3UBGG-V3uEsYmUTORsLEbVa8yi54hWmh60tddlTcKdTzc"
        self.channel=1218183303694254240

    @Cog.listener()
    async def on_command_completion(self, context: Context) -> None:
      await self.client.wait_until_ready()
      full_command_name = context.command.qualified_name
      split = full_command_name.split("\n")
      executed_command = str(split[0])
      if not context.message.content.startswith("$"):
        pcmd = f"`{context.message.content}`"
      else:
        pcmd = f"`{context.message.content}`"
      if context.guild is not None:
        try:
            
            embed = discord.Embed(color=0x2f3136)
            embed.set_author(
                name=
                f"Executed {executed_command} Command By : {context.author}",
                icon_url=f"{context.author.avatar}")
            embed.set_thumbnail(url=f"{context.author.avatar}")
            embed.add_field(
                name="Command Name :",
                value=f"{executed_command}",
                inline=False)
            embed.add_field(
                name="Command Content :",
                value="{}".format(pcmd),
                inline=False)
            embed.add_field(
                name="Command Executed By :",
                value=
                f"{context.author} | ID: [{context.author.id}](https://discord.com/users/{context.author.id})",
                inline=False)
            embed.add_field(
                name="Command Executed In :",
                value=
                f"{context.guild.name}  | ID: [{context.guild.id}](https://discord.com/users/{context.author.id})",
                inline=False)
            embed.add_field(
                name=
                "Command Executed In Channel :",
                value=
                f"{context.channel.name}  | ID: [{context.channel.id}](https://discord.com/channel/{context.channel.id})",
                inline=False)
            embed.set_footer(text=f"Thank you for choosing  {self.client.user.name}",
                             icon_url=self.client.user.display_avatar.url)
            try:
               webhook = discord.SyncWebhook.from_url(self.web)
               webhook.send(embed=embed)
            except:
               channel = self.client.get_channel(self.channel)
               await channel.send(embed=embed)
        except:
            print('LOL')
      else:
        try:

            embed1 = discord.Embed(color=0x2f3136)
            embed1.set_author(
                name=
                f"Executed {executed_command} Command By : {context.author}",
                icon_url=f"{context.author.avatar}")
            embed1.set_thumbnail(url=f"{context.author.avatar}")
            embed1.add_field(
                name="Command Name :",
                value=f"{executed_command}",
                inline=False)
            embed1.add_field(
                name="Command Executed By :",
                value=
                f"{context.author} | ID: [{context.author.id}](https://discord.com/users/{context.author.id})",
                inline=False)
            embed1.set_footer(text=f"Thank you for choosing  {self.client.user.name}",
                              icon_url=self.client.user.display_avatar.url)
            try:
               webhook = discord.SyncWebhook.from_url(self.web)
               webhook.send(embed=embed1)
            except discord.NotFound:
               channel = self.client.get_channel(self.channel)
               await channel.send(embed=embed1)
        except:
            print("Lowl") 

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        data1 = getIgnore(ctx.guild.id)
        ch = data1["channel"]
        iuser = data1["user"]

        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)
            return

        # Check for Blacklist-related errors
        if isinstance(error, commands.CheckFailure):
            if str(ctx.author.id) in self.blacklist_data["ids"]:
                # Handle Blacklist error
                bl = discord.Embed(description="You are blacklisted from using my commands.\nreason could be excessive use or spamming commands\nJoin our [Support Server](https://discord.gg/oxytech) to appeal.", color=discord.Colour(0x2f3136))
                await ctx.reply(embed=bl, mention_author=False, delete_after=8)
                return

            # Check for Ignore-related errors
            if str(ctx.channel.id) in ch:
                await ctx.reply(embed=discord.Embed(description="This Channel is in the ignored channel list. Try my commands in another channel.", color=discord.Colour(0x2f3136)), delete_after=8)
                return

            if str(ctx.author.id) in iuser:
                await ctx.reply(embed=discord.Embed(description=f"You are set as an ignored user for {ctx.guild.name}.\nTry my commands or modules in another guild.", color=discord.Colour(0x2f3136)), delete_after=8)
                return

        if isinstance(error, commands.NoPrivateMessage):
            hacker = discord.Embed(color=0x2f3136, description="You Can't Use My Commands In Dm(s)")
            hacker.set_author(name=ctx.author, icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            hacker.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker, delete_after=20)
            return

        if isinstance(error, commands.TooManyArguments):
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)
            return

        if isinstance(error, commands.CommandOnCooldown):
            hacker = discord.Embed(color=0x2f3136, description=f"<a:crossss:1131829269509709875> | {ctx.author.name} is on cooldown retry after {error.retry_after:.2f} second(s)")
            hacker.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            hacker.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker, delete_after=10)
            return

        if isinstance(error, commands.MaxConcurrencyReached):
            hacker = discord.Embed(color=0x2f3136, description="<a:crossss:1131829269509709875> | This Command is already going on, let it finish and retry after")
            hacker.set_author(name=ctx.author, icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            hacker.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=hacker, delete_after=10)
            ctx.command.reset_cooldown(ctx)
            return
        if isinstance(error, commands.MissingPermissions):
            member =  ctx.author if isinstance(ctx.author, discord.Member) else ctx.guild.get_member(ctx.author.id)
            missing = [
                perm.replace("_", " ").replace("guild", "server").title()
                for perm in error.missing_permissions
            ]
            fmt = ", and ".join(missing) if len(missing) > 1 else "".join(missing)
            
            hacker = discord.Embed(color=0x2f3136, description=f"<a:crossss:1131829269509709875> | You lack `{fmt}` permission(s) to run `{ctx.command.name}` command!")
            
            # Check if the bot can send messages in the channel
            if ctx.channel.permissions_for(ctx.guild.me).send_messages:
                await ctx.reply(embed=hacker, delete_after=6)
            else:
                await ctx.author.send(embed=hacker)  # Send the embed as a DM if the bot can't send messages in the channel
            
            ctx.command.reset_cooldown(ctx)
            return

        if isinstance(error, commands.BadArgument):
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)
            return

        if isinstance(error, commands.BotMissingPermissions):
            missing = ", ".join(error.missing_perms)
            await ctx.send(f'<a:crossss:1131829269509709875> | I need the **{missing}** to run the **{ctx.command.name}** command!', delete_after=10)
            return
        if isinstance(error, discord.Forbidden):
            missing_permissions = error.missing_perms
            try:
                await ctx.send(f"I'm sorry, I don't have Enough Permissions Tor Run This  Command. I Require {missing_permissions} To Run This Command.")
                return
            except:
                await ctx.author.send("I don't have permission to send messages in that channel.")
            return
       # else:
         # print(f"An error occurred: {error}")
