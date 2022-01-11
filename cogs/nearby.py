import discord
from discord.ext import commands
from discord.commands import Option, OptionChoice

from assets.data.strip_indents import strip_indents
from assets.data.calculate_distance import calculate_distance

import json
config = json.loads(open("./config.json", "r").read())

import requests, os

from io import BytesIO

from tabulate import tabulate


class nearby(commands.Cog):
   def __init__(self, bot):
      self.bot = bot


   choices = [
      OptionChoice("Bournemouth Airport 🇬🇧 (BOH/EGHH) 🛫",                              "boh"),
      OptionChoice("Exeter Airport 🇬🇧 (EXT/EGTE) 🛫",                                   "ext"),
      OptionChoice("London Heathrow Airport 🇬🇧 (LHR/EGLL) 🛫",                          "lhr"),
      OptionChoice("London Gatwick Airport 🇬🇧 (LGW/EGKK) 🛫",                           "lgw"),
      OptionChoice("Paris Charles de Gaulle Airport 🇫🇷 (CDG/LFPG) 🛫",                  "cdg"),
      OptionChoice("Frankfurt Airport 🇩🇪 (FRA/EDDF) 🛫",                                "fra"),
      OptionChoice("Madrid Barajas Airport 🇪🇸 (MAD/LEMD) 🛫",                           "mad"),
      OptionChoice("New York John F. Kennedy International Airport 🇺🇸 (JFK/KJFK) 🛫",   "jfk"),
      OptionChoice("Pittsburgh International Airport 🇺🇸 (PIT/KPIT) 🛫",                 "pit"),
      OptionChoice("Atlanta Hartsfield-Jackson International Airport 🇺🇸 (ATL/KATL) 🛫", "atl"),
      OptionChoice("Chicago O'Hare International Airport 🇺🇸 (ORD/KORD) 🛫",             "ord"),
      OptionChoice("Dallas Fort Worth International Airport 🇺🇸 (DFW/KDFW) 🛫",          "dfw"),
      OptionChoice("Jacksonville International Airport 🇺🇸 (JAX/KJAX) 🛫",               "jax"),
      OptionChoice("Orlando International Airport 🇺🇸 (MCO/KMCO) 🛫",                    "mco"),
      OptionChoice("Los Angeles International Airport 🇺🇸 (LAX/KLAX) 🛫",                "lax"),
      OptionChoice("Vancouver International Airport 🇨🇦 (YVR/CYVR) 🛫",                  "yvr"),
      OptionChoice("Sao Paulo Guarulhos International Airport 🇧🇷 (GRU/SBGR) 🛫",        "gru"),
      OptionChoice("Dubai International Airport 🇦🇪 (DXB/OMDB) 🛫",                      "dxb"),
      OptionChoice("Singapore Changi Airport 🇸🇬 (SIN/WSSS) 🛫",                         "sin"),
      OptionChoice("Manila Ninoy Aquino International Airport 🇵🇭 (MNL/RPLL) 🛫",        "mnl"),
      OptionChoice("Seoul Incheon International Airport 🇰🇷 (ICN/RKSI) 🛫",              "icn"),
      OptionChoice("Tokyo Narita International Airport 🇯🇵 (NRT/RJAA) 🛫",               "nrt"),
      OptionChoice("Sydney Kingsford Smith Airport 🇦🇺 (SYD/YSSY) 🛫",                   "syd"),
      OptionChoice("Auckland Airport 🇳🇿 (AKL/NZAA) 🛫",                                 "akl")
   ]

   @commands.slash_command(name="nearby", description="lookup nearby aircraft 🔎")
   async def command(self, ctx, area: Option(str, "area to search 🗺️", choices=choices)):
      # emojis
      airplane = "<:airplane:896512829572644925>"


      # marker icons
      triangle_flag_marker = "https://media.discordapp.net/attachments/927585144775278662/929898049768136774/triangle_flag.png"
      airplane_marker = "https://media.discordapp.net/attachments/927585144775278662/929898049440993320/airplane.png"

      
      # airport coordinates
      airport_data = { #  i *could* find a formula to automatically get these, but....i can't find one right now >w>
         "boh": {
            "name": "Bournemouth Airport",
            "la":  50.7811,
            "lo": - 1.8410,

            "lamin":  50.460875525342790,
            "lomin": - 2.719339898146346,
            "lamax":  51.100327367948495,
            "lomax": - 0.949485733082829
         },
         "ext": {
            "name": "Exeter Airport",
            "la":  50.7350,
            "lo": - 3.4153,

            "lamin":  50.415847079739620,
            "lomin": - 4.319282915033121,
            "lamax":   51.05194461562965,
            "lomax": - 2.532722884583755
         },
         "lhr": {
            "name": "London Heathrow Airport",
            "la":  51.4700,
            "lo": - 0.4543,

            "lamin":  51.154608322094750,
            "lomin": - 1.356855991629260,
            "lamax":  51.786800771678440,
            "lomax":   0.448223509864210
         },
         "lgw": {
            "name": "London Gatwick Airport",
            "la":  51.1537,
            "lo": - 0.1821,

            "lamin":  50.841047736504340,
            "lomin": - 1.078300089893334,
            "lamax":  51.471392664172270,
            "lomax":   0.709801407364011
         },
         "cdg": {
            "name": "Paris Charles de Gaulle Airport",
            "la": 49.0097,
            "lo":  2.5480,

            "lamin": 48.7075757091366550,
            "lomin":  1.7249257658565418,
            "lamax": 49.3139279091122660,
            "lomax":  3.3632086725770970
         },
         "fra": {
            "name": "Frankfurt Airport",
            "la": 50.0379,
            "lo":  8.5622,

            "lamin": 49.7076031606075050,
            "lomin":  7.6399474056987020,
            "lamax": 50.3719931286164500,
            "lomax":  9.4788577042499310
         },
         "mad": {
            "name": "Madrid Barajas Airport",
            "la":  40.4983,
            "lo": - 3.5676,

            "lamin":  40.112508214557900,
            "lomin": - 4.471434284883078,
            "lamax":  40.887466191043260,
            "lomax": - 2.663527720740442
         },
         "jfk": {
            "name": "New York John F. Kennedy International Airport",
            "la":  40.6413,
            "lo": -73.7781,

            "lamin":  40.236234184666730,
            "lomin": -74.728091784916270,
            "lamax":  41.046665662794860,
            "lomax": -72.832031099353370 
         },
         "pit": {
            "name": "Pittsburgh International Airport",
            "la":  40.4919,
            "lo": -80.2352,

            "lamin":  40.112237113905906,
            "lomin": -81.129047947371160,
            "lamax":  40.871491440556460,
            "lomax": -79.345143218470270
         },
         "atl": {
            "name": "Atlanta Hartsfield-Jackson International Airport",
            "la":  33.6407,
            "lo": -84.4277,

            "lamin":  33.237556369914564,
            "lomin": -85.294184861308410,
            "lamax":  34.043951683884536,
            "lomax": -83.562398585368810
         },
         "ord": {
            "name": "Chicago O'Hare International Airport",
            "la":  41.9803,
            "lo": -87.9090,

            "lamin":  41.607971001503990,
            "lomin": -88.799206485670230,
            "lamax":  42.351159201809494,
            "lomax": -87.019421518825270
         },
         "dfw": {
            "name": "Dallas Fort Worth International Airport",
            "la":  32.8998,
            "lo": -97.0403,

            "lamin":  32.455562270303610,
            "lomin": -97.988727175541360,
            "lamax":  33.344872650852670,
            "lomax": -96.101655762267630
         },
         "jax": {
            "name": "Jacksonville International Airport",
            "la":  30.4941,
            "lo": -81.6879,

            "lamin":  30.058759752267330,
            "lomin": -82.592706228583040,
            "lamax":  30.932049516762753,
            "lomax": -80.786213195764990
         },
         "mco": {
            "name": "Orlando International Airport",
            "la":  28.4179,
            "lo": -81.3041,

            "lamin":  27.983045073334196,
            "lomin": -82.186736233966120,
            "lamax":  28.851452008381504,
            "lomax": -80.428924029968330
         },
         "lax": {
            "name": "Los Angeles International Airport",
            "la":   33.9416,
            "lo": -118.4085,

            "lamin":   33.521298161601536,
            "lomin": -119.315140267699700,
            "lamax":   34.364424937999964,
            "lomax": -117.504406640907890
         },
         "yvr": {
            "name": "Vancouver International Airport",
            "la":   49.1967,
            "lo": -123.1815,

            "lamin":   48.87078838081826,
            "lomin": -124.07773344978166,
            "lamax":   49.52749796818695,
            "lomax": -122.28654901890837
         },
         "gru": {
            "name": "Sao Paulo Guarulhos International Airport",
            "la": -23.4306,
            "lo": -46.4730,

            "lamin": -23.875520202357870,
            "lomin": -47.343926576726870,
            "lamax": -22.978222163070640,
            "lomax": -45.608226430405270
         },
         "dxb": {
            "name": "Dubai International Airport",
            "la": 25.2532,
            "lo": 55.3657,

            "lamin": 24.814729101111364,
            "lomin": 54.495487090990856,
            "lamax": 25.697803450553323,
            "lomax": 56.234182405813440
         },
         "sin": {
            "name": "Singapore Changi Airport",
            "la":   1.3644,
            "lo": 103.9915,

            "lamin":   0.89011766376433,
            "lomin": 103.14604164334601,
            "lamax":   1.83846589142574,
            "lomax": 104.83523965436733
         },
         "mnl": {
            "name": "Manila Ninoy Aquino International Airport",
            "la":  14.5123,
            "lo": 121.0165,

            "lamin":  14.02005011701964,
            "lomin": 120.10897046514074,
            "lamax":  15.00966670474826,
            "lomax": 121.93265078177481
         },
         "icn": {
            "name": "Seoul Incheon International Airport",
            "la":  37.4602,
            "lo": 126.4407,

            "lamin":  37.07444970060118,
            "lomin": 125.57972530851085,
            "lamax":  37.84169473588783,
            "lomax": 127.29936953377349
         },
         "nrt": {
            "name": "Tokyo Narita International Airport",
            "la":  35.7720,
            "lo": 140.3929,

            "lamin":  35.38268010597130,
            "lomin": 139.52972478353882,
            "lamax":  36.16686190560277,
            "lomax": 141.25273086531777
         },
         "syd": {
            "name": "Sydney Kingsford Smith Airport",
            "la": - 33.9500,
            "lo":  151.1819,

            "lamin": - 34.35338290433131,
            "lomin":  150.31734742800330,
            "lamax": - 33.55022852062867,
            "lomax":   152.0369915466958
         },
         "akl": {
            "name": "Auckland Airport",
            "la": - 37.0082,
            "lo":  174.7850,

            "lamin": - 37.39099149035015,
            "lomin":  173.91856839184885,
            "lamax": - 36.62047189659440,
            "lomax":  175.63989338541032
         }
      }

      area_data = airport_data[area]


      # defer the reply
      await ctx.defer()


      # get nearby aircraft info in the specified area's coordinates
      r = requests.get(
         f"https://opensky-network.org/api/states/all?lomin={area_data['lomin']}&lamin={area_data['lamin']}&lomax={area_data['lomax']}&lamax={area_data['lamax']}", # https://openskynetwork.github.io/opensky-api/rest.html#all-state-vectors
         headers = {
            "Accept": "application/json",
            "User-Agent": f"discord-aviflight558-bot/{config['version']} ({os.getenv('AGENT')}) (https://github.com/magicalbunny31/aviflight558)"
         }
      )


      # response isn't okai
      if not r.ok:
         developer = await self.bot.fetch_user(config["developer"])
         return await ctx.interaction.edit_original_message(
            content = strip_indents(f"""
               **`Error: "something bad happened with the data, try again later" 💥`**
               > **problem persists? contact `{developer.name}#{developer.discriminator}`**
            """)
         )


      # get response object
      res = r.json()


      # nearby aircraft data
      aircraft = (res["states"] or [])

      aircraft_rows = sorted(
         list(
            map(
               lambda aircraft: [
                  aircraft[1].strip() or "---",
                  f"{calculate_distance(aircraft[5], aircraft[6], area_data['lo'], area_data['la'])}km" if aircraft[5] and aircraft[6] else "---"
               ],
               aircraft
            )
         ),
         key=lambda a: float(a[1][0:-2]) if a[1] != "---" else a[1]
      )


      # image data
      centre = f"{area_data['la']},{area_data['lo']}"
      zoom = "9"
      size = "640x360"
      scale = "2"
      format = "png"
      maptype = "satellite"
      markers = [
         f"anchor:center|icon:{triangle_flag_marker}|{area_data['la']},{area_data['lo']}",
         *list(map(lambda aircraft: f"anchor:center|icon:{airplane_marker}|{aircraft[6]},{aircraft[5]}", aircraft))
      ]
      key = os.getenv("GOOGLE_STATIC_MAPS_API")

      r = requests.get(
         f"https://maps.googleapis.com/maps/api/staticmap?center={centre}&zoom={zoom}&size={size}&scale={scale}&format={format}&maptype={maptype}&markers={'&markers='.join(markers)}&key={key}",
         headers = {
            "User-Agent": f"discord-aviflight558-bot/{config['version']} ({os.getenv('AGENT')}) (https://github.com/magicalbunny31/aviflight558)"
         }
      )
      

      image = BytesIO(r.content)
      file = discord.File(image, filename=f"{area}.png")


      # embed
      embed = discord.Embed(
         colour = discord.Colour.from_rgb(67, 196, 205), # #43c4cd
         title = f"{area_data['name']} {airplane}",
         description = strip_indents(f"""
            ```
            {
               tabulate(
                  aircraft_rows,
                  headers = ["CALLSIGN", f"DISTANCE FROM {area.upper()}"],
                  tablefmt = "simple",
                  disable_numparse = True
               )
               if aircraft_rows else
               "no nearby aircraft.."
            }
            ```
            **`last updated`** : <t:{res["time"]}>
         """)
      ) \
         .set_image(url=f"attachment://{area}.png")


      return await ctx.respond(
         embeds = [embed],
         files = [file]
      )



def setup(bot):
   bot.add_cog(nearby(bot))