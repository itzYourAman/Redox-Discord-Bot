import discord
from discord.ext import commands
import json
import datetime

def loadafks():
    try:
        with open('data/json/afk.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
            if "global" not in data:
                data["global"] = []
            return data
    except FileNotFoundError:
        return {"global": []}

def saveafks(data):
    with open('data/json/afk.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4)

afks = loadafks()

class AFKButton(discord.ui.Button):
    def __init__(self, ctx: commands.Context, label, reason, style=discord.ButtonStyle.primary, customid="serverafk"):
        super().__init__(style=style, label=label, custom_id=customid)
        self.ctx = ctx
        self.reason = reason

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(
                embed=discord.Embed(description=f"Only **{self.ctx.author}** can use this button. Use `{self.ctx.prefix}{self.ctx.command}` to run the command.", color=discord.Color.red()),
                ephemeral=True
            )
            return

        timestamp = datetime.datetime.utcnow().isoformat()
        user_id = str(interaction.user.id)

        if self.custom_id == "serverafk":
            server_id = str(interaction.guild.id)
            if server_id not in afks:
                afks[server_id] = []
            afks[server_id].append({"id": user_id, "reason": self.reason, "timestamp": timestamp, "mentions": []})
            saveafks(afks)
            success_message = f"{interaction.user.name}, your server AFK status has been set."
        elif self.custom_id == "globalafk":
            afks["global"].append({"id": user_id, "reason": self.reason, "timestamp": timestamp, "mentions": []})
            saveafks(afks)
            success_message = f"{interaction.user.name}, your global AFK status has been set."

        success_embed = discord.Embed(description=f"Reason: {self.reason}")
        success_embed.set_author(name=success_message, icon_url=interaction.user.avatar.url)

        await interaction.message.edit(embed=success_embed, view=None)

class afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(help="Sets afk into a server or globally")
    async def afk(self, ctx, *, reason="I'm AFK :D"):
        view = discord.ui.View()
        view.add_item(AFKButton(ctx, "Global AFK", reason, customid="globalafk", style=discord.ButtonStyle.green))
        view.add_item(AFKButton(ctx, "Server AFK", reason, customid="serverafk", style=discord.ButtonStyle.green))
        afk_embed = discord.Embed(
            description="Choose your AFK style from the buttons below.",
           
)
        afk_embed.set_author(name=f"{ctx.author.display_name}", icon_url=ctx.author.avatar.url)

        await ctx.send(embed=afk_embed, view=view)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = str(message.author.id)
        server_id = str(message.guild.id)

        afk_removed = False
        removed_reason = ""
        removed_timestamp = None
        removed_mentions = []

        if server_id in afks:
            for entry in afks[server_id]:
                if entry["id"] == user_id:
                    removed_reason = entry["reason"]
                    removed_timestamp = entry["timestamp"]
                    removed_mentions = entry["mentions"]
                    afks[server_id].remove(entry)
                    afk_removed = True
                    break
            if afk_removed:
                saveafks(afks)

        if not afk_removed and "global" in afks:
            for entry in afks["global"]:
                if entry["id"] == user_id:
                    removed_reason = entry["reason"]
                    removed_timestamp = entry["timestamp"]
                    removed_mentions = entry["mentions"]
                    afks["global"].remove(entry)
                    afk_removed = True
                    break
            if afk_removed:
                saveafks(afks)

        if afk_removed:
            removed_time = datetime.datetime.fromisoformat(removed_timestamp)
            afk_duration = datetime.datetime.utcnow() - removed_time
            afk_seconds = int(afk_duration.total_seconds())
            afk_minutes = afk_seconds // 60
            afk_hours = afk_minutes // 60
            afk_minutes = afk_minutes % 60
            afk_seconds = afk_seconds % 60

            if afk_hours > 0:
                duration_message = f"{afk_hours} hours {afk_minutes} minutes"
            elif afk_minutes > 0:
                duration_message = f"{afk_minutes} minutes"
            else:
                duration_message = f"{afk_seconds} seconds"

            mention_messages = "\n".join([f"`{idx + 1}.` **{mention['user']}** - [Message Link]({mention['link']})" for idx, mention in enumerate(removed_mentions)])
            mention_text = f"Following user(s) mentioned you while you were AFK:\n{mention_messages}" if removed_mentions else ""

            embed = discord.Embed(
                description=f"Reason was: {removed_reason}\n\n{mention_text}",
              
            )
            embed.set_author(name=f"Your AFK status has been removed after {duration_message}.", icon_url=message.author.avatar.url)

            await message.channel.send(f"{message.author.mention}", embed=embed)

        for user in message.mentions:
            user_id = str(user.id)
            afk_reason = None
            afk_timestamp = None
            afk_type = None

            if server_id in afks:
                for entry in afks[server_id]:
                    if entry["id"] == user_id:
                        afk_reason = entry["reason"]
                        afk_timestamp = entry["timestamp"]
                        afk_type = "server"
                        break

            if not afk_reason and "global" in afks:
                for entry in afks["global"]:
                    if entry["id"] == user_id:
                        afk_reason = entry["reason"]
                        afk_timestamp = entry["timestamp"]
                        afk_type = "global"
                        break

            if afk_reason:
                afk_time = datetime.datetime.fromisoformat(afk_timestamp)
                afk_duration = datetime.datetime.utcnow() - afk_time
                afk_seconds = int(afk_duration.total_seconds())
                afk_minutes = afk_seconds // 60
                afk_hours = afk_minutes // 60
                afk_minutes = afk_minutes % 60
                afk_seconds = afk_seconds % 60

                if afk_hours > 0:
                    duration_message = f"{afk_hours} hours {afk_minutes} minutes"
                elif afk_minutes > 0:
                    duration_message = f"{afk_minutes} minutes"
                else:
                    duration_message = f"{afk_seconds} seconds"

                afk_type_message = "globally " if afk_type == "global" else ""
                
                afk_embed = discord.Embed(
                    description=f"{user.display_name} went AFK {afk_type_message}{duration_message} ago.",
                )
                afk_embed.set_author(name=f"{user.display_name}", icon_url=user.avatar.url)
                await message.channel.send(embed=afk_embed)

                if afk_type == "server":
                    for entry in afks[server_id]:
                        if entry["id"] == user_id:
                            entry["mentions"].append({"user": message.author.display_name, "link": message.jump_url})
                            break
                elif afk_type == "global":
                    for entry in afks["global"]:
                        if entry["id"] == user_id:
                            entry["mentions"].append({"user": message.author.display_name, "link": message.jump_url})
                            break
                saveafks(afks)

       # await self.bot.process_commands(message)


    