import os
import aiohttp
import json
import discord
from discord.ext import commands
import logging
import random
from replit import db
from keep_alive import keep_alive

logging.basicConfig(level=logging.INFO)

client = commands.Bot(command_prefix='$')
client.remove_command('help')

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

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
    "Cheer up!", "Hang in there.", "You are a great person!"
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


async def get_quote():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://zenquotes.io/api/random') as resp:
            json_data = json.loads(await resp.text())
            quote = '"' + json_data[0]['q'] + '" - ' + json_data[0]['a']
            return (quote)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

    msg = message.content

    if db["responding"] == True:
        options = starter_encouragements
        if "encouragements" in db.keys():
            options = options + db["encouragements"]

        if any(word in msg for word in sad_words):
            if "$" not in msg:
                await message.reply(random.choice(options))

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


@client.command()
async def responding(ctx, arg):

    if arg.lower() == "true" or arg.lower() == "on":
        db["responding"] = True
    else:
        db["responding"] = False

    if db["responding"] == True or db["responding"]:
        await ctx.reply("Responding is on.")
    else:
        await ctx.reply("Responding is off.")


@client.command()
async def list(ctx):
    encouragements = []
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
    await ctx.reply(encouragements)


@client.command()
async def delete(ctx, arg):
    encouragements = []
    if "encouragements" in db.keys():
        index = int(arg) - 1
        delete_encouragment(index)
        encouragements = db["encouragements"]
    await ctx.reply(encouragements)


@client.command()
async def new(ctx, arg):
    if "-" in arg:
        encouraging_message = arg.replace('"', '')
        update_encouragements(encouraging_message)
        await ctx.reply(f'New encouraging message added: {encouraging_message}'
                        )
    else:
        await ctx.reply(
            'Please try again, and put your text inside of quotation marks (").\n\nExample: $new "Hello World!"'
        )


@client.command()
async def hello(ctx, arg):
    if arg.lower() == "there":
        await ctx.reply("General Kenobi!")


@client.command()
async def repeat(ctx, arg):
    text = arg.replace('"', '')
    await ctx.channel.send(text)
    await ctx.message.delete()


@client.command()
async def ping(ctx):
    await ctx.reply('Pong!')


@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(colour=discord.Colour.orange())

    embed.set_author(name='Help')
    embed.add_field(name='$help', value='Shows this message', inline=False)
    embed.add_field(name='$ping', value='Returns "Pong!"', inline=False)
    embed.add_field(name='$inspire',
                    value='Send a random quote from https://zenquotes.io/',
                    inline=False)
    embed.add_field(name='$hi', value='Returns "Hello!"', inline=False)
    embed.add_field(name='$bye', value='Returns "Bye!"', inline=False)
    embed.add_field(
        name='$responding on/off',
        value=
        'Toggles between replying to certain words or phrases automatically.',
        inline=False)
    embed.add_field(name='$new "text"',
                    value='Adds more encouraging messages.',
                    inline=False)
    embed.add_field(
        name='$list',
        value='Only lists the encouragements that have been added from $new.',
        inline=False)
    embed.add_field(
        name='$delete number',
        value='Deletes the corresponding encouraging message listed in $list.',
        inline=False)
    embed.add_field(name='$hello there',
                    value='Returns "General Kenobi!"',
                    inline=False)
    embed.add_field(name='$repeat "text"',
                    value='Repeats your text.',
                    inline=False)

    await ctx.send(embed=embed)


keep_alive()
client.run(os.getenv('TOKEN'))
