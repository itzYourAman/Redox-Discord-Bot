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

class AntiPrune(Cog):
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
    async def on_member_remove(self, member: discord.Member):
        try:
            guild = member.guild
            data = getConfig(guild.id)
            anti = getanti(guild.id)
            punishment = data["punishment"]
            wled = data["whitelisted"]
            wlrole = data['wlrole']
            wlrole_obj = guild.get_role(wlrole)
            reason = "Pruned Guild | Not Whitelisted"

            # Check the latest audit logs for prune actions in the last 30 seconds
            async for entry in guild.audit_logs(
                limit=1,
                action=discord.AuditLogAction.member_prune,
                after=datetime.utcnow() - timedelta(seconds=30)
            ):
                user = entry.user
                member_user = guild.get_member(user.id)

                if user.id == self.client.user.id or user.id == guild.owner_id:
                    continue
                if str(user.id) in wled or anti == "off" or (wlrole_obj in member_user.roles):
                    continue

                await self.apply_punishment(member_user, punishment, reason)

        except discord.Forbidden:
            logging.warning("Bot does not have permission to punish member.")
        except Exception as e:
            logging.error(f"Error in anti-prune: {e}")
