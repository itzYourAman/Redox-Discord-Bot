import discord
from discord.ext import commands, tasks
from itertools import cycle
from core import Redox, Cog
import datetime
import logging
import time
import random
from utils.Tools import *

logging.basicConfig(
    level=logging.INFO,
    format="[\x1b[38;5;197m%(asctime)s\x1b[0m] -> %(message)s",
    datefmt="%H:%M:%S",
)

class Antichannel(Cog):
    def __init__(self, client: Redox):
        self.client = client      
        self.processing = []

    @tasks.loop(seconds=15)
    async def clean_processing(self):
        self.processing.clear()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.clean_processing.start()

    async def safe_delete(self, channel: discord.abc.GuildChannel):
        try:
            await channel.delete()
        except discord.Forbidden:
            logging.warning(f"Cannot delete channel {channel.name}")
        except discord.HTTPException as e:
            logging.error(f"Failed to delete channel {channel.name}: {e}")

    async def apply_punishment(self, member: discord.Member, punishment: str, reason: str):
        try:
            if punishment == "ban":
                await member.ban(reason=reason)
                logging.info(f"Successfully banned {member}")
            elif punishment == "kick":
                await member.kick(reason=reason)
                logging.info(f"Successfully kicked {member}")
            elif punishment == "none":
                # Remove admin permissions
                roles_to_edit = [role for role in member.roles if role.permissions.administrator]
                if roles_to_edit:
                    await member.remove_roles(*roles_to_edit, reason=reason)
                    logging.info(f"Removed admin roles from {member}")
        except discord.Forbidden:
            logging.warning(f"No permission to punish {member}")
        except discord.HTTPException as e:
            logging.error(f"Failed to punish {member}: {e}")

    async def check_entry(self, guild: discord.Guild, action: discord.AuditLogAction):
        async for entry in guild.audit_logs(limit=1, action=action):
            return entry
        return None

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        try:
            start = time.perf_counter()
            data = getConfig(channel.guild.id)
            anti = getanti(channel.guild.id)
            punishment = data["punishment"]
            wlrole = data['wlrole']
            wled = data["whitelisted"]
            guild = channel.guild
            wlrole_obj = guild.get_role(wlrole)

            entry = await self.check_entry(guild, discord.AuditLogAction.channel_create)
            if not entry:
                return

            user = entry.user
            if user.id == self.client.user.id or user.id == guild.owner_id or str(user.id) in wled or anti == "off" or (wlrole_obj in user.roles):
                return

            reason = "Channel Created | Not Whitelisted"
            await self.apply_punishment(user, punishment, reason)
            await self.safe_delete(channel)

            end = time.perf_counter()
            logging.info(f"Processed {user} in {round((end-start)*1000)}ms")
        except Exception as e:
            logging.error(e)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        try:
            data = getConfig(channel.guild.id)
            anti = getanti(channel.guild.id)
            punishment = data["punishment"]
            wlrole = data['wlrole']
            wled = data["whitelisted"]
            guild = channel.guild
            wlrole_obj = guild.get_role(wlrole)

            entry = await self.check_entry(guild, discord.AuditLogAction.channel_delete)
            if not entry:
                return

            user = entry.user
            if user.id == self.client.user.id or user == guild.owner or str(user.id) in wled or anti == "off" or (wlrole_obj in user.roles):
                return

            reason = "Channel Deleted | Not Whitelisted"
            await self.apply_punishment(user, punishment, reason)
            # Recreate the channel
            new_channel = await channel.clone(reason=reason)
            await new_channel.edit(category=channel.category, position=channel.position)
        except Exception as e:
            logging.error(e)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        try:
            data = getConfig(before.guild.id)
            anti = getanti(before.guild.id)
            punishment = data["punishment"]
            wlrole = data['wlrole']
            wled = data["whitelisted"]
            guild = after.guild
            wlrole_obj = guild.get_role(wlrole)

            # Check audit log for recent channel update
            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_update,
                                               after=datetime.datetime.utcnow() - datetime.timedelta(seconds=30)):
                user = entry.user
                break
            else:
                return

            if user.id == self.client.user.id or user == guild.owner or str(user.id) in wled or anti == "off" or (wlrole_obj in user.roles):
                return

            reason = "Channel Updated | Not Whitelisted"
            await self.apply_punishment(user, punishment, reason)

            # Revert channel changes
            await after.edit(
                name=before.name,
                topic=before.topic,
                nsfw=before.nsfw,
                category=before.category,
                slowmode_delay=before.slowmode_delay,
                overwrites=before.overwrites,
                reason=reason
            )
        except Exception as e:
            logging.error(e)
