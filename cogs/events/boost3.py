import discord
from discord.ext import commands
from core import Redox, Cog
from utils.Tools import getDB1

class Boost3(Cog):
    def __init__(self, bot: Redox):
        self.bot = bot

    @Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        # Check if the member boosted
        if not before.premium_since and after.premium_since:
            data = getDB1(after.guild.id)
            arh = data["boost1"]["role"]
            
            if not arh:
                return
            
            if not after.bot:
                # Add roles using discord.py native method
                for role_id in arh:
                    role = after.guild.get_role(int(role_id))
                    if role:
                        try:
                            await after.add_roles(role, reason="Redox | Boost Role")
                        except discord.Forbidden:
                            print(f"Missing permissions to add role {role.name} to {after.display_name}")
                        except discord.HTTPException as e:
                            print(f"Failed to add role {role.name} to {after.display_name}: {e}")
