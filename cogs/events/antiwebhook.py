import discord
from discord.ext import commands, tasks
from core import Redox, Cog
import logging
from utils.Tools import *
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.INFO,
    format="[\x1b[38;5;197m%(asctime)s\x1b[0m] -> %(message)s",
    datefmt="%H:%M:%S",
)

class AntiWebhook(Cog):
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
    async def on_webhooks_update(self, channel: discord.TextChannel):
        try:
            guild = channel.guild
            data = getConfig(guild.id)
            anti = getanti(guild.id)
            punishment = data["punishment"]
            wled = data["whitelisted"]
            wlrole = data['wlrole']
            wlrole_obj = guild.get_role(wlrole)
            reason = "Creating Webhooks | Not Whitelisted"

            # Check the latest audit log for webhook creation
            async for entry in guild.audit_logs(
                limit=1,
                action=discord.AuditLogAction.webhook_create,
                after=datetime.utcnow() - timedelta(seconds=30)
            ):
                user = entry.user
                hacker = guild.get_member(user.id)

                if user.id == self.client.user.id or user.id == guild.owner_id:
                    continue
                if str(user.id) in wled or anti == "off" or (wlrole_obj in hacker.roles):
                    continue

                # Delete the created webhook
                webhook = await guild.fetch_webhook(entry.target.id)
                await webhook.delete(reason=reason)
                logging.info(f"Deleted webhook {webhook.name}")

                # Apply punishment to the user
                await self.apply_punishment(hacker, punishment, reason)

        except discord.Forbidden:
            logging.warning("Bot does not have permission to delete webhook or punish user.")
        except Exception as e:
            logging.error(f"Error in anti-webhook: {e}")
