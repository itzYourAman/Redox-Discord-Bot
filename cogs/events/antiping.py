import discord
from discord.ext import commands
from utils.Tools import *
from itertools import cycle
import logging
from core import Redox, Cog
from discord.ui import View, Button
import json

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

proxies = open('data/proxies.txt').read().split('\n')
proxs = cycle(proxies)
proxies={"http": 'http://' + next(proxs)}

class antipinginv(Cog):
    def __init__(self, client: Redox):
        self.client = client
        self.spam_control = commands.CooldownMapping.from_cooldown(10, 12.0, commands.BucketType.user)

    @commands.Cog.listener()
    async def on_message(self, message):
        button = Button(label="Invite Me", url="https://discord.com/oauth2/authorize?client_id=1126351590064930847&permissions=1239031351480&scope=bot")
        button1 = Button(label="Support Server", url="https://discord.com/invite/5SUKAB7n93")
        button2 = Button(label="Vote Me", url="https://discord.com/invite/CCYef4Ad4M")

        try:
            with open("data/json/blacklist.json", "r", encoding="utf-8") as f:
                data2 = json.load(f)
                data1 = getIgnore(message.guild.id)
                ch = data1["channel"]
                iuser = data1["user"]
                Redox = '<@1126351590064930847>'
                try:
                    data = getConfig(message.guild.id)
                    anti = getanti(message.guild.id)
                    prefix = data["prefix"]
                    wled = data["whitelisted"]
                    punishment = data["punishment"]
                    wlrole = data['wlrole']
                    guild = message.guild
                    hacker = guild.get_member(message.author.id)
                    wlroles = guild.get_role(wlrole)
                except Exception:
                    pass

                if message.mention_everyone:
                    if str(message.author.id) in wled or anti == "off" or wlroles in hacker.roles:
                        pass
                    else:
                        if punishment == "ban":
                            await message.guild.ban(message.author, reason="Mentioning Everyone | Not Whitelisted")
                        elif punishment == "kick":
                            await message.guild.kick(message.author, reason="Mentioning Everyone | Not Whitelisted")
                        elif punishment == "none":
                            return

                elif message.content == Redox or message.content == "<@!1126351590064930847>":
                    if str(message.channel.id) in ch:
                        embed = discord.Embed(description="This Channel is in the ignored channel list. Try my commands in another channel.",color=0x2f3136)
                        await message.reply(embed=embed,mention_author=True, delete_after=10)
                        return  # Add this line to exit the function after sending the ignored channel text

                    if str(message.author.id) in iuser:
                        await message.reply(embed=discord.Embed(description=f"You are set as an ignored user for {message.guild.name}.\nTry my commands or modules in another guild.", color=discord.Colour(0x2f3136)), delete_after=8)
                        return  # Add this line to exit the function after sending the ignored user text

                    if str(message.author.id) in data2["ids"]:
                        embed = discord.Embed(title="<:blacklist:1138851262587224124> Blacklisted", description="*You Are Blacklisted From Using My Commands.*\n**If You Think That It Is A Mistake, You Can Appeal In Our Support Server By Clicking [here](https://discord.com/invite/4njeczb8st)**")
                        await message.reply(embed=embed, mention_author=False,delete_after=10)
                        return  # Add this line to exit the function after sending the blacklist text

                    else:
                        embed = discord.Embed(description=f"Hey {message.author.mention}\nMy prefix is `{prefix}`\nTo know more type `{prefix}help`.\n\nIf you continue to have problems, consider asking for help [Click Here](https://discord.com/invite/4njeczb8st)", color=0x0d0d13)
                        view = View()
                        view.add_item(button)
                        view.add_item(button1)
                        #view.add_item(button2)

                        await message.reply(embed=embed, delete_after=20, mention_author=False, view=view)
                else:
                    return

        except Exception as error:
            if isinstance(error, discord.Forbidden):
                return
