from __future__ import annotations
from core import Redox # type: ignore

#____________ Commands ___________
from .commands.webhook import WebCog
#from .commands.games1 import Games
from .commands.ticket import ticket
from .commands.starboard import Starboard 
from .commands.embed import Embed
from .commands.mod import mod
from .commands.Autorole import autorole
from .commands.Giveaways import giveaway
from .commands.giveaway_task import gwtask
from .commands.youtube import Youtube
from .commands.help import Help
from .commands.general import General
#from .commands.music import Music
from .commands.moderation import Moderation
from .commands.vcroles import Voice
from .commands.anti import Security
from .commands.raidmode import Automod
from .commands.welcome import Welcomer
from .commands.fun import Fun
from .commands.extra import Utility
from .commands.owner import Owner
from .commands.role import Server
from .commands.ignore import Ignore
from .commands.vanityroles import Vanityroles
from .commands.List import list
from .commands.serverinfo import Info
from .commands.Afk import afk

from .commands.Media import Media
from .commands.Logging import Logging
from .commands.Reminder import Reminder


from .commands.react import react
#from .commands.about import About
from .commands.uptime import Uptime
#from .commands.filter import MusicFilters
from .commands.nitro import Nitro
from .commands.boost import boost
from .commands.stats import Stats
#____________ Events _____________


from .events.join import Join
from .events.antiban import antiban
from .events.antichannel import Antichannel
from .events.antiguild import AntiGuild
from .events.antirole import antirole
from .events.antibot import antibot
from .events.antikick import AntiKick
from .events.antiprune import AntiPrune
from .events.antiwebhook import AntiWebhook
from .events.antiping import antipinginv
from .events.antiemostick import AntiEmojiCreate
from .events.antintegration import AntiIntegration
from .events.antispam import AntiSpam
from .events.autoblacklist import AutoBlacklist
from .events.antiemojid import AntiEmoji
from .events.antiemojiu import AntiEmojiUpdate
from .events.Errors import Errors
from .events.on_guild import Guild
from .events.greet2 import greet
from .events.voiceupdate import Vcroles2
from .events.boost2 import bst
from .events.boost3 import Boost3


##############select menu + button#############

from .commands.ticket1 import ticket1

from .commands.anti1 import anti1
from .commands.general1 import general1
from .commands.extra1 import extra1
from .commands.gw1 import gw1

from .commands.mod2 import mod1
from .commands.music1 import music1
from .commands.boost1 import velo1
from .commands.raidmode1 import raidmode1

from .commands.welcome1 import welcome1
from .commands.fun1 import fun1
from .commands.logging1 import logging1
from .commands.role1 import role1
from .commands.vanity1 import vanity1
from .commands.voice1 import voice1
from .commands.vcrole1 import vcrole1





###############cmnd add################ games

async def setup(bot: Redox):
  await bot.add_cog(Help(bot))
  await bot.add_cog(Stats(bot))
  await bot.add_cog(WebCog(bot))
  await bot.add_cog(Starboard(bot))
  await bot.add_cog(autorole(bot))
  await bot.add_cog(General(bot))
  #await bot.add_cog(Music(bot))
  await bot.add_cog(Moderation(bot))
  await bot.add_cog(Security(bot))
  await bot.add_cog(Automod(bot))
  await bot.add_cog(Welcomer(bot))
  await bot.add_cog(boost(bot))
  await bot.add_cog(ticket(bot))
  #await bot.add_cog(Games(bot))
  await bot.add_cog(Fun(bot))
  await bot.add_cog(Utility(bot))
  await bot.add_cog(Voice(bot))
  await bot.add_cog(Owner(bot))
  await bot.add_cog(Server(bot))
 # await bot.add_cog(Vanityroles(bot))
 # await bot.add_cog(vanity1(bot))
  await bot.add_cog(Ignore(bot))
  
  await bot.add_cog(Media(bot))
  await bot.add_cog(Info(bot))
  await bot.add_cog(list(bot))
  await bot.add_cog(afk(bot))
  await bot.add_cog(Logging(bot))
  await bot.add_cog(Youtube(bot))
  await bot.add_cog(Reminder(bot))
  await bot.add_cog(giveaway(bot))
  await bot.add_cog(gwtask(bot))
  
 
  await bot.add_cog(react(bot))
 # await bot.add_cog(About(bot))
  await bot.add_cog(Uptime(bot))
  #await bot.add_cog(MusicFilters(bot))
  await bot.add_cog(mod(bot))
  await bot.add_cog(Nitro(bot))
  await bot.add_cog(Embed(bot))
############select menu + button###############

  await bot.add_cog(anti1(bot))
  await bot.add_cog(gw1(bot))
  await bot.add_cog(music1(bot))
  await bot.add_cog(mod1(bot))
  await bot.add_cog(ticket1(bot))
  await bot.add_cog(extra1(bot))
  await bot.add_cog(velo1(bot)) 
  await bot.add_cog(logging1(bot))
  await bot.add_cog(welcome1(bot))
  
  await bot.add_cog(raidmode1(bot))
  
  await bot.add_cog(role1(bot))
  await bot.add_cog(fun1(bot))
  
  await bot.add_cog(general1(bot))  
  
  
  await bot.add_cog(voice1(bot)) 
  await bot.add_cog(vcrole1(bot))
 # await bot.add_cog(vanity1(bot)) 


    
###########################events################3
  
  await bot.add_cog(antiban(bot))
  await bot.add_cog(Antichannel(bot))
  await bot.add_cog(AntiGuild(bot))
  await bot.add_cog(antirole(bot))
  await bot.add_cog(antibot(bot))
  await bot.add_cog(AntiKick(bot))
  await bot.add_cog(AntiPrune(bot))
  await bot.add_cog(AntiWebhook(bot))
  await bot.add_cog(antipinginv(bot))
  await bot.add_cog(AntiEmoji(bot))
  await bot.add_cog(AntiIntegration(bot))  
  await bot.add_cog(AntiSpam(bot))
  await bot.add_cog(AutoBlacklist(bot))
  await bot.add_cog(AntiEmojiCreate(bot))
  await bot.add_cog(AntiEmojiUpdate(bot))
  await bot.add_cog(Guild(bot))
  await bot.add_cog(Errors(bot))
  await bot.add_cog(greet(bot))
  await bot.add_cog(Join(bot))
  await bot.add_cog(Vcroles2(bot))
  await bot.add_cog(bst(bot))
  await bot.add_cog(Boost3(bot))