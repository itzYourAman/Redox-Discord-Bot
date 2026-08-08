import discord
from discord.ext import commands
from core import Cog, Redox, Context
from utils.Tools import *
from typing import *


class greet(Cog):
    def __init__(self, bot: Redox):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        data = getautorole(member.guild.id)
        bot_roles = data.get("botautoroles", [])
        human_roles = data.get("humanautoroles", [])
        reason = f"{self.bot.user.name} | Autorole"

        roles_to_assign = bot_roles if member.bot else human_roles

        if not roles_to_assign:
            return  # Nothing to assign

        for role_id in roles_to_assign:
            role = member.guild.get_role(int(role_id))
            if role:
                try:
                    await member.add_roles(role, reason=reason)
                except discord.Forbidden:
                    print(f"Bot doesn't have permissions to assign role {role.name}")
                except discord.HTTPException:
                    print(f"Failed to assign role {role.name} to {member.display_name}")
            else:
                print(f"Role with ID {role_id} not found.")

    @Cog.listener()
    async def on_member_join(self, member):
        data = getDB(member.guild.id)
        clr = data["welcome"]["color"]
        msg = data["welcome"]["message"]
        chan = list(data["welcome"]["channel"])
        emtog = data["welcome"]["embed"]
        emping = data["welcome"]["ping"]
        emimage = data["welcome"]["image"]
        tital = data["welcome"]["title"]
        eauthor = data["welcome"]["author"]
        efooter = data["welcome"]["footer"]
        emthumbnail = data["welcome"]["thumbnail"]
        emautodel = data["welcome"]["autodel"]
        user = member
        if chan == []:
          return
        else:
            if "<<server.name>>" in msg:
               msg = msg.replace("<<server.name>>", "%s" % (user.guild.name))
            if "<<server.member_count>>" in msg:
              msg = msg.replace("<<server.member_count>>", "%s" % (user.guild.member_count))
            if "<<user.name>>" in msg:
              msg = msg.replace("<<user.name>>", "%s" % (user))
            if "<<user.mention>>" in msg:
              msg = msg.replace("<<user.mention>>", "%s" % (user.mention))
            if "<<user.created_at>>" in msg:
              msg = msg.replace("<<user.created_at>>", f"<t:{int(user.created_at.timestamp())}:F>")
            if "<<user.joined_at>>" in msg:
              msg = msg.replace("<<user.joined_at>>", f"<t:{int(user.joined_at.timestamp())}:F>")
            if msg == "":
              msg = ""
            else:
              msg = msg
            if emping == True:
              emping = f"**Hey {user.mention} Welcome To {user.guild.name}**"
            else:
              emping = ""
            if emautodel == 0:
              emautodel = None
            else:
              emautodel = emautodel
            em = discord.Embed(description=msg)
            if clr == "":
              em.color = discord.Color(0x0d0d13)  
            else:
                try:
                  color_value = int(clr.replace("#", "0x"), 16)
                  em.color = discord.Color(color_value)
                except ValueError:
                  em.color = discord.Color(0x0d0d13)          
            if eauthor== "":
              em.set_author(name=user, icon_url=member.avatar.url if member.avatar else member.default_avatar.url)
            else:
              em.set_author(name=eauthor, icon_url=member.avatar.url if member.avatar else member.default_avatar.url)
            em.timestamp = discord.utils.utcnow()
            if emimage == "":
                em.set_image(url=None)
            else:
                em.set_image(url=emimage)
            if emthumbnail == "":
                em.set_thumbnail(url=None)
            else:
                em.set_thumbnail(url=emthumbnail)
            if efooter == "":
                em.set_footer(  text=user.guild.name, icon_url=user.guild.icon.url)
            else:
              em.set_footer(  text=efooter, icon_url=user.guild.icon.url)
            if tital == "":
                pass
            else:
              em.title = tital
            if emtog == True:
                for chh in chan:
                    ch = self.bot.get_channel(int(chh))
                    await ch.send(emping, embed=em, delete_after=emautodel)
            else:
                for chh in chan:
                    ch = self.bot.get_channel(int(chh))
                    if emtog == False:
                        await ch.send(msg, delete_after=emautodel)
                        