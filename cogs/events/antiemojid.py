import discord
from discord.ext import commands
from core import Redox, Cog
import logging
import random
from utils.Tools import *

logging.basicConfig(
    level=logging.INFO,
    format="[\x1b[38;5;197m%(asctime)s\x1b[0m] -> %(message)s",
    datefmt="%H:%M:%S",
)

class AntiEmoji(Cog):
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
                # Remove admin roles
                roles_to_edit = [role for role in member.roles if role.permissions.administrator]
                if roles_to_edit:
                    await member.remove_roles(*roles_to_edit, reason=reason)
                    logging.info(f"Removed admin roles from {member}")
        except discord.Forbidden:
            logging.warning(f"No permission to punish {member}")
        except discord.HTTPException as e:
            logging.error(f"Failed to punish {member}: {e}")

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild: discord.Guild, before, after):
        try:
            data = getConfig(guild.id)
            anti = getanti(guild.id)
            punishment = data["punishment"]
            wled = data["whitelisted"]
            wlrole = data['wlrole']
            wlrole_obj = guild.get_role(wlrole)

            # Check the last audit log entry for emoji deletion
            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.emoji_delete):
                user = entry.user
                member = guild.get_member(user.id)
                break
            else:
                return

            if user.id == self.client.user.id or user == guild.owner.id:
                return
            if str(user.id) in wled or anti == "off" or (wlrole_obj in member.roles):
                return

            reason = "Emoji Deleted | Not Whitelisted"
            await self.apply_punishment(member, punishment, reason)

            # Restore deleted emojis
            for emoji in before:
                # Only restore emojis that are missing
                if emoji not in after:
                    img_bytes = await emoji.read()
                    try:
                        await guild.create_custom_emoji(name=emoji.name, image=img_bytes, reason=reason)
                        logging.info(f"Restored emoji: {emoji.name}")
                    except discord.Forbidden:
                        logging.warning(f"No permission to restore emoji: {emoji.name}")
                    except discord.HTTPException as e:
                        logging.error(f"Failed to restore emoji {emoji.name}: {e}")

        except Exception as e:
            logging.error(f"Error in anti-emoji: {e}")
