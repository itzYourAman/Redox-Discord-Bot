import discord
import asyncio
from discord.ext import commands, tasks
import datetime
import time 
import json
import random
import os 
from discord.ui import View, Button

class gwtask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x11100d
        self.giveaway_task.start()

    def cog_unload(self):
        self.giveaway_task.cancel()

    @tasks.loop(seconds=5)
    async def giveaway_task(self):
        await self.bot.wait_until_ready()
        with open(f"data/json/giveaways.json", "r") as f:
            giveaways = json.load(f)

        if len(giveaways) == 0:
            return

        current_time = int(time.time())
        
        for giveaway_id, data in giveaways.items():
            if current_time > data["end_time"] and not data["ended"]:
                channel = self.bot.get_channel(data["channel_id"])
                if channel is None:
                    print(f"Giveaway channel not found for ID: {giveaway_id}")
                    giveaways[giveaway_id]["ended"] = True
                    with open("data/json/giveaways.json", "w", encoding="utf-8") as f:
                        json.dump(giveaways, f, indent=4)
                    continue
                try:
                    giveaway_message = await channel.fetch_message(int(giveaway_id))
                except discord.NotFound:
                    print(f"Giveaway message not found for ID: {giveaway_id}")
                    giveaways[giveaway_id]["ended"] = True

                    with open("data/json/giveaways.json", "w", encoding="utf-8") as f:
                        json.dump(giveaways, f, indent=4)
                    continue

                reaction = discord.utils.get(giveaway_message.reactions, emoji="🎉")
                participants = [user.id async for user in reaction.users() if not user.bot]
                giveaways[giveaway_id]["participants"] = participants
                giveaways[giveaway_id]["entries"] = len(participants)

                if len(participants) == 0:
                    result_embed = discord.Embed(
                        title="<a:tadaaa:1226091325682876487> {} <a:tadaaa:1226091325682876487>".format(data["prize"]),
                        color=0x030404,
                        description=f"No one participated in the giveaway!\nHosted By: <@{data['host']}>"
                    )
                    result_embed.set_footer(icon_url=self.bot.user.display_avatar.url, text="Redox | Giveaway Ended")
                    result_embed.timestamp = discord.utils.utcnow()
                    await giveaway_message.edit(content="", embed=result_embed, view=None)
                    giveaways[giveaway_id]["ended"] = True
                    with open(f"data/json/giveaways.json", "w") as f:
                        json.dump(giveaways, f, indent=4)
                    continue

                winners = random.sample(participants, data["winners"])
                winner_mentions = '\n'.join([f'<@{winner}>' for winner in winners])

                result_embed = discord.Embed(
                    title="<a:tadaaa:1226091325682876487> {} <a:tadaaa:1226091325682876487>".format(data["prize"]),
                    color=0x030404,
                    description=f"Winners: {winner_mentions}\nHosted By: <@{data['host']}>\nValid Participants : {len(participants)}"
                )
                result_embed.set_footer(icon_url=self.bot.user.display_avatar.url, text="Redox | Giveaway Ended")
                result_embed.timestamp = discord.utils.utcnow()
                link = data['link']
                button = Button(label="Giveaway Link", url =link)
                view= View()
                view.add_item(button)
                await channel.send(content=f"**Congratulations {winner_mentions} **", embed=discord.Embed(title="<a:tadaaa:1226091325682876487> {} <a:tadaaa:1226091325682876487>".format(data["prize"]),color=0x030404,description=f"Winners: {winner_mentions}\nHosted By: <@{data['host']}>"),view=view)
                await giveaway_message.edit(content="<a:Gift:1226091270511001661>**GIVEAWAY ENDED** <a:Gift:1226091270511001661>", embed=result_embed, view=None)

                giveaways[giveaway_id]["ended"] = True

                with open(f"data/json/giveaways.json", "w") as f:
                    json.dump(giveaways, f, indent=4)
                    