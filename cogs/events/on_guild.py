import discord
from discord.ext import commands
from core import Redox, Cog
import json
from utils.Tools import *
from discord.ui import View, Button
import logging

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

class Guild(Cog):
    def __init__(self, client: Redox):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        
        
        me = self.client.get_channel(1218183304826720286)
        channels = len(set(self.client.get_all_channels()))
        embed = discord.Embed(
            title=f"{guild.name}'s Information",
            color=0x0d0d13
        ).set_author(
            name="Guild Joined",
            icon_url=guild.me.display_avatar.url if guild.icon is None else guild.icon.url
        ).set_footer(
            text=f"{guild.name}",
            icon_url=guild.me.display_avatar.url if guild.icon is None else guild.icon.url
        )
        embed.add_field(
            name="**__About__**",
            value=f"**Name : ** {guild.name}\n**ID :** {guild.id}\n**Owner <:Redox_owner:1138644816759111840> :** {guild.owner} (<@{guild.owner_id}>)\n**Created At : **{guild.created_at.month}/{guild.created_at.day}/{guild.created_at.year}\n**Members :** {len(guild.members)}",
            inline=False
        )
        embed.add_field(
            name="**__Description__**",
            value=f"{guild.description}",
            inline=False
        )
        if guild.features:
            embed.add_field(
                name="**__Features__**",
                value='\n'.join([feature.replace('_', ' ').title() for feature in guild.features]),
                inline=False
            )
        embed.add_field(
            name="**__Members__**",
            value=f"""
Members : {len(guild.members)}
Humans : {len(list(filter(lambda m: not m.bot, guild.members)))}
Bots : {len(list(filter(lambda m: m.bot, guild.members)))}
            """,
            inline=False
        )
        embed.add_field(
            name="**__Channels__**",
            value=f"""
Categories : {len(guild.categories)}
Text Channels : {len(guild.text_channels)}
Voice Channels : {len(guild.voice_channels)}
Threads : {len(guild.threads)}
            """,
            inline=False
        )
        embed.add_field(
            name="**__Emoji Info__**",
            value=f"Emojis : {len(guild.emojis)}\nStickers : {len(guild.stickers)}",
            inline=False
        )
        embed.add_field(
            name="Bot Info:", 
            value=f"Servers: `{len(self.client.guilds)}`\nUsers: `{len(self.client.users)}`\nChannels: `{channels}`",
            inline=False
        )
        if guild.icon is not None:
            embed.set_thumbnail(url=guild.icon.url)
        embed.timestamp = discord.utils.utcnow()
        await me.send(embed=embed)
        if not guild.chunked:
            await guild.chunk()

        # Send welcome message to the server
        embed = discord.Embed(
            description="Thank you for adding me to your server!\n・ My default prefix is `$`\n・ You can use the `$help` command to get a list of commands\n・ Our [support server](https://discord.com/invite/CCYef4Ad4M) or our team offers detailed information & guides for commands\n・ Feel free to join our [Support Server](https://discord.com/invite/CCYef4Ad4M) if you need help/support for anything related to the bot",
            color=0x2f3136
        )
        velocity = Button(label='Support Server', style=discord.ButtonStyle.link, url='https://discord.com/invite/4njeczb8st')
        velocity1 = Button(label='Invite Me', style=discord.ButtonStyle.link, url='https://discord.com/api/oauth2/authorize?client_id=1126351590064930847&permissions=8&scope=bot%20applications.commandshttps://discord.com/api/oauth2/authorize?client_id=1147798554023305237&permissions=8&scope=bot%20applications.commands')

        view = View()
        view.add_item(velocity) 
        view.add_item(velocity1)
        embed.set_author(name=f"{guild.name}", icon_url=guild.me.display_avatar.url if guild.icon is None else guild.icon.url)
        embed.set_thumbnail(url=guild.me.display_avatar.url if guild.icon is None else guild.icon.url)
        channel = discord.utils.get(guild.text_channels, name="general")
        if not channel:
            channels = [channel for channel in guild.text_channels if channel.permissions_for(guild.me).send_messages]
            if channels:
                channel = channels[0]
                await channel.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.client.wait_until_ready()
        idk = self.client.get_channel(1218183305820897390)
        channels = len(set(self.client.get_all_channels()))
        embed = discord.Embed(
            title=f"{guild.name}'s Information",
            color=0x00FFCA
        ).set_author(
            name="Guild Removed",
        ).set_footer(
            text=f"{guild.name}"
        )
        embed.add_field(
            name="**__About__**",
            value=f"**Name : ** {guild.name}\n**ID :** {guild.id}\n**Owner <:Redox_owner:1138644816759111840> :** {guild.owner} (<@{guild.owner_id}>)\n**Created At : **{guild.created_at.month}/{guild.created_at.day}/{guild.created_at.year}\n**Members :** {len(guild.members)}",
            inline=False
        )
        embed.add_field(
            name="**__Description__**",
            value=f"{guild.description}",
            inline=False
        )
        if guild.features:
            embed.add_field(
                name="**__Features__**",
                value='\n'.join([feature.replace('_', ' ').title() for feature in guild.features]),
                inline=False
            )
        embed.add_field(
            name="**__Members__**",
            value=f"""
Members : {len(guild.members)}
Humans : {len(list(filter(lambda m: not m.bot, guild.members)))}
Bots : {len(list(filter(lambda m: m.bot, guild.members)))}
            """,
            inline=False
        )
        embed.add_field(
            name="**__Channels__**",
            value=f"""
Categories : {len(guild.categories)}
Text Channels : {len(guild.text_channels)}
Voice Channels : {len(guild.voice_channels)}
Threads : {len(guild.threads)}
            """,
            inline=False
        )
        embed.add_field(
            name="Bot Info:", 
            value=f"Servers: `{len(self.client.guilds)}`\nUsers: `{len(self.client.users)}`\nChannels: `{channels}`",
            inline=False
        )
        if guild.icon is not None:
            embed.set_thumbnail(url=guild.icon.url)
        embed.timestamp = discord.utils.utcnow()
        await idk.send(embed=embed)

        # Remove guild from config
        with open("data/json/config.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        if str(guild.id) in data["guilds"]:
            del data["guilds"][str(guild.id)]

            with open("data/json/config.json", "w", encoding="utf-8") as f:
                json.dump(data, f)

    @commands.Cog.listener()
    async def on_shard_ready(self, shard_id):
        logging.info(f"Shard #{shard_id} is ready")

    @commands.Cog.listener()
    async def on_shard_connect(self, shard_id):
        logging.info(f"Shard #{shard_id} has connected")

    @commands.Cog.listener()
    async def on_shard_disconnect(self, shard_id):
        logging.info(f"Shard #{shard_id} has disconnected")

    @commands.Cog.listener()
    async def on_shard_resume(self, shard_id):
        logging.info(f"Shard #{shard_id} has resumed")

  