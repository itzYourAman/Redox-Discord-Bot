import discord
from discord.ext import commands, tasks
from core import Cog, Redox
import logging
from utils.Tools import *

logging.basicConfig(
    level=logging.INFO,
    format="[\x1b[38;5;197m%(asctime)s\x1b[0m] -> %(message)s",
    datefmt="%H:%M:%S",
)

class AntiGuild(Cog):
    def __init__(self, client: Redox):
        self.client = client
        self.processing = []

    @tasks.loop(seconds=15)
    async def clean_processing(self):
        self.processing.clear()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.clean_processing.start()

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
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        try:
            data = getConfig(before.id)
            anti = getanti(before.id)
            punishment = data["punishment"]
            wled = data["whitelisted"]
            wlrole = data['wlrole']
            wlrole_obj = after.get_role(wlrole)
            reason = "Updating Guild | Not Whitelisted"

            # Fetch the latest guild update audit log
            async for entry in after.audit_logs(limit=1, action=discord.AuditLogAction.guild_update):
                user = entry.user
                member = after.get_member(user.id)
                break
            else:
                return

            # Skip whitelisted users, owner, or bot itself
            if user.id == self.client.user.id or user.id == after.owner_id:
                return
            if str(user.id) in wled or anti == "off" or (wlrole_obj in member.roles):
                return

            # Apply punishment
            await self.apply_punishment(member, punishment, reason)

            # Revert changes to the guild
            guild_edit_kwargs = {
                "name": before.name,
                "description": before.description,
                "verification_level": before.verification_level,
                "rules_channel": before.rules_channel,
                "afk_channel": before.afk_channel,
                "afk_timeout": before.afk_timeout,
                "default_notifications": before.default_notifications,
                "explicit_content_filter": before.explicit_content_filter,
                "system_channel": before.system_channel,
                "system_channel_flags": before.system_channel_flags,
                "public_updates_channel": before.public_updates_channel,
                "premium_progress_bar_enabled": getattr(before, "premium_progress_bar_enabled", None)
            }

            # Handle guild icon
            if before.icon:
                icon_bytes = await before.icon.read()
                guild_edit_kwargs["icon"] = icon_bytes
            else:
                guild_edit_kwargs["icon"] = None

            await after.edit(**guild_edit_kwargs, reason=reason)

        except discord.Forbidden:
            logging.warning("Bot does not have permission to revert guild changes or punish member.")
        except Exception as e:
            logging.error(f"Error in anti-guild update: {e}")
