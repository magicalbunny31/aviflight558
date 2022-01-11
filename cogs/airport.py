import discord
from discord.ext import commands
from discord.commands import Option

from assets.data.strip_indents import strip_indents

import json
config = json.loads(open("./config.json", "r").read())

import re

import requests, os

from io import BytesIO

from tabulate import tabulate


class airport(commands.Cog):
   def __init__(self, bot):
      self.bot = bot


   @commands.slash_command(name="airport", description="info about an airport 🛫")
   async def command(self, ctx, code: Option(str, "this airport's IATA/ICAO code 🆔", name="airport-code")):
      # emojis
      airplane = "<:airplane:896512829572644925>"
      hash_char = "<:hash_char:889290260952006707>"
      globe = "<:globe:901948628015415346>"


      # check if this is a valid airport code
      iata_code_regex = re.compile("^[a-z]{3}$")
      is_iata_code = bool(iata_code_regex.match(code))

      icao_code_regex = re.compile("^[a-z]{4}$")
      is_icao_code = bool(icao_code_regex.match(code))

      if not (is_iata_code or is_icao_code):
         return await ctx.respond(
            content = "**`Error: not a valid airport IATA/ICAO code 💥`**",
            ephemeral = True
         )


      # defer the reply
      await ctx.defer()


      # get airport info
      r = requests.get(
         f"https://aerodatabox.p.rapidapi.com/airports/{'iata' if is_iata_code else 'icao'}/{code}?withRunways=true", # https://doc.aerodatabox.com/#operation/GetAirport
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
                  "airport not found"
                  if r.status_code == 404 else
                  "something bad happened with the data, try again later"
               } 💥`**
               > **problem persists? contact `{developer.name}#{developer.discriminator}`**
            """)
         )


      # get response object
      res = r.json()


      # airport data
      name = res["fullName"]

      iata = res.get("iata", None)
      icao = res["icao"]

      serving_short = res.get("shortName", None)
      serving_country = res["country"].get("name", None)

      latitude  = res["location"]["lat"]
      longitude = res["location"]["lon"]


      # links data
      website       = res["urls"].get("webSite",     None)
      wiki          = res["urls"].get("wikipedia",   None)
      twitter       = res["urls"].get("twitter",     None)
      live_atc      = res["urls"].get("liveAtc",     None)
      flightradar24 = res["urls"].get("flightRadar", None)
      maps          = res["urls"].get("googleMaps",  None)

      
      # runways data
      runways = res.get("runways", [])

      runway_rows = list(
         map(
            lambda runway: [
               runway["name"],
               "{:,}".format(round(runway.get("length", {}).get("feet", "---"))),
               runway["surface"]
            ],
            runways
         )
      )


      # image data
      centre = f"{latitude},{longitude}"
      zoom = "13"
      size = "640x360"
      scale = "2"
      format = "png"
      maptype = "satellite"
      key = os.getenv("GOOGLE_STATIC_MAPS_API")


      r = requests.get(
         f"https://maps.googleapis.com/maps/api/staticmap?center={centre}&zoom={zoom}&size={size}&scale={scale}&format={format}&maptype={maptype}&key={key}",
         headers = {
            "User-Agent": f"discord-aviflight558-bot/{config['version']} ({os.getenv('AGENT')}) (https://github.com/magicalbunny31/aviflight558)"
         }
      )

      image = BytesIO(r.content)
      file = discord.File(image, filename=f"{icao}.png")


      # embed fields
      airport_data = strip_indents(f"""
         **`iata`** : {f"`{iata}`" if iata else "---"}
         **`icao`** : `{icao}`

         **`serving`** : {serving_short or "---"}, {serving_country or "---"}
      """)

      links_data = strip_indents(f"""
         **`website      `** : {f"[link]({website} '{website} 🔗')"             if website       else "---"}
         **`wikipedia    `** : {f"[link]({wiki} '{wiki} 🔗')"                   if wiki          else "---"}
         **`twitter      `** : {f"[link]({twitter} '{twitter} 🔗')"             if twitter       else "---"}
         **`LiveATC      `** : {f"[link]({live_atc} '{live_atc} 🔗')"           if live_atc      else "---"}
         **`Flightradar24`** : {f"[link]({flightradar24} '{flightradar24} 🔗')" if flightradar24 else "---"}
         **`Google Maps  `** : {f"[link]({maps} '{maps} 🔗')"                   if maps          else "---"}
      """)

      runways_data = strip_indents(f"""
         ```
         {tabulate(
            runway_rows,
            headers = ["RUNWAY", "LENGTH (ft)", "SURFACE"],
            tablefmt = "simple",
            disable_numparse = True
         ) if runway_rows else "no runway data"}
         ```
      """)


      # embed
      embed = discord.Embed(
         colour = discord.Colour.from_rgb(67, 196, 205), # #43c4cd
         title = f"{name} {airplane}"
      ) \
         .add_field(
            name = "airport",
            value = airport_data,
            inline = False
         ) \
         .set_image(url=f"attachment://{icao}.png")


      # get the embed field to add
      def get_embed_field(field):
         # todo: use match/case when pycord supports python 3.10
         # match field:
         #    case "airport": return airport_data
         #    case "links":   return links_data
         #    case "runways": return runways_data

         if (field == "airport"): return airport_data
         if (field == "links"): return links_data
         if (field == "runways"): return runways_data


      # select menus
      class change_fields(discord.ui.Select):
         def __init__(self):
            super().__init__(
               placeholder = "change fields..",
               options = [
                  discord.SelectOption(
                     label = "airport",
                     value = "airport",
                     emoji = discord.PartialEmoji.from_str(airplane),
                     default = True
                  ),
                  discord.SelectOption(
                     label = "links",
                     value = "links",
                     emoji = discord.PartialEmoji.from_str(globe)
                  ),
                  discord.SelectOption(
                     label = "runways",
                     value = "runways",
                     emoji = discord.PartialEmoji.from_str(hash_char)
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
                     prefer to select options? use the command `/airport`
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
      class flightradar24_button(discord.ui.Button):
         def __init__(self):
            super().__init__(
               style = discord.ButtonStyle.link,
               label = "Flightradar24",
               url = flightradar24 or "https://discord.com",
               emoji = discord.PartialEmoji.from_str(globe),
               disabled = not flightradar24,
               row = 1
            )

      class live_atc_button(discord.ui.Button):
         def __init__(self):
            super().__init__(
               style = discord.ButtonStyle.link,
               label = "LiveATC",
               url = live_atc or "https://discord.com",
               emoji = discord.PartialEmoji.from_str(globe),
               disabled = not live_atc,
               row = 1
            )


      # create a view
      view = discord.ui.View(
         change_fields(),
         flightradar24_button(), live_atc_button(),

         timeout = None
      )


      return await ctx.respond(
         embeds = [embed],
         files = [file],
         view = view
      )


def setup(bot):
   bot.add_cog(airport(bot))