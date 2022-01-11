import discord
from discord.ext import commands

from assets.data.strip_indents import strip_indents

import json
config = json.loads(open("./config.json", "r").read())


class apis(commands.Cog):
   def __init__(self, bot):
      self.bot = bot


   @commands.slash_command(name="apis", description="the APIs used for data 🦊")
   async def command(self, ctx):
      # api urls
      aerodatabox     = "https://www.aerodatabox.com/"
      maps_static_api = "https://developers.google.com/maps/documentation/maps-static/overview"
      opensky_network = "https://opensky-network.org/"


      # embeds
      embeds = [
         discord.Embed(
            colour = discord.Colour.from_rgb(67, 196, 205), # #43c4cd
            description = strip_indents(f"""
               `AeroDataBox           ` : [link]({aerodatabox} "{aerodatabox} 🔗")
               `Google Maps Static API` : [link]({maps_static_api} "{maps_static_api} 🔗")
               `OpenSky Network       ` : [link]({opensky_network} "{opensky_network} 🔗")
            """)
         ),
         discord.Embed(
            colour = discord.Colour.from_rgb(67, 196, 205), # #43c4cd
            description = strip_indents(f"""
               `source code` : [link to github repository]({config["github"]} "{config["github"]} 🔗")
            """)
         ),
      ]


      # reply ephemerally
      return await ctx.respond(
         embeds = embeds,
         ephemeral = True
      )



def setup(bot):
   bot.add_cog(apis(bot))