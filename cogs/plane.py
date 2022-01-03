import discord, random, os
from discord.ext import commands


class plane(commands.Cog):
   def __init__(self, bot):
      self.bot = bot


   @commands.slash_command(name="plane", description="get a random image of Aviation558's planes 📸")
   async def command(self, ctx):
      await ctx.defer()

      plane = random.choice(os.listdir("./assets/images"))
      [id, ext] = plane.split('.')
      attachment = discord.File(filename=f"plane.{ext}", fp=f"./assets/images/{plane}")

      camcorder = "<:camcorder:924387366225981510>"
      view = discord.ui.View(
         discord.ui.Button(
            style = discord.ButtonStyle.link,
            label = "Aviation558",
            url = "https://www.instagram.com/aviation558_",
            emoji = discord.PartialEmoji.from_str(camcorder)
         )
      )

      return await ctx.interaction.edit_original_message(
         content = f"> id: **`{id}`**",
         files = [attachment],
         view = view
      )


def setup(bot):
   bot.add_cog(plane(bot))