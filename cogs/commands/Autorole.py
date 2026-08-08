from  __future__ import annotations
import discord
import logging
from discord.ext import commands
from utils.Tools import *
from typing import *
from discord.ext import commands

logging.basicConfig(
    level=logging.INFO,
    format=
    "\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)



class BasicView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout = 60):
        super().__init__(timeout=timeout)
        self.ctx = ctx

    
      
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in [926831289649201213]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command .", ephemeral=True)
            return False
        return True
    
    
    
    
class Autodel(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None
        
    @discord.ui.button(label="10s", custom_id='ten', style=discord.ButtonStyle.green)
    async def _10(self, interaction, button):
        self.value = '10'
        self.stop()

    @discord.ui.button(label="15s", custom_id='fifteen', style=discord.ButtonStyle.green)
    async def _15(self, interaction, button):
        self.value = '15'
        self.stop()

    @discord.ui.button(label="20s", custom_id='twenty', style=discord.ButtonStyle.green)
    async def _20(self, interaction, button):
        self.value = '20'
        self.stop()

    @discord.ui.button(label="25s", custom_id='twentyfive', style=discord.ButtonStyle.green)
    async def _25(self, interaction, button):
        self.value = '25'
        self.stop()

    @discord.ui.button(label="30s", custom_id='thirty', style=discord.ButtonStyle.green)
    async def _30(self, interaction, button):
        self.value = '30'
        self.stop()
        
        
        

class autorole(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.color = 0x2f3136

    @commands.group(name="autorole", invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @blacklist_check()
    @ignore_check()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_autorole.command(name="config")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _ar_config(self, ctx):
        if data := getautorole(ctx.guild.id):
            hum = list(data["humanautoroles"])
            bo = list(data["botautoroles"])

            fetched_humans: list = []
            fetched_bots: list = []

            for i in hum:
                role = ctx.guild.get_role(int(i))
                if role is not None:
                    fetched_humans.append(role)

            for i in bo:
                role = ctx.guild.get_role(int(i))
                if role is not None:
                    fetched_bots.append(role)

            hums = "\n".join(i.mention for i in fetched_humans)
            if not hums:
                hums = " Humans Autorole Not Set."

            bos = "\n".join(i.mention for i in fetched_bots)
            if not bos:
                bos = " Bots Autorole Not Set."

            emb = discord.Embed(
                color=self.color,
                title=f"Autorole of - {ctx.guild.name}").add_field(
                    name="__Humans__", value=hums,
                    inline=False).add_field(name="__Bots__",
                                            value=bos,
                                            inline=False)

            await ctx.send(embed=emb)

    @_autorole.group(name="reset",
                     help="Clear autorole config for the server .")
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _autorole_reset(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_autorole_reset.command(name="humans",
                             help="Clear autorole config for the server .")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _autorole_humans_reset(self, ctx):
        data = getautorole(ctx.guild.id)
        rl = data["humanautoroles"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if rl == []:
                embed = discord.Embed(
                    description=
                    "<a:crossss:1174609979932684328> | This server don't have any autoroles setupped .",
                    color=self.color)
                await ctx.send(embed=embed)
            else:
                if rl != []:
                    data["humanautoroles"] = []
                    updateautorole(ctx.guild.id, data)
                    hacker = discord.Embed(
                        description=
                        f"<a:tickkk:1174609776206950430> | Succesfully cleared all human autoroles for {ctx.guild.name} .",
                        color=self.color)
                    await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)

    @_autorole_reset.command(name="bots")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _autorole_bots_reset(self, ctx):
        data = getautorole(ctx.guild.id)
        rl = data["botautoroles"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if rl == []:
                embed = discord.Embed(
                    description=
                    f"<a:crossss:1174609979932684328> | This server don't have any autoroles setupped .",
                    color=self.color)
                await ctx.send(embed=embed)
            else:
                if rl != []:
                    data["botautoroles"] = []
                    updateautorole(ctx.guild.id, data)
                    hacker = discord.Embed(
                        description=
                        f"<a:tickkk:1174609776206950430> | Succesfully cleared all bot autoroles for this server .",
                        color=self.color)
                    await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)

    @_autorole_reset.command(name="all")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_reset_all(self, ctx):
        data = getautorole(ctx.guild.id)
        brl = data["botautoroles"]
        hrl = data["humanautoroles"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if len(brl) == 0 and len(hrl) == 0:
                embed = discord.Embed(
                    description=
                    f"<a:crossss:1174609979932684328> | This server don't have any autoroles setupped .",
                    color=self.color)
                await ctx.send(embed=embed)
            else:
                if hrl != []:
                    data["botautoroles"] = []
                    data["humanautoroles"] = []
                    updateautorole(ctx.guild.id, data)
                    hacker = discord.Embed(
                        description=
                        f"<a:tickkk:1174609776206950430> | Succesfully cleared all autoroles for this server .",
                        color=self.color)
                    await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)

    @_autorole.group(name="humans", help="Setup autoroles for human users.")
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_humans(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_autorole_humans.command(name="add",
                              help="Add role to list of autorole humans users."
                              )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_humans_add(self, ctx, *, role: discord.Role):
        data = getautorole(ctx.guild.id)
        rl = data["humanautoroles"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if len(rl) == 10:
                embed = discord.Embed(
                    description=
                    f"<a:crossss:1174609979932684328> | You have reached maximum channel limit for autorole humans which is ten .",
                    color=self.color)
                await ctx.send(embed=embed)
            else:
                if str(role.id) in rl:
                    embed1 = discord.Embed(
                        description=
                        "<a:crossss:1174609979932684328> | {} is already in human autoroles ."
                        .format(role.mention),
                        color=self.color)
                    await ctx.send(embed=embed1)
                else:
                    rl.append(str(role.id))
                    updateautorole(ctx.guild.id, data)
                    hacker = discord.Embed(
                        description=
                        f"<a:tickkk:1174609776206950430> | {role.mention} has been added to human autoroles .",
                        color=self.color)
                    await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)

    @_autorole_humans.command(
        name="remove", help="Remove a role from autoroles for human users.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_humans_remove(self, ctx, *, role: discord.Role):
        data = getautorole(ctx.guild.id)
        rl = data["humanautoroles"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if len(rl) == 0:
                embed = discord.Embed(
                    description=
                    f"<a:crossss:1174609979932684328> | This server dont have any autrole humans setupped yet .",
                    color=self.color)
                await ctx.send(embed=embed)
            else:
                if str(role.id) not in rl:
                    embed1 = discord.Embed(
                        description="{} is not in human autoroles .".format(
                            role.mention),
                        color=self.color)
                    await ctx.send(embed=embed1)
                else:
                    rl.remove(str(role.id))
                    updateautorole(ctx.guild.id, data)
                    hacker = discord.Embed(
                        description=
                        f"<a:tickkk:1174609776206950430> | {role.mention} has been removed from human autoroles .",
                        color=self.color)
                    await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)

    @_autorole.group(name="bots", help="Setup autoroles for bots.")
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_bots(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_autorole_bots.command(name="add",
                            help="Add role to list of autorole bot users.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_bots_add(self, ctx, *, role: discord.Role):
        data = getautorole(ctx.guild.id)
        rl = data["botautoroles"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if len(rl) == 5:
                embed = discord.Embed(
                    description=
                    f"<a:crossss:1174609979932684328> | You have reached maximum role limit for autorole bots which is five.",
                    color=self.color)
                await ctx.send(embed=embed)
            else:
                if str(role.id) in rl:
                    embed1 = discord.Embed(
                        description=
                        "<a:crossss:1174609979932684328> | {} is already in bot autoroles."
                        .format(role.mention),
                        color=self.color)
                    await ctx.send(embed=embed1)
                else:
                    rl.append(str(role.id))
                    updateautorole(ctx.guild.id, data)
                    hacker = discord.Embed(
                        description=
                        f"<a:tickkk:1174609776206950430> | {role.mention} has been added to bot autoroles .",
                        color=self.color)
                    await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)

    @_autorole_bots.command(name="remove",
                            help="Remove a role from autoroles for bot users.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_bots_remove(self, ctx, *, role: discord.Role):
        data = getautorole(ctx.guild.id)
        rl = data["botautoroles"]
        if ctx.author == ctx.guild.owner or ctx.author.top_role.position > ctx.guild.me.top_role.position:
            if len(rl) == 0:
                embed = discord.Embed(
                    description=
                    f"<a:crossss:1174609979932684328> | This server dont have any autrole humans setupped yet .",
                    color=self.color)
                await ctx.send(embed=embed)
            else:
                if str(role.id) not in rl:
                    embed1 = discord.Embed(
                        description=
                        "<a:crossss:1174609979932684328> | {} is not in bot autoroles."
                        .format(role.mention),
                        color=self.color)
                    await ctx.send(embed=embed1)
                else:
                    rl.remove(str(role.id))
                    updateautorole(ctx.guild.id, data)
                    hacker = discord.Embed(
                        description=
                        f"<a:tickkk:1174609776206950430> | {role.mention} has been removed from bot autoroles.",
                        color=self.color)
                    await ctx.send(embed=hacker)
        else:
            hacker5 = discord.Embed(
                description=
                """```diff\n - You must have Administrator permission.\n - Your top role should be above my top role. \n```""",
                color=self.color)
            hacker5.set_author(name=ctx.author,
                               icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

            await ctx.send(embed=hacker5)