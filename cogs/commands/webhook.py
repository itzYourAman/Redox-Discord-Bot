import discord
from discord.ext import commands
from utils.Tools import *

class WebCog(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.group(name="webhook",invoke_without_command=True)
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _wh(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)
            
    @_wh.command(usage="webhook create <name>")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def create(self, ctx, name=None):
        '''Creates a webhook in the current channel'''
        if not name:
            await ctx.send("Please specify a name for the webhook.")
            return

        webhook = await ctx.channel.create_webhook(name=name)
        embed = discord.Embed(
            title=f"Webhook {webhook.name} created successfully",
            color=discord.Color.blue()
        )

        try:
            await ctx.author.send(f"||{webhook.url}||")
            await ctx.author.send(embed=embed)
            await ctx.send(f"Webhook {webhook.name} created successfully. Check your DMs for the URL.")
        except discord.Forbidden:
            await ctx.send(f"Webhook {webhook.name} (Unable to DM user)")

    @_wh.command(usage="webhook delete <name>")
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def delete(self, ctx, webhook_id):
        '''Deletes a webhook by ID'''
        try:
            webhook = await discord.Webhook.from_url(
                webhook_id, adapter=discord.RequestsWebhookAdapter())
            await webhook.delete()
            await ctx.send("Webhook deleted successfully.")
        except discord.NotFound:
            await ctx.send("Webhook not found.")

    @_wh.command(usage="webhook list")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def list(self, ctx):
        '''Lists all webhooks in the current channel'''
        webhooks = await ctx.channel.webhooks()
        if not webhooks:
            await ctx.send("No webhooks found in this channel.")
            return

        embed = discord.Embed(title="List of Webhooks", color=discord.Color.blue())
        for webhook in webhooks:
            embed.add_field(
                name="__Name__",
                value=f"**{webhook.name}**"
            )
            embed.add_field(name="__ID__", value=webhook.id)
            embed.add_field(name="\u200b", value="\u200b")

        await ctx.send(f"{ctx.author.mention}, Here are the webhooks in this channel", embed=embed)

