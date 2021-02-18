import discord
import os
import aiohttp
import json
from discord.ext import commands
import logging
import random
from replit import db
from keep_alive import keep_alive

logging.basicConfig(level=logging.INFO)

client = commands.Bot(command_prefix='$')

copypasta = """And now
AsapSCIENCE presents-
100 digits of π
3.14159, this is π
Followed by 2-6-5-3-5-8-9
Circumference over diameter
7-9, then 3-2-3
OMG! Can't you see?
8-4-6-2-6-4-3
And now we're on a spree
38 and 32, now we're blue
Oh, who knew?
7, 950 and then a two
88 and 41, so much fun
Now a run
9-7-1-6-9-3-9-9
Then 3-7, 51
Half way done!
0-5-8, now don't be late
2-0-9, where's the wine?
7-4, it's on the floor
Then 9-4-4-5-9
2-3-0, we gotta go
7-8, we can't wait
1-6-4-0-6-2-8
We're almost near the end, keep going
62, we're getting through
0-8-9-9, on time
8-6-2-8-0-3-4
There's only a few more!
8-2, then 5-3
42, 11, 7-0 and 67
We're done! Was that fun?
Learning random digits
So that you can brag to your friends"""

# From VIDEO CODE THINGIE:
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person!"
]

if "responding" not in db.keys():
  db["responding"] = True

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements


# ^ VIDEO CODE THINGIE, need to change to commands

async def get_quote():
  async with aiohttp.ClientSession() as session:
    async with session.get('https://zenquotes.io/api/random') as resp:
      json_data = json.loads(await resp.text())
      quote = json_data[0]['q'] + " - " + json_data[0]['a']
      return(quote)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if db["responding"] == True:
    replies = {'stupid':'no u','π':copypasta,'omg':'OMG!','lol':'LOL!','wow':'Wow okay..!','haha':'HAHAHA!', 'f':'Everyone press "F" to pay your respect!'}
    found_replies = [x for x in replies.keys() if x in message.content.lower().split(" ")]
    if message.author == client.user:
      return
  # VIDEO CODE THINGIE:

  msg = message.content

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.reply(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.reply("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.reply(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.reply(encouragements)

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.reply("Responding is on.")
    else:
      db["responding"] = False
      await message.reply("Responding is off.")


  # ^ VIDEO CODE THINGIE
  elif len(found_replies) >= 1:
    for found_reply in found_replies:
      await message.reply(replies[found_reply])

  await client.process_commands(message)

@client.command() 
async def inspire(ctx):
  quote = await get_quote()
  print(f'quote is {quote}')
  await ctx.reply(quote)

@client.command()
async def hi(ctx):
  await ctx.reply('Hello!')

@client.command()
async def bye(ctx):
  await ctx.reply('Bye!')

keep_alive()
client.run(os.getenv('TOKEN'))