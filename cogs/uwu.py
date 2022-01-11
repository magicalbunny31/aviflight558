import discord
from discord.ext      import commands
from discord.commands import Option

import json
config = json.loads(open("./config.json", "r").read())

import os


class uwu(commands.Cog):
   def __init__(self, bot):
      self.bot = bot


   @commands.slash_command(name="uwu", description="testtesttesttest 🦊🐾")
   async def command(self, ctx, coords: Option(str, "coords")):
      zoom = "9"
      size = "640x360"
      scale = "2"
      format = "png"
      maptype = "satellite"
      key = os.getenv("GOOGLE_STATIC_MAPS_API")

      return await ctx.respond(
         content = f"`https://maps.googleapis.com/maps/api/staticmap?center={coords}&zoom={zoom}&size={size}&scale={scale}&format={format}&maptype={maptype}&key={key}`",
         ephemeral = True
      )



def setup(bot):
   bot.add_cog(uwu(bot))