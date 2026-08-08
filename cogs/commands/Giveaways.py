import discord
from discord.ext import commands
import datetime
import time
import json
import random
from discord.ui import View, Button

class giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x2f3136

    def convert(self, time_str):
        units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        unit = time_str[-1]
        if unit not in units:
            return -1  # incorrect unit of time
        try:
            return int(time_str[:-1]) * units[unit], None
        except ValueError:
            return -2  # incorrect time value

    @commands.command(description="Starts a new giveaway.")
    @commands.has_permissions(administrator=True)
    async def gstart(self, ctx, duration: str, winners: int, *, prize: str):
        await ctx.message.delete()

        converted_time, error = self.convert(duration)
        if error:
            await ctx.send("Invalid duration format. Please use a valid format like `1d`, `1h`, `1m`, or `1s`.")
            return

        end_time = int(time.time()) + converted_time
        giveaway_embed = discord.Embed(
            title=f"<a:tadaaa:1226091325682876487> {prize} <a:tadaaa:1226091325682876487>",
            color=self.color,
            description=f'<a:dot:1226091089740562463> Winners: {winners}\n<a:dot:1226091089740562463>Ends: <t:{end_time}:R> (<t:{end_time}:f>)\n<a:dot:1226091089740562463>Hosted by: {ctx.author.mention}\n\n<a:dot:1226091089740562463> React on 🎉 to participate!!'
        )
        giveaway_embed.set_footer(icon_url=self.bot.user.display_avatar.url, text="Ends at")
        giveaway_embed.timestamp = datetime.datetime.utcnow() + datetime.timedelta(seconds=converted_time)

        channel = ctx.channel
        giveaway_message = await channel.send(content="<a:Gift:1226091270511001661>** New Giveaway **<a:Gift:1226091270511001661>", embed=giveaway_embed)
        await giveaway_message.add_reaction("🎉")

        with open(f"data/json/giveaways.json", "r") as f:
            giveaways = json.load(f)

        data = {
            "prize": prize,
            "host": ctx.author.id,
            "winners": winners,
            "end_time": end_time,
            "channel_id": channel.id,
            "link": giveaway_message.jump_url,
            "ended": False
        }
        giveaways[str(giveaway_message.id)] = data

        with open(f"data/json/giveaways.json", "w") as f:
            json.dump(giveaways, f, indent=4)

    @commands.command(description="Ends a current giveaway.")
    @commands.has_permissions(administrator=True)
    async def gend(self, ctx, giveaway_id: int):
        with open(f"data/json/giveaways.json", "r") as f:
            giveaways = json.load(f)

        if str(giveaway_id) in giveaways:
            data = giveaways[str(giveaway_id)]
            channel = self.bot.get_channel(data["channel_id"])
            giveaway_message = await channel.fetch_message(giveaway_id)

            reaction = discord.utils.get(giveaway_message.reactions, emoji="🎉")
            participants = [user.id async for user in reaction.users() if not user.bot]
            giveaways[str(giveaway_id)]["entries"] = len(participants)

            winners = []
            if len(participants) ==0:
              await ctx.send("No valid participants. The giveaway has been cancelled.")
              giveaways[str(giveaway_id)]["ended"] = True
              with open(f"data/json/giveaways.json", "w") as f:
                json.dump(giveaways, f, indent=4)
                
              return
            if len(participants) < data["winners"] and len(participants) != 0:
                winners = participants
            elif len(participants) != 0:
                winners = random.sample(participants, data["winners"])

            winner_mentions = '\n'.join([f'<@{winner}>' for winner in winners])

            result_embed = discord.Embed(
                title=f"<a:tadaaa:1226091325682876487> {data['prize']} <a:tadaaa:1226091325682876487>",
                color=self.color,
                description=f"<a:dot:1226091089740562463> Winners: {winner_mentions}\n<a:dot:1226091089740562463> Hosted By: <@{data['host']}>\n<a:dot:1226091089740562463> Participants: {len(participants)}"
            )
            result_embed.set_footer(icon_url=self.bot.user.display_avatar.url, text="Redox | Giveaway Ended")
            result_embed.timestamp = discord.utils.utcnow()
            link = data['link']
            button = Button(label="Giveaway Link", url =link)
            view= View()
            view.add_item(button)
            await channel.send(content=f"**Congratulations {winner_mentions}**", embed=discord.Embed(title="<a:tadaaa:1226091325682876487> {} <a:tadaaa:1226091325682876487>".format(data["prize"]),color=0x030404,description=f"Winners: {winner_mentions}\nHosted By: <@{data['host']}>"),view=view)
            await giveaway_message.edit(content="<a:Gift:1226091270511001661> **GIVEAWAY ENDED** <a:Gift:1226091270511001661>", embed=result_embed)

            giveaways[str(giveaway_id)]["ended"] = True

            with open(f"data/json/giveaways.json", "w") as f:
                json.dump(giveaways, f, indent=4)

    @commands.command(description="Rerolls winners for a specific giveaway.")
    @commands.has_permissions(administrator=True)
    async def greroll(self, ctx, giveaway_id: int):
        with open(f"data/json/giveaways.json", "r") as f:
            giveaways = json.load(f)

        if str(giveaway_id) in giveaways:
            data = giveaways[str(giveaway_id)]
            if data["ended"] is False:
              await ctx.send("The giveaway has not ended yet.")
              return
            channel = self.bot.get_channel(data["channel_id"])
            giveaway_message = await channel.fetch_message(giveaway_id)

            reaction = discord.utils.get(giveaway_message.reactions, emoji="🎉")
            participants = [user.id async for user in reaction.users() if not user.bot]

            if len(participants) == 0:
                await ctx.send("No one participated in the giveaway.")
                return

            winners = random.sample(participants, data["winners"])

            winner_mentions = '\n'.join([f'<@{winner}>' for winner in winners])

            result_embed = discord.Embed(
                title=f" **<a:tadaaa:1226091325682876487> {data['prize']} <a:tadaaa:1226091325682876487>**",
                color=self.color,
                description=f"<a:dot:1226091089740562463>New Winners: {winner_mentions}"
            )
            result_embed.set_footer(icon_url=self.bot.user.display_avatar.url, text="Redox | Giveaway Rerolled")
            result_embed.timestamp = discord.utils.utcnow()

            await channel.send(content=winner_mentions, embed=result_embed)

