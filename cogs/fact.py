import discord
from discord.ext import commands
from random import choice

from assets.data.strip_indents import strip_indents


class fact(commands.Cog):
   def __init__(self, bot):
      self.bot = bot


   @commands.slash_command(name="fact", description="get a random aviation fact 💬")
   async def command(self, ctx):
      facts = [
         ["pilots eat a different meal", "this is to mitigate the risk of all pilots getting food poisoning", "https://ctipft.com/interesting-facts-about-aviation"],
         ["the 747 has six million parts", "that's a lot of parts!", "https://ctipft.com/interesting-facts-about-aviation"],
         ["80% of the population has a fear of flying", "this is called aerophobia; they may also fear heights too", "https://ctipft.com/interesting-facts-about-aviation"],
         ["only 5% of the population have flown on a plane", "this percentage is skewed because of people from poorer regions aren't able to afford flying", "https://ctipft.com/interesting-facts-about-aviation"],
         ["your taste changes", "the pressure in the airline cabin changes your ability to taste", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["in 1987, American Airlines saved US $40,000 annually..", "..by removing one olive from their first class salads", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["the aircraft cabin lights are dimmed not to give you a better night's sleep..", "..but to make passengers' eyes adjust to the darkness, making emergency exits clearer in case of evacuation", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["tap water on an aircraft is bad", "the bacteria levels in them are up to x100 the amount allowed bacteria in the USA", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["the first airline to introduce online check-in..", "..was Alaska Airlines", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["the highest price ever paid for a flight ticket was US $123,000", "bought by an Australian millionaire for flight SQ380 (SIN-SYD) for the A380's maiden flight", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["a man is more likely to cry on a flight", "the chances from crying from a movie are 15% higher than on ground", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["the safest section on a plane is the back third", "the fatality rate is \\*only\\* 32%, whereas the other sections are ~38%", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["there is 225km of cable in a 747", "the 747 is beautiful", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["the first transatlantic flight took place in 1919", "it was operated by the US NAVY; it only took 24 days!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["Qantas was the first airline to introduce business class", "this was in 1979!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["Jeju to Seoul (CJU-GMP) is the busiest air route by number of passengers", "the distance between them is only 449km, yet carries 14 million passengers in 2018 alone!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["aircraft tray tables are disgusting", "the bacteria levels found on them were three times as high as the levels on the toilet flush button", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["food was first served on a plane in 1919", "this happened on a London to Paris trip, it costed three shillings", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["pilots are not allowed to have beards", "at most airlines anyway; this is because it could cause problems when donning the oxygen mask", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["chicken guns", "to simulate bird strikes, a \"chicken gun\" is used to shoot dead chickens into an engine", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["death by plane?", "the chances of that is very low: 0.000024%!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["Air Force One has a maximum capacity of 96 people", "despite it being able to carry over 300 pax", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["with the 747, 78 billion km have been logged on all of its flights", "that's enough to go to the moon and back 100,000 times!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["in 2019, there was 1.7 million lost luggage!", "this includes mishandled luggage that were delivered late, too", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["the Bermuda Triangle myth is a fallacy!", "airlines no longer avoid the area", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["on a three-hour flight..", "..the average human body loses 1.5 litres of water", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["80% of all plane crashes..", "..happen during take-off and landing", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["in 1947..", "..a plane broke the sound barrier for the first time", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["the amount of fuel that a 747 can use..", "..could fuel 1,400 minivans!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["in a survey..", "67% of pilots have admitted that they've fallen asleep while flying at least once", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["the A380's wingspan is longer than its body", "it's about 8 metres longer", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["there's only one transportation mode that's safer than travelling by aircraft..", "..and that's the elevator!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["Singapore Airlines serves 20,000 bottles of alcohol every month..", "..and that's just from their first-class!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["in 1986..", "..the first non-stop flight around the world took place!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["the first person to serve as a flight attendant was back in 1912", "it was a German man, who served on the Zeppelin \"Schwaben\"", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["the 747 burns 3.7 litres of fuel per second", "doesn't sound very fuel-efficient, huh?", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["the airline that serves the most airlines is..", "..Turkish Airlines!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["on average, 10% of an aircraft's bulk weight is..", "..the passenger payload!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["black boxes aren't black", "they're actually painted with a special, bright-orange colour!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["what if someone dies while in flight?", "there's no standard procedure when this happens: some airlines have special locations to store dead bodies, while others move the body to the last seat row", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["Signapore Airlines spends US $60 million..", "..annually for wine!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["before New York John F. Kennedy Airport (JFK) was named that..", "..it was previously named Idlewild Airport!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["the longest duration a twin-engine aircraft is allowed to fly with only one engine..", "..is 5½ hours!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["the world's safest airline is..", "..Qantas!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["the height of some winglets is larger than most people", "they're usually 2.4 metres tall!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["the humidity in an aircraft is about 20%", "that's drier than the driest place on earth - Death Valley - with an average humidity of about 50%!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["today's aircraft are over 70% more fuel-efficient per seat kilometre than planes in the 1960s", "what a feat!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["on Concorde, flying from London to New York took just under three hours", "with today's fastest aircraft, that could take just over five hours!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["Flybondi was 2021's most unpunctual airline", "so much that 0% of their flights arrived on time!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["Osaka International Airport (ITM) was 2021's most punctual airport", "98.5% of its flights depart on time!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["the most successful airline on Facebook..", "..is Quatar Airways, with 22.5 million followers!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["Hainan Airlines was the world's most valuable airline in May 2021", "they had a market cap of US $34.8 billion! however, this only lasted for a couple of days..", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["the most successful airline on Twitter..", "..is Garuda Indonesia, with 3.4 million followers!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["despite COVID-19, four passenger airlines were still profitable in 2020", "they were: China Airlines, Korean Air, Ethiopian Airlines and Bamboo Airways", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"],
         ["the most successful airline on Instagram..", "..is Emirates, with 5.6 million followers!", "https://www.id1.de/2021/07/05/the-ultimate-source-for-crazy-aviation-facts"]
      ]
      fact = choice(facts)

      [main, secondary, sauce] = fact

      yellow_book = "<:yellow_book:809123390438768660>"
      view = discord.ui.View(
         discord.ui.Button(
            style = discord.ButtonStyle.link,
            label = "source",
            url = sauce,
            emoji = discord.PartialEmoji.from_str(yellow_book)
         )
      )

      fact_number = [i[0] for i in facts].index(main) + 1

      return await ctx.respond(
         content = strip_indents(f"""
            **{main}**
            {secondary}
            > `fact #{fact_number}/{len(facts)}`
         """),
         view = view
      )


def setup(bot):
   bot.add_cog(fact(bot))