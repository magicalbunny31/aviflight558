import discord
from discord.ext import commands
from discord.commands import Option

from assets.data.strip_indents import strip_indents

import json
config = json.loads(open("./config.json", "r").read())

import requests, os

from dateutil import parser

import re


class aircraft(commands.Cog):
   def __init__(self, bot):
      self.bot = bot


   @commands.slash_command(name="aircraft", description="info about an aircraft ✈️")
   async def command(self, ctx, registration: Option(str, "this aircraft's registration 🆔", name="aircraft-registration")):
      # emojis
      airplane = "<:airplane:896512829572644925>"
      calendar_spiral = "<:calendar_spiral:897530264782258236>"

      yes = "<:yes:792173102146519051>"
      no  = "<:no:792173102377205811>"

      info = "<:info:792165588331921489>"
      camcorder = "<:camcorder:924387366225981510>"


      # defer the reply
      await ctx.defer()


      # get aircraft info
      r = requests.get(
         f"https://aerodatabox.p.rapidapi.com/aircrafts/reg/{registration.lower()}", # https://doc.aerodatabox.com/#operation/GetAircraft
         headers = {
            "Accept": "application/json",
            "User-Agent": f"discord-aviflight558-bot/{config['version']} ({os.getenv('AGENT')}) (https://github.com/magicalbunny31/aviflight558)",
            "X-RapidAPI-Key": os.getenv("RAPIDAPI_APPLICTION_KEY")
         }
      )

      # response isn't okai
      if not r.ok:
         developer = await self.bot.fetch_user(config["developer"])
         return await ctx.interaction.edit_original_message(
            content = strip_indents(f"""
               **`Error: {
                  "out of command uses for this month"
                  if r.status_code == 429 else
                  "aircraft not found"
                  if r.status_code == 404 else
                  "not a valid aircraft registration"
                  if r.status_code == 400 else
                  "something bad happened with the data, try again later"
               } 💥`**
               > **problem persists? contact `{developer.name}#{developer.discriminator}`**
            """)
         )


      # get response object
      res = r.json()


      # format a time string to unix timestamp
      to_unix_timestamp = lambda time: int(parser.parse(time).timestamp()) if time else 0


      # aircraft data
      aircraft_registration = res["reg"]
      icao24                = res.get("hexIcao", None)
      serial                = res.get("serial",  None)
      
      type      = res.get("typeName",     None)
      model     = res.get("modelCode",    None)

      is_active    = yes if res["active"]      else no
      is_freighter = yes if res["isFreighter"] else no

      airline = res.get("airlineName", None)


      # dates data
      rollout      = to_unix_timestamp(res.get("rolloutDate",      0))
      first_flight = to_unix_timestamp(res.get("firstFlightDate",  0))
      delivered    = to_unix_timestamp(res.get("deliveryDate",     0))
      registered   = to_unix_timestamp(res.get("registrationDate", 0))
   
      
      # image data
      aircraft_image_url    = res.get("image", {}).get("url",    discord.Embed.Empty)
      aircraft_image_source = res.get("image", {}).get("webUrl", None)
      aircraft_image_author = res.get("image", {}).get("author", discord.Embed.Empty)
   
      license_regex               = "(https:\/\/creativecommons\.org\/licenses\/by[-a-s]*\/[0-9.]*\/?)|(CC0? BY[-A-Z]*[ 0-9.]*)"
      aircraft_image_attributions = res.get("image", {}).get("htmlAttributions", "")

      aircraft_image             = ["".join(match) for match in re.findall(license_regex, json.dumps(aircraft_image_attributions))]
      aircraft_image_license_url = aircraft_image[0] if 0 < len(aircraft_image) else None
      aircraft_image_license     = aircraft_image[1] if 1 < len(aircraft_image) else None


      # embed fields
      aircraft_data = strip_indents(f"""
         **`registration       `** : `{aircraft_registration}`
         **`icao 24-bit address`** : {f"`{icao24}`" if icao24 else "---"}
         **`serial number      `** : {f"`{serial}`" if serial else "---"}

         **`aircraft type `** : {type  or "---"}
         **`aircraft model`** : {model or "---"}

         **`active   `** : {is_active}
         **`freighter`** : {is_freighter}

         **`airline`** : {airline or "---"}
      """)

      dates_data = strip_indents(f"""
         **`roll-out`**
         {f"<t:{rollout}:D>" if rollout else "---"}

         **`first flight`**
         {f"<t:{first_flight}:D>" if first_flight else "---"}

         **`delivered`**
         {f"<t:{delivered}:D>" if delivered else "---"}

         **`registered`**
         {f"<t:{registered}:D>" if registered else "---"}
      """)


      # embed
      embed = discord.Embed(
         colour = discord.Colour.from_rgb(67, 196, 205), # #43c4cd
         title = f"{aircraft_registration} {airplane}"
      ) \
         .add_field(
            name = "aircraft",
            value = aircraft_data,
            inline = False
         ) \
         .set_image(url=aircraft_image_url) \
         .set_footer(text=aircraft_image_author)


      # get the embed field to add
      def get_embed_field(field):
         # todo: use match/case when pycord supports python 3.10
         # match field:
         #    case "aircraft": return aircraft_data
         #    case "dates":    return dates_data

         if (field == "aircraft"): return aircraft_data
         if (field == "dates"): return dates_data


      # select menu
      class change_fields(discord.ui.Select):
         def __init__(self):
            super().__init__(
               placeholder = "change fields..",
               options = [
                  discord.SelectOption(
                     label = "aircraft",
                     value = "aircraft",
                     emoji = discord.PartialEmoji.from_str(airplane),
                     default = True
                  ),
                  discord.SelectOption(
                     label = "dates",
                     value = "dates",
                     emoji = discord.PartialEmoji.from_str(calendar_spiral)
                  )
               ],
               row = 0
            )

         async def callback(self, interaction: discord.Interaction):
            [selection] = self.values

            # this isn't the user who used the command
            if interaction.user.id != ctx.user.id:
               return await interaction.response.send_message(
                  content = strip_indents(f"""
                     since {ctx.user.mention} used this command, only they can use the select menu!
                     prefer to select options? use the command `/aircraft`
                  """),
                  ephemeral = True
               )

            # remove the embed field and add the selected embed field
            embed.clear_fields()
            embed.add_field(
               name = selection,
               value = get_embed_field(selection),
               inline = False
            )

            # change the select menu's default value
            for option in self.options: option.default = False
            self.options[[i.value for i in self.options].index(selection)].default = True

            # update the interaction
            return await interaction.response.edit_message(
               embeds = [embed],
               view = self.view
            )


      # buttons
      class image_source(discord.ui.Button):
         def __init__(self):
            super().__init__(
               style = discord.ButtonStyle.link,
               label = "image source",
               url = aircraft_image_source or "https://discord.com",
               emoji = discord.PartialEmoji.from_str(camcorder),
               disabled = not aircraft_image_source,
               row = 1
            )

      class image_license(discord.ui.Button):
         def __init__(self):
            super().__init__(
               style = discord.ButtonStyle.link,
               label = aircraft_image_license or "no image",
               url = aircraft_image_license_url or "https://discord.com",
               emoji = discord.PartialEmoji.from_str(info),
               disabled = not aircraft_image_license_url,
               row = 1
            )


      # create a view
      view = discord.ui.View(
         change_fields(),
         image_source(), image_license(),

         timeout = None
      )


      # edit the interaction
      return await ctx.interaction.edit_original_message(
         embeds = [embed],
         view = view
      )



def setup(bot):
   bot.add_cog(aircraft(bot))