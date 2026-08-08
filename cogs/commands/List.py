
import discord
from discord.ext import commands
from utils import Paginator, DescriptionEmbedPaginator
from utils.Tools import blacklist_check, ignore_check

async def create_paginated_embed(ctx, title, entries, color):
    paginator = Paginator(
        source=DescriptionEmbedPaginator(entries=entries, title=title, description="", per_page=10, color=color),
        ctx=ctx
    )
    await paginator.paginate()

class list(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="list")
    async def jija(self, ctx: commands.Context):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @jija.command(name="boost", aliases=["boosters", "booster", "bst", "boosted", "bsted", "bost"], description="See a list of boosters in the server")
    @blacklist_check()
    @ignore_check()
    async def seggs(self, ctx):
        '''ᗣ See a list of boosters in the server.'''
        l = []
        for member in sorted(ctx.guild.premium_subscribers, key=lambda m: m.premium_since or discord.utils.utcnow()):
            l.append(f"{member.display_name} [{member.mention}] - <t:{round(member.premium_since.timestamp())}:R>")
        if not l:
            return await ctx.send("No booster found in this server :(")
        await create_paginated_embed(ctx, f"List of Boosters in {ctx.guild.name} - {len(l)}", l, 0x41eeee)

    @jija.command(name="joinpos", aliases=["joinposi", "joinposition"])
    @blacklist_check()
    @ignore_check()
    async def seggss(self, ctx):
        '''See a List of Join Position in the server'''
        l = []
        for member in sorted(ctx.guild.members, key=lambda m: m.joined_at or discord.utils.utcnow()):
            l.append(f"{member.display_name} [{member.mention}] - Joined at <t:{round(member.joined_at.timestamp())}:R>")
        await create_paginated_embed(ctx, f"List of Join Position in {ctx.guild.name} - {len(l)}", l, 0x41eeee)

    @jija.command(name="noroles", aliases=["noroless", "norole"])
    @blacklist_check()
    @ignore_check()
    async def seggsss(self, ctx):
        '''See a List of Members without roles in the server'''
        l = [member for member in ctx.guild.members if len(member.roles) == 1]
        if not l:
            return await ctx.send("Bruh, there are no members without any role.")
        entries = [f"{member.display_name} [{member.mention}]" for member in l]
        await create_paginated_embed(ctx, f"List of users without any role - {len(l)}", entries, 0x41eeee)

    @jija.command(name="emojis", aliases=["emo", "emoji"])
    @blacklist_check()
    @ignore_check()
    async def seggssss(self, ctx):
        '''See a List of Emojis in the server.'''
        l = [str(emoji) for emoji in ctx.guild.emojis]
        await create_paginated_embed(ctx, f"List of Emojis in {ctx.guild.name} - {len(l)}", l, 0x41eeee)

    @jija.command(name="bots", aliases=["bot"], description="Get a list of all bots in a server")
    @blacklist_check()
    @ignore_check()
    async def bots(self, ctx):
        '''Get a list of All Bots in a server.'''
        l = [member for member in ctx.guild.members if member.bot]
        if not l:
            return await ctx.send("No Bots Found")
        entries = [f"{member.display_name} [{member.mention}]" for member in l]
        await create_paginated_embed(ctx, f"Bots in {ctx.guild.name} - {len(l)}", entries, 0x41eeee)

    @jija.command(name="admins", aliases=["admin", "administrator", "administration"], description="Get a list of all admins of a server")
    @blacklist_check()
    @ignore_check()
    async def admins(self, ctx):
        '''Get a list of All Admins of a server .'''
        l = [member for member in ctx.guild.members if member.guild_permissions.administrator]
        if not l:
            return await ctx.send("Cannot find any admin in this server.")
        entries = [f"{member.display_name} [{member.mention}]" for member in l]
        await create_paginated_embed(ctx, f"Admins in {ctx.guild.name} - {len(l)}", entries, 0x41eeee)

    @jija.command(name="mods", aliases=["mod", "moderator"], description="Get a list of all mods of a server")
    @blacklist_check()
    @ignore_check()
    async def mods(self, ctx):
        '''Get a list of All Mods of a server .'''
        l = [member for member in ctx.guild.members if (member.guild_permissions.manage_guild or member.guild_permissions.manage_messages or member.guild_permissions.manage_channels or member.guild_permissions.manage_nicknames or member.guild_permissions.manage_roles or member.guild_permissions.manage_emojis_and_stickers or member.guild_permissions.manage_emojis or member.guild_permissions.moderate_members) and not member.guild_permissions.administrator]
        if not l:
            return await ctx.send("Cannot find any mod in this server. (Admins are not included)")
        entries = [f"{member.display_name} [{member.mention}]" for member in l]
        await create_paginated_embed(ctx, f"Mods in {ctx.guild.name} - {len(l)}", entries, 0x41eeee)

    @jija.command(name="early", aliases=["earlybadge", "earlysupporter"], description="Get a list of early id in a server")
    @blacklist_check()
    @ignore_check()
    async def early(self, ctx):
        '''Get a list of Early Id in a server.'''
        l = [member for member in ctx.guild.members if member.public_flags.early_supporter]
        if not l:
            return await ctx.send("No Early Supporter Found")
        entries = [f"{member.display_name} [{member.mention}]" for member in l]
        await create_paginated_embed(ctx, f"Early Id's in {ctx.guild.name} - {len(l)}", entries, 0x41eeee)

    @jija.command(name="active-dev", aliases=["activedev", "activedeveloper"], description="Get a list of early id in a server")
    @blacklist_check()
    @ignore_check()
    async def activedev(self, ctx):
        '''Get a list of Early Id in a server.'''
        l = [member for member in ctx.guild.members if member.public_flags.active_developer]
        if not l:
            return await ctx.send("No Active Developers Found")
        entries = [f"{member.display_name} [{member.mention}]" for member in l]
        await create_paginated_embed(ctx, f"Active Developer's in {ctx.guild.name} - {len(l)}", entries, 0x41eeee)

    @jija.command(name="botdev", aliases=["developer", "botdeveloper"], description="Get a list of bot developer in a server")
    @blacklist_check()
    @ignore_check()
    async def botdev(self, ctx):
        '''Get a list of Bot Developers in a server.'''
        l = [member for member in ctx.guild.members if member.public_flags.early_verified_bot_developer]
        if not l:
            return await ctx.send("No Bot Developers Found")
        entries = [f"{member.display_name} [{member.mention}]" for member in l]
        await create_paginated_embed(ctx, f"List of developer in {ctx.guild.name} - {len(l)}", entries, 0x41eeee)

    @jija.command(name="inrole", aliases=["inside-role"], description="See a list of members that are in the separate role")
    @blacklist_check()
    @ignore_check()
    async def list_inrole(self, ctx, role: discord.Role):
        '''ᗣ See a list of members that are in the specified role .'''
        l = role.members
        entries = [f"{member.display_name} [{member.mention}]" for member in l]
        await create_paginated_embed(ctx, f"List of members in {role.name} - {len(l)}", entries, 0x41eeee)

    @jija.command(name="bans", aliases=["ban"], description="See a list of banned user")
    @blacklist_check()
    @ignore_check()
    async def list_bans(self, ctx):
        '''Shows The List of Banned users.'''
        ok = []
        async for ban_entry in ctx.guild.bans(limit=None):
            user = ban_entry.user
            ok.append(user)
        if not ok:
            return await ctx.send("There aren't any banned users")
        entries = [f"{user.display_name} [{user.mention}]" for user in ok]
        await create_paginated_embed(ctx, f"List of Banned users in {ctx.guild.name} - {len(ok)}", entries, 0x41eeee)

        



    @jija.command(name="roles", invoke_without_command=True, aliases=['role'])
    @blacklist_check()
    @ignore_check()
    async def listroles(self, ctx: commands.Context):
        '''Lists all roles in the server.'''
        roles = ctx.guild.roles
        if not roles:
            return await ctx.send("No roles found in this server.")
        
        entries = [f"{role.mention} - {len(role.members)} members" for role in roles]
        await create_paginated_embed(ctx, f"List of Roles in {ctx.guild.name} - {len(roles)}", entries, 0x41eeee)
