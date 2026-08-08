import os
import discord
from discord.ext import commands, tasks
from utils.Tools import *
from core import Redox, Cog
import logging

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)


class antiban(Cog):
    def __init__(self, client: Redox):
        self.client = client
        self.processing = []

    @tasks.loop(seconds=15)
    async def clean_processing(self):
        self.processing.clear()

    @commands.Cog.listener()
    async def on_ready(self):
        self.clean_processing.start()

    async def punish(self, guild: discord.Guild, member: discord.Member, punishment: str, reason: str):
        """Helper to apply punishment cleanly"""
        try:
            if punishment == "ban":
                await guild.ban(member, reason=reason)
                logging.info(f"Banned {member} for {reason}")
            elif punishment == "kick":
                await member.kick(reason=reason)
                logging.info(f"Kicked {member} for {reason}")
            elif punishment == "none":
                await member.edit(roles=[r for r in member.roles if not r.permissions.administrator], reason=reason)
                logging.info(f"Removed admin roles from {member} for {reason}")
        except discord.Forbidden:
            logging.warning(f"Missing permissions to punish {member}")
        except Exception as e:
            logging.error(f"Error punishing {member}: {e}")

    # -----------------------------------------------------------
    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.User):
        try:
            data = getConfig(guild.id)
            anti = getanti(guild.id)
            punishment = data["punishment"]
            whitelisted = data["whitelisted"]
            wlrole = data["wlrole"]
            wl_role = guild.get_role(wlrole)
            reason = "Banning Members | Not Whitelisted"

            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
                actor = entry.user
                break
            else:
                return

            if (
                actor.id == self.client.user.id
                or actor.id == guild.owner_id
                or str(actor.id) in whitelisted
                or anti == "off"
            ):
                return

            member = guild.get_member(actor.id)
            if not member:
                return

            if wl_role and wl_role in member.roles:
                return

            # Undo the ban first
            await guild.unban(user, reason="Unauthorized ban")

            # Then punish the actor
            await self.punish(guild, member, punishment, reason)

        except discord.Forbidden:
            logging.warning("Missing permissions to undo ban or punish")
        except Exception as e:
            logging.error(f"on_member_ban error: {e}")

    # -----------------------------------------------------------
    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.User):
        try:
            data = getConfig(guild.id)
            anti = getanti(guild.id)
            punishment = data["punishment"]
            whitelisted = data["whitelisted"]
            wlrole = data["wlrole"]
            wl_role = guild.get_role(wlrole)
            reason = "Unbanning Members | Not Whitelisted"

            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.unban):
                actor = entry.user
                break
            else:
                return

            if (
                actor.id == self.client.user.id
                or actor.id == guild.owner_id
                or str(actor.id) in whitelisted
                or anti == "off"
            ):
                return

            member = guild.get_member(actor.id)
            if not member:
                return

            if wl_role and wl_role in member.roles:
                return

            # Re-ban the victim (user)
            await guild.ban(user, reason="Unauthorized unban")

            # Punish the actor
            await self.punish(guild, member, punishment, reason)

        except discord.Forbidden:
            logging.warning("Missing permissions to reban or punish")
        except Exception as e:
            logging.error(f"on_member_unban error: {e}")
