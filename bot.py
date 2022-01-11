#########################################
#                                       #
#   code by magicalbunny31              #
#   https://github.com/magicalbunny31   #
#                                       #
#########################################


import discord, os

from dotenv import load_dotenv
load_dotenv()

# bot
bot = discord.Bot(
   activity = discord.Activity(
      name = "planes ✈️",
      type = discord.ActivityType.watching
   ),
   status = discord.Status.idle,
   intents = discord.Intents(
      guilds = True
   ),
   # debug_guilds = [516701797411323915]
)


# bot is ready
@bot.event
async def on_ready():
   print("🦊")


# load cogs
for file in os.listdir("./cogs"):
   if not file.endswith(".py"): continue
   if not bot.debug_guilds and file == "uwu.py": continue # if this isn't in debug, don't use the test command

   bot.load_extension(f"cogs.{file[0:-3]}")


# run the bot
token = os.getenv("TOKEN")
bot.run(token)