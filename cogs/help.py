import discord, emoji
from discord.ext import commands

import json
config = json.loads(open("./config.json", "r").read())

from assets.data.strip_indents import strip_indents


class help(commands.Cog):
   def __init__(self, bot):
      self.bot = bot


   @commands.slash_command(name="help", description="help with aviflight558 ✈️")
   async def command(self, ctx):
      replace_emoji = lambda match: f"\\{match.group()}" 
      commands = "\n".join(set(map(lambda command: f"› `/{command.name}` - {emoji.get_emoji_regexp().sub(replace_emoji, command.description)}", self.bot.commands)))

      happ = "<:happ:906683365791502366>"
      yellow_book = "<:yellow_book:809123390438768660>"
      developer = f"<@{config['developer']}>"

      embed = discord.Embed(
         colour = discord.Colour.from_rgb(67, 196, 205), # #43c4cd
         description = strip_indents(f"""
            {self.bot.user.mention} : **{emoji.get_emoji_regexp().sub(replace_emoji, ctx.guild.name if ctx.guild is not None else ctx.user.mention)}**

            **commands** {yellow_book}
            {commands}

            `developer` › {developer} 2022 {happ}
            `github` › [link to repository]({config["github"]} "{config["github"]} 🔗")
         """)
      )

      return await ctx.respond(embeds=[embed])


def setup(bot):
   bot.add_cog(help(bot))