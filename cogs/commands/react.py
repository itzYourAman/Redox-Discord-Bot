import json
from utils import *
import discord
from discord.ext import commands

class react(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reaction_triggers = {}

        # load saved reaction triggers from file
        try:
            with open('data/json/reaction_triggers.json', 'r', encoding="utf-8") as f:
                self.reaction_triggers = json.load(f)
        except FileNotFoundError:
            pass

    # function to save reaction triggers to file
    def save_reaction_triggers(self):
        with open('data/json/reaction_triggers.json', 'w', encoding="utf-8") as f:
            json.dump(self.reaction_triggers, f)

    # check if user is admin
    def is_admin():
        def predicate(ctx):
            return ctx.author.guild_permissions.administrator
        return commands.check(predicate)

    @commands.group(name="autoreact",invoke_without_command=True)#,aliases=['ar'])
    @is_admin()
    async def react(self, ctx: commands.Context):
      if ctx.subcommand_passed is None:
        await ctx.send_help(ctx.command)
        ctx.command.reset_cooldown(ctx)      
       # a
    @react.command()
    async def list(self, ctx, *, view=None):
        if not self.reaction_triggers:
            await ctx.send("There are no reaction triggers set")
        else:
            if view == 'raw':
                await ctx.send(self.reaction_triggers)
            else:
                entries = [] 
                for trigger, reaction in self.reaction_triggers.items():
                    entry = f"{trigger}: {reaction}"
                    entries.append(entry)

              
                paginator = Paginator(source=DescriptionEmbedPaginator(entries=entries,title="Current Reaction Triggers",color=0x2f3136,per_page=10),ctx=ctx,)
                await paginator.paginate()

    @react.command()
    async def remove(self, ctx, *, trigger):
        if trigger in self.reaction_triggers:
            del self.reaction_triggers[trigger]
            self.save_reaction_triggers()
            await ctx.send(f"Removed reaction trigger for '{trigger}'")
        else:
            await ctx.send(f"No reaction trigger found for '{trigger}'")

    @react.command()
    async def clear(self, ctx):
        self.reaction_triggers.clear()
        self.save_reaction_triggers()
        await ctx.send("Cleared all reaction triggers")
      
              

    @react.command()
    async def add(self, ctx, trigger, reaction):
        if '<@1126351590064930847>' in trigger:
            await ctx.send("You cannot add triggers with that mention.")
            return

        self.reaction_triggers[trigger] = reaction
        self.save_reaction_triggers()
        await ctx.send(f"Added reaction trigger for '{trigger}'")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        for trigger, reaction in self.reaction_triggers.items():
            if trigger.lower() in message.content.lower():
                await message.add_reaction(reaction)