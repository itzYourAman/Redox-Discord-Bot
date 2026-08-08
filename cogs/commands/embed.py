import discord ,asyncio
from discord.ext import commands
from utils.Tools import *



class view(discord.ui.View):
  def __init__(self, ctx,bot, embed):
    super().__init__()
    self.emb= embed
    self.ctx=ctx
    self.bot =bot
    self.msg=None
  async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in [926831289649201213]:
            await interaction.response.send_message("Opps , Looks like you are not the author of the command .", ephemeral=True)
            return False
        return True        

                                                        
  def chk(self,m):
      return m.channel == self.ctx.channel and m.author == self.ctx.author and not m.author.bot 
  @discord.ui.button(label="Title", style=discord.ButtonStyle.grey, row=1)
  async def callback(self, button, interaction):
      for amanop in self.children:
        amanop.disabled=True
      await button.response.edit_message(view=self) 

      bot_msg= None
      try:
            bot_msg = await self.ctx.send("Please enter the title of the embed")
            tit = await self.ctx.bot.wait_for("message", timeout=40, check=self.chk)
            self.emb.title= tit.content
            await bot_msg.delete()
            await tit.delete()
            for amanop in self.children:
              amanop.disabled= False
            await self.msg.edit(embed=self.emb,view=self)
      except Exception as e:
        print(e)
        if bot_msg:
          await bot_msg.delete() 
          await self.ctx.send("Timed Out")

  @discord.ui.button(label="Description", style=discord.ButtonStyle.grey, row=1)
  async def callback2(self, button, interaction):
      for amanop in self.children:
        amanop.disabled=True
      await button.response.edit_message(view=self) 

      bot_msg= None
      try:
            bot_msg = await self.ctx.send("Please enter the description of the embed")
            tit = await self.ctx.bot.wait_for("message", timeout=40, check=self.chk)
            self.emb.description= tit.content
            await bot_msg.delete()
            await tit.delete()
            for amanop in self.children:
              amanop.disabled= False
            await self.msg.edit(embed=self.emb,view=self)
      except Exception as e:
        print(e)
        if bot_msg:
          await bot_msg.delete() 
          await self.ctx.send("Timed Out")            
  @discord.ui.button(label="Author", style=discord.ButtonStyle.grey, row=1)
  async def callback3(self, button, interaction):
      for amanop in self.children:
        amanop.disabled=True
      await button.response.edit_message(view=self) 

      bot_msg= None
      try:
            bot_msg = await self.ctx.send("Please enter the author of the embed")
            tit = await self.ctx.bot.wait_for("message", timeout=40, check=self.chk)
            self.emb.set_author(name= tit.content)
            await bot_msg.delete()
            await tit.delete()
            for amanop in self.children:
              amanop.disabled= False
            await self.msg.edit(embed=self.emb,view=self)
      except Exception as e:
        print(e)
        if bot_msg:
          await bot_msg.delete() 
          await self.ctx.send("Timed Out")
  @discord.ui.button(label="Footer", style=discord.ButtonStyle.grey, row=2)
  async def callback4(self, button, interaction):
      for amanop in self.children:
        amanop.disabled=True
      await button.response.edit_message(view=self) 

      bot_msg= None
      try:
            bot_msg = await self.ctx.send("Please enter the footer of the embed")
            tit = await self.ctx.bot.wait_for("message", timeout=40, check=self.chk)
            self.emb.set_footer(text= tit.content)
            await bot_msg.delete()
            await tit.delete()
            for amanop in self.children:
              amanop.disabled= False
            await self.msg.edit(embed=self.emb,view=self)
      except Exception as e:
        print(e)
        if bot_msg:
          await bot_msg.delete() 
          await self.ctx.send("Timed Out")

  @discord.ui.button(label="Thumbnail", style=discord.ButtonStyle.grey, row=2)
  async def callback5(self, button, interaction):
      for amanop in self.children:
        amanop.disabled=True
      await button.response.edit_message(view=self) 

      bot_msg= None
      try:
            bot_msg = await self.ctx.send("Please enter the thumbnail url of the embed")
            tit = await self.ctx.bot.wait_for("message", timeout=40, check=self.chk) 
            try:
              if not tit.content.startswith(('http://', 'https://')):
                raise ValueError("Invalid URL. Please enter a valid URL.")
              self.emb.set_thumbnail(url=tit.content)
              for amanop in self.children:
                  amanop.disabled= False
              await self.msg.edit(embed=self.emb,view=self)
              await bot_msg.delete()
              await tit.delete()
            except ValueError as ve:
                  xd = await self.ctx.send(str(ve))
                  await asyncio.sleep(2)
                  await xd.delete()
                  await bot_msg.delete()
                  for amanop in self.children:
                    amanop.disabled= False
                  await self.msg.edit(view=self)
      except Exception as e:
        print(e)
        if bot_msg:
          await bot_msg.delete() 
          await self.ctx.send("Timed Out")

  @discord.ui.button(label="Image", style=discord.ButtonStyle.grey, row=2)
  async def callback6(self, button, interaction):
      for amanop in self.children:
        amanop.disabled=True
      await button.response.edit_message(view=self) 

      bot_msg= None
      try:
            bot_msg = await self.ctx.send("Please enter the image url of the embed")
            tit = await self.ctx.bot.wait_for("message", timeout=40, check=self.chk) 
            try:
              if not tit.content.startswith(('http://', 'https://')):
                raise ValueError("Invalid URL. Please enter a valid URL.")
              self.emb.set_image(url=tit.content)
              for amanop in self.children:
                  amanop.disabled= False
              await self.msg.edit(embed=self.emb,view=self)
              await bot_msg.delete()
              await tit.delete()
            except ValueError as ve:
                  xd = await self.ctx.send(str(ve))
                  await asyncio.sleep(2)
                  await xd.delete()
                  await bot_msg.delete()
                  for amanop in self.children:
                    amanop.disabled= False
                  await self.msg.edit(view=self)
      except Exception as e:
        print(e)
        if bot_msg:
          await bot_msg.delete() 
          await self.ctx.send("Timed Out")
          

  @discord.ui.button(label="Color", style=discord.ButtonStyle.grey, row=3)
  async def cal(self, button, interaction):
    for amanop in self.children:
        amanop.disabled=True
    await button.response.edit_message(view=self)
    bot_msg= None
    try:
        bot_msg = await self.ctx.send("Please enter the color of the embed (e.g. #ff0000)")
        tit = await self.ctx.bot.wait_for("message", timeout=40, check=self.chk)
        try:
            if not tit.content.startswith('#'):
                raise ValueError("Invalid color. Please enter a valid color code (e.g. #ff0000).")
            self.emb.color = discord.Color(int(tit.content.lstrip('#'), 16))
            for amanop in self.children:
                amanop.disabled= False
            await self.msg.edit(embed=self.emb,view=self)
            await bot_msg.delete()
            await tit.delete()
        except:
            xd = await self.ctx.send(f"Invalid color: {tit.content}. Please enter a valid color code (e.g. #ff0000).")
            await asyncio.sleep(2)
            await xd.delete()
            await bot_msg.delete()
            for amanop in self.children:
                amanop.disabled= False
            await self.msg.edit(view=self)
    except Exception as e:
      print(e)
      if bot_msg:
        await bot_msg.delete()
      await self.ctx.send("Timed Out")
  @discord.ui.button(label="Send", style=discord.ButtonStyle.grey, row=3)
  async def call(self, button, interaction):
        for amanop in self.children:
          amanop.disabled=True
        await button.response.edit_message(view=self)  
        try:
            msg=await self.ctx.send("Please mention the channel where you want to send this embed.")
            chan_mention = await self.ctx.bot.wait_for("message", timeout=30, check=self.chk)
            channel = discord.utils.get(self.ctx.guild.channels, mention=chan_mention.content)
            if channel:
                await channel.send(embed=self.emb)
                await self.ctx.send("Embed sent to the channel successfully.")
                await msg.delete()
                await self.msg.edit(view=None)
            else:
                await msg.delete()
                await self.ctx.send("Invalid channel mention.")   
                for amanop in self.children:
                  amanop.disabled=False
                await self.msg.edit(view=self)
        except Exception as e:
            print(e)
            await self.ctx.send("Timed Out or an error occurred")
    


class Embed(commands.Cog):
    def __init__(self, bot):
      self.bot = bot 
    @commands.hybrid_command(name="embed",help="Create a embed using Redox")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def embed(self, ctx):
      embed = discord.Embed(description="This Is An Example Embed, You Can Customize Everything")
      views = view(ctx,self.bot,embed)  
      msg=await ctx.send(embed=embed, view=views)
      views.msg= msg