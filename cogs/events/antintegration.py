import discord
from discord.ext import commands
from core import Cog, Redox
import logging
from utils.Tools import *
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.INFO,
    format="[\x1b[38;5;197m%(asctime)s\x1b[0m] -> %(message)s",
    datefmt="%H:%M:%S",
)

class AntiIntegration(Cog):
    def __init__(self, client: Redox):
        self.client = client      

    async def apply_punishment(self, member: discord.Member, punishment: str, reason: str):
        try:
            if punishment == "ban":
                await member.ban(reason=reason)
                logging.info(f"Successfully banned {member}")
            elif punishment == "kick":
                await member.kick(reason=reason)
                logging.info(f"Successfully kicked {member}")
            elif punishment == "none":
                roles_to_remove = [role for role in member.roles if role.permissions.administrator]
                if roles_to_remove:
                    await member.remove_roles(*roles_to_remove, reason=reason)
                    logging.info(f"Removed admin roles from {member}")
        except discord.Forbidden:
            logging.warning(f"No permission to punish {member}")
        except discord.HTTPException as e:
            logging.error(f"Failed to punish {member}: {e}")

    @commands.Cog.listener()
    async def on_guild_integrations_update(self, guild: discord.Guild):
        try:
            data = getConfig(guild.id)
            anti = getanti(guild.id)
            punishment = data["punishment"]
            wled = data["whitelisted"]
            wlrole = data['wlrole']
            wlrole_obj = guild.get_role(wlrole)
            reason = "Creating Integration | Not Whitelisted"

            # Check audit logs for the latest integration creation in the last 30 seconds
            async for entry in guild.audit_logs(
                limit=1,
                action=discord.AuditLogAction.integration_create,
                after=datetime.utcnow() - timedelta(seconds=30)
            ):
                user = entry.user
                member = guild.get_member(user.id)

                if user.id == self.client.user.id or user.id == guild.owner_id:
                    continue
                if str(user.id) in wled or anti == "off" or (wlrole_obj in member.roles):
                    continue

                await self.apply_punishment(member, punishment, reason)

        except Exception as e:
            logging.error(f"Error in anti-integration: {e}")
