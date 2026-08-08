import discord
from discord.ext import commands, tasks
import datetime
import random
import logging
from itertools import cycle
from core import Redox, Cog
from utils.Tools import *

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

proxies = open('data/proxies.txt').read().split('\n')
proxs = cycle(proxies)
proxies = {"http": 'http://' + next(proxs)}

class antirole(Cog):
    def __init__(self, client: Redox):
        self.client = client
        self.processing = []

    @tasks.loop(seconds=15)
    async def clean_processing(self):
        self.processing.clear()

    @commands.Cog.listener()
    async def on_ready(self):
        self.clean_processing.start()

    # -----------------------------------------------------
    # Helper function
    async def punish(self, guild: discord.Guild, user: discord.Member, punishment: str, reason: str):
        try:
            if punishment == "ban":
                await guild.ban(user, reason=reason)
                logging.info(f"Banned {user} for {reason}")
            elif punishment == "kick":
                await user.kick(reason=reason)
                logging.info(f"Kicked {user} for {reason}")
            elif punishment == "none":
                await user.edit(roles=[r for r in user.roles if not r.permissions.administrator], reason=reason)
                logging.info(f"Removed admin roles from {user} for {reason}")
        except discord.Forbidden:
            logging.warning(f"Missing permissions to punish {user}")
        except Exception as e:
            logging.error(f"Error punishing {user}: {e}")

    # -----------------------------------------------------
    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        try:
            guild = role.guild
            anti = getanti(guild.id)
            data = getConfig(guild.id)
            punishment = data["punishment"]
            wled = data["whitelisted"]
            wlrole = data["wlrole"]

            reason = "Creating Roles | Not Whitelisted"
            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create):
                actor = entry.user
                break
            else:
                return

            if (
                actor.id == self.client.user.id
                or actor.id == guild.owner_id
                or str(actor.id) in wled
                or anti == "off"
            ):
                return

            member = guild.get_member(actor.id)
            if member is None:
                return

            wlroles = guild.get_role(wlrole)
            if wlroles in member.roles:
                return

            await self.punish(guild, member, punishment, reason)
            await role.delete(reason=reason)

        except Exception as e:
            logging.error(f"Role Create Error: {e}")

    # -----------------------------------------------------
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        try:
            guild = role.guild
            anti = getanti(guild.id)
            data = getConfig(guild.id)
            punishment = data["punishment"]
            wled = data["whitelisted"]
            wlrole = data["wlrole"]

            reason = "Deleting Roles | Not Whitelisted"
            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
                actor = entry.user
                break
            else:
                return

            if (
                actor.id == self.client.user.id
                or actor.id == guild.owner_id
                or str(actor.id) in wled
                or anti == "off"
            ):
                return

            member = guild.get_member(actor.id)
            if member is None:
                return

            wlroles = guild.get_role(wlrole)
            if wlroles in member.roles:
                return

            await self.punish(guild, member, punishment, reason)

            # Restore deleted role
            if not role.is_bot_managed() and not role.is_integration():
                restored = await guild.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    hoist=role.hoist,
                    mentionable=role.mentionable,
                    colour=role.colour,
                    reason="Restoring deleted role"
                )
                await restored.edit(position=int(role.position))
                logging.info(f"Restored deleted role {role.name}")

        except Exception as e:
            logging.error(f"Role Delete Error: {e}")

    # -----------------------------------------------------
    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        try:
            guild = after.guild
            anti = getanti(guild.id)
            data = getConfig(guild.id)
            punishment = data["punishment"]
            wled = data["whitelisted"]
            wlrole = data["wlrole"]

            reason = "Updating Roles | Not Whitelisted"
            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_update):
                actor = entry.user
                break
            else:
                return

            if (
                actor.id == self.client.user.id
                or actor.id == guild.owner_id
                or str(actor.id) in wled
                or anti == "off"
            ):
                return

            member = guild.get_member(actor.id)
            if member is None:
                return

            wlroles = guild.get_role(wlrole)
            if wlroles in member.roles:
                return

            await self.punish(guild, member, punishment, reason)
            await after.edit(
                name=before.name,
                permissions=before.permissions,
                colour=before.colour,
                hoist=before.hoist,
                mentionable=before.mentionable,
                reason="Restored due to unauthorized update"
            )

        except Exception as e:
            logging.error(f"Role Update Error: {e}")
