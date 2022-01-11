import discord
from discord.ext      import commands
from discord.commands import Option

import json
config = json.loads(open("./config.json", "r").read())

import requests, os
from io import BytesIO
from asyncio import sleep


class uwu(commands.Cog):
   def __init__(self, bot):
      self.bot = bot


   @commands.slash_command(name="uwu", description="testtesttesttest 🦊🐾")
   async def command(self, ctx):
      zoom = "9"
      size = "640x360"
      scale = "2"
      format = "png"
      maptype = "satellite"
      key = os.getenv("GOOGLE_STATIC_MAPS_API")

      await ctx.defer(
         ephemeral = True
      )

      r = requests.get(
         f"https://maps.googleapis.com/maps/api/staticmap?center=50.7811,-1.841&zoom=9&size=640x360&scale=2&format=png&maptype=satellite&markers=anchor:center%7Cicon:https://media.discordapp.net/attachments/927585144775278662/929898049768136774/triangle_flag.png%7C50.7811,-1.841&key=AIzaSyAdF6VYSMuKjl30FMz61G5O1nIJsqGq_Gc",
         headers = {
            "User-Agent": f"discord-aviflight558-bot/{config['version']} ({os.getenv('AGENT')}) (https://github.com/magicalbunny31/aviflight558)"
         }
      )


      # image = BytesIO(r.content)
      # file = discord.File(image, filename=f"asdf.png")
      file = discord.File("./asdf.lua")

      await ctx.respond(
         files = [file]
      )



def setup(bot):
   bot.add_cog(uwu(bot))