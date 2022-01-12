import discord
from discord.ext import commands
from discord.commands import Option

from assets.data.strip_indents import strip_indents

import json
config = json.loads(open("./config.json", "r").read())

import re

import requests, os

from dateutil import parser
import time


class flight(commands.Cog):
   def __init__(self, bot):
      self.bot = bot


   @commands.slash_command(name="flight", description="info about a flight 🛩️")
   async def command(self, ctx, callsign: Option(str, "this flight's IATA/ICAO callsign 🆔")):
      # emojis
      info = "<:info:792165588331921489>"
      airplane = "<:airplane:896512829572644925>"
      national_park = "<:national_park:809180470771712021>"

      yes = "<:yes:792173102146519051>"
      no  = "<:no:792173102377205811>"

      camcorder = "<:camcorder:924387366225981510>"


      # check if this is a valid callsign
      callsign_regex = re.compile("(^[a-z0-9]{2} ?[0-9]+$)|(^[a-z]{3} ?[0-9]{1,4}[a-z]*$)", re.I)
      is_callsign = bool(callsign_regex.match(callsign))

      if not is_callsign:
         return await ctx.respond(
            content = "**`Error: not a valid IATA/ICAO callsign 💥`**",
            ephemeral = True
         )


      # defer the reply
      await ctx.defer()


      # get flight info
      r = requests.get(
         f"https://aerodatabox.p.rapidapi.com/flights/number/{callsign.lower()}?withAircraftImage=true&withLocation=true", # https://doc.aerodatabox.com/#operation/GetFlight
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
                  "something bad happened with the data, try again later"
               } 💥`**
               > **problem persists? contact `{developer.name}#{developer.discriminator}`**
            """)
         )

     
      # get response object
      r = r.json()


      # flight not found
      if not r:
         return await ctx.respond(
            content = "**`Error: flight not found 💥`**",
            ephemeral = True
         )


      # format a time string to unix timestamp
      to_unix_timestamp = lambda time: int(parser.parse(time).timestamp()) if time else 0


      # get the first flight data that has an aircraft flying, or just the flight data
      res_last_updated_times = [to_unix_timestamp(x["lastUpdatedUtc"]) for x in r]
      res_latest_updated_time = max(res_last_updated_times)
      res_index = next((i for (i, x) in enumerate(r) if to_unix_timestamp(x["lastUpdatedUtc"]) == res_latest_updated_time), None)
      res = r[res_index]


      # departure data
      departure_airport_icao       = res["departure"].get("airport", {}).get("icao",      None)
      departure_airport_iata       = res["departure"].get("airport", {}).get("iata",      None)
      departure_airport_name       = res["departure"].get("airport", {}).get("name",      None)
      departure_airport_short_name = res["departure"].get("airport", {}).get("shortName", None)

      scheduled_departure_time = to_unix_timestamp(res["departure"].get("scheduledTimeUtc", 0))
      actual_departure_time    = to_unix_timestamp(res["departure"].get("actualTimeUtc",    0)) # if "takeoff_time" is defined, this will be the time the aircraft left the gate instead
      takeoff_time             = to_unix_timestamp(res["departure"].get("runwayTimeUtc",    0))

      departure_terminal       = res["departure"].get("terminal",    None)
      check_in_desk            = res["departure"].get("checkInDesk", None)
      departure_gate           = res["departure"].get("gate",        None)
      takeoff_runway           = res["departure"].get("runway",      None)

      next_departure = "next " if scheduled_departure_time > int(time.time()) else ""


      # arrival data
      arrival_airport_icao       = res["arrival"].get("airport", {}).get("icao",      None)
      arrival_airport_iata       = res["arrival"].get("airport", {}).get("iata",      None)
      arrival_airport_name       = res["arrival"].get("airport", {}).get("name",      None)
      arrival_airport_short_name = res["arrival"].get("airport", {}).get("shortName", None)

      scheduled_arrival_time = to_unix_timestamp(res["arrival"].get("scheduledTimeUtc", 0))
      actual_arrival_time    = to_unix_timestamp(res["arrival"].get("actualTimeUtc",    0)) # if "landing_time" is defined, this will be the time the aircraft arrived at the gate instead
      landing_time           = to_unix_timestamp(res["arrival"].get("runwayTimeUtc",    0))

      arrival_terminal       = res["arrival"].get("terminal",    None)
      arrival_gate           = res["arrival"].get("gate",        None)
      baggage_belt           = res["arrival"].get("baggageBelt", None)
      landing_runway         = res["arrival"].get("runway",      None)

      next_arrival = "next " if next_departure else "" # the next scheduled arrival only really makes sense if the departure is in the future too


      # last update of this information (excluding location data)
      last_updated = to_unix_timestamp(res["lastUpdatedUtc"])


      # flight info
      flight_number   = res["number"]
      flight_callsign = res.get("callSign", None)


      # get this flight's current status
      def get_status():
         # todo: use match/case when pycord supports python 3.10
         # match res["status"]:
         #    case "EnRoute":           return "en route"
         #    case "CheckIn":           return "open for check-in"
         #    case "GateClosed":        return "gate has closed"
         #    case "Canceled":          return "flight cancelled"
         #    case "CanceledUncertain": return "flight cancelled/uncertain"
         #    case _:                   return res["status"].lower() # i'm too lazy to re-write all the others

         if (res["status"] == "EnRoute"): return "en route"
         elif (res["status"] == "CheckIn"): return "open for check-in"
         elif (res["status"] == "GateClosed"): return "gate has closed"
         elif (res["status"] == "Canceled"): return "flight cancelled"
         elif (res["status"] == "CanceledUncertain"): return "flight cancelled/uncertain"
         else: return res["status"].lower()


      # this is a cargo flight
      is_cargo = yes if res["isCargo"] else no


      # aircraft data (if this flight has an aircraft currently flying)
      aircraft_registration = res.get("aircraft", {}).get("reg",   None)
      aircraft_icao24       = res.get("aircraft", {}).get("modeS", None)
      aircraft_model        = res.get("aircraft", {}).get("model", None)

      aircraft_image_url    = res.get("aircraft", {}).get("image", {}).get("url",    discord.Embed.Empty)
      aircraft_image_source = res.get("aircraft", {}).get("image", {}).get("webUrl", None)
      aircraft_image_author = res.get("aircraft", {}).get("image", {}).get("author", discord.Embed.Empty)
   
      license_regex               = "(https:\/\/creativecommons\.org\/licenses\/by[-a-s]*\/[0-9.]*\/?)|(CC0? BY[-A-Z]*[ 0-9.]*)"
      aircraft_image_attributions = res.get("aircraft", {}).get("image", {}).get("htmlAttributions", "")

      aircraft_image             = ["".join(match) for match in re.findall(license_regex, json.dumps(aircraft_image_attributions))]
      aircraft_image_license_url = aircraft_image[0] if 0 < len(aircraft_image) else None
      aircraft_image_license     = aircraft_image[1] if 1 < len(aircraft_image) else None


      # airline data
      airline_name = res.get("airline", {}).get("name", None)


      # location data
      altitude              = res.get("location", {}).get("pressureAltFt", None)
      ground_speed          = res.get("location", {}).get("gsKt",          None)
      heading               = res.get("location", {}).get("trackDeg",      None)
      latitude              = res.get("location", {}).get("lat",           None)
      longitude             = res.get("location", {}).get("lon",           None)
      
      location_last_updated = to_unix_timestamp(res.get("location", {}).get("reportedAtUtc", 0))


      # embed fields
      departure_data = strip_indents(f"""
         **`departure airport`**
         {f"`{departure_airport_iata}`" if departure_airport_iata else "---"}/{f"`{departure_airport_icao}`" if departure_airport_icao else "---"} - {departure_airport_short_name or departure_airport_name}
         
         **`{next_departure}scheduled departure time`**
         {f"<t:{scheduled_departure_time}>" if scheduled_departure_time else "---"}

         **`{"left gate at" if takeoff_time else "actual departure time"}`**
         {f"<t:{actual_departure_time}>" if actual_departure_time else "---"}

         **`takeoff time`**
         {f"<t:{takeoff_time}>" if takeoff_time else "---"}

         **`terminal      `** : {f"terminal `{departure_terminal}`" if departure_terminal else "---"}
         **`check-in desk `** : {f"desk `{check_in_desk}`"          if check_in_desk      else "---"}
         **`gate          `** : {f"gate `{departure_gate}`"         if departure_gate     else "---"}
         **`takeoff runway`** : {f"`RWY {takeoff_runway}`"          if takeoff_runway     else "---"}

         **`last updated`** : {f"<t:{last_updated}>"}
      """)

      arrival_data = strip_indents(f"""
         **`arrival airport`**
         {f"`{arrival_airport_iata}`" if arrival_airport_iata else "---"}/{f"`{arrival_airport_icao}`" if arrival_airport_icao else "---"} - {arrival_airport_short_name or arrival_airport_name}
         
         **`{next_arrival}scheduled arrival time`**
         {f"<t:{scheduled_arrival_time}>" if scheduled_arrival_time else "---"}

         **`{"arrived to gate at " if landing_time else "actual arrival time"}`**
         {f"<t:{actual_arrival_time}>" if actual_arrival_time else "---"}

         **`landing time`**
         {f"<t:{landing_time}>" if landing_time else "---"}

         **`terminal      `** : {f"terminal `{arrival_terminal}`" if arrival_terminal else "---"}
         **`gate          `** : {f"gate `{arrival_gate}`"         if arrival_gate     else "---"}
         **`baggage belt  `** : {f"belt `{baggage_belt}`"         if baggage_belt     else "---"}
         **`landing runway`** : {f"`RWY {landing_runway}`"        if landing_runway   else "---"}

         **`last updated`** : {f"<t:{last_updated}>"}
      """)

      flight_data = strip_indents(f"""
         **`flight number`** : `{flight_number}`
         **`callsign     `** : {f"`{flight_callsign}`" if flight_callsign else "---"}
         **`status       `** : `{get_status()}`
         **`cargo flight `** : {is_cargo}

         **`last updated`** : {f"<t:{last_updated}>"}
      """)

      aircraft_data = strip_indents(f"""
         **`registration       `** : {f"`{aircraft_registration}`" if aircraft_registration else "---"}
         **`icao 24-bit address`** : {f"`{aircraft_icao24}`"       if aircraft_icao24       else "---"}
         **`aircraft model     `** : {aircraft_model}

         **`airline`** : {airline_name}
      """)

      location_data = strip_indents(f"""
         **`altitude    `** : {f"`{altitude}ft`"                        if altitude              else "---"}
         **`ground speed`** : {f"`{ground_speed}kn`"                    if ground_speed          else "---"}
         **`heading     `** : {f"`{heading}°`"                          if heading               else "---"}
         **`position    `** : {f"lon: `{longitude}`, lat: `{latitude}`" if longitude or latitude else "---"}

         **`last updated`** : {f"<t:{location_last_updated}:R>" if location_last_updated else "---"}
      """)


      # embed
      embed = discord.Embed(
         colour = discord.Colour.from_rgb(67, 196, 205), # #43c4cd
         title = f"{flight_number} {airplane}"
      ) \
         .add_field(
            name = "departure",
            value = departure_data,
            inline = False
         ) \
         .set_image(url=aircraft_image_url) \
         .set_footer(text=aircraft_image_author)


      # get the embed field to add
      def get_embed_field(field):
         # todo: use match/case when pycord supports python 3.10
         # match field:
         #    case "departure": return departure_data
         #    case "arrival":   return arrival_data
         #    case "flight":    return flight_data
         #    case "aircraft":  return aircraft_data
         #    case "location":  return location_data

         if (field == "departure"): return departure_data
         if (field == "arrival"): return arrival_data
         if (field == "flight"): return flight_data
         if (field == "aircraft"): return aircraft_data
         if (field == "location"): return location_data


      # select menu
      class change_fields(discord.ui.Select):
         def __init__(self):
            super().__init__(
               placeholder = "change fields..",
               options = [
                  discord.SelectOption(
                     label = "departure",
                     value = "departure",
                     emoji = discord.PartialEmoji.from_str(info),
                     default = True
                  ),
                  discord.SelectOption(
                     label = "arrival",
                     value = "arrival",
                     emoji = discord.PartialEmoji.from_str(info)
                  ),
                  discord.SelectOption(
                     label = "flight",
                     value = "flight",
                     emoji = discord.PartialEmoji.from_str(airplane)
                  ),
                  discord.SelectOption(
                     label = "aircraft",
                     value = "aircraft",
                     emoji = discord.PartialEmoji.from_str(airplane)
                  ),
                  discord.SelectOption(
                     label = "location",
                     value = "location",
                     emoji = discord.PartialEmoji.from_str(national_park)
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
                     prefer to select options? use the command `/flight`
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
   bot.add_cog(flight(bot))