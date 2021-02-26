import os
import aiohttp
import json
import discord
from discord.ext import commands, tasks
import logging
import random
from replit import db
from keep_alive import keep_alive
import asyncio
from itertools import cycle

logging.basicConfig(level=logging.INFO)

client = commands.Bot(command_prefix='/')
client.remove_command('help')
status = cycle(['/help', 'your messages', '/help', 'Never Gonna Give You Up'])

sad_words = [
    "sad", "depressed", "unhappy", "angry", "miserable", "depressing",
    "bitter", "dismal", "heartbroken", "melancholy", "mournful", "pessimistic",
    "somber", "sorrowful", "sorry", "wistful", "bereaved", "blue", "cheerless",
    "dejected", "despairing", "despondent", "disconsolate", "distressed",
    "doleful", "down in dumps", "down in mouth", "downcast", "forlorn",
    "gloomy", "glum", "grief-stricken", "grieved", "heartsick", "heavyhearted",
    "hurting", "in doldrums", "in grief", "in the dumps", "languishing",
    "low-spirited", "lugubrious", "morbid", "morose", "out of sorts",
    "pensive", "sick at heart", "troubled", "weeping", "woebegone"
]

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
    change_status.start()
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply(
            'Command was not found. Be sure you did not make a typo and try again.'
        )


@client.event
async def on_message(message):

    msg = message.content

    if db["responding"] == True:
        options = starter_encouragements
        if "encouragements" in db.keys():
            options = options + db["encouragements"]

        if any(word in msg for word in sad_words):
            if "!" not in msg and "/" not in msg and "not" not in msg and "n't" not in msg and "aint" not in msg and "never" not in msg:
                await message.reply(random.choice(options))

    await client.process_commands(message)


@client.event
async def on_member_join(member):
    print(f'{member} has joined a server!')


@client.event
async def on_member_remove(member):
    print(f'{member} has left a server.')


@client.command()
async def inspire(ctx):
    quote = await get_quote()
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


@responding.error
async def responding_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(
            'Please specify whether you want responding to be on or off.')


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
async def new(ctx, *, arg):
    encouraging_message = arg
    update_encouragements(encouraging_message)
    await ctx.reply(f'New encouraging message added: {encouraging_message}')


@client.command(aliases=['purge'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Removed {amount} messages.")
    await asyncio.sleep(3)
    await ctx.channel.purge(limit=1)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply("You do not have the manage messages permission.")
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=1)


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.reply(f"Kicked {member} because {reason}.")


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.reply(f"Banned {member.mention} because {reason}.")


@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name,
                                               member_discriminator):
            await ctx.guild.unban(user)
            person = f"{user.name}#{user.discriminator}"
            await ctx.reply(f"Unbanned {person}.")
            return


@client.command()
async def hello(ctx, *, arg):
    if arg.lower() == "there":
        await ctx.reply("General Kenobi!")
    else:
        textx = arg.lower()
        texty = textx.capitalize()
        await ctx.channel.send(f"Hello {texty}!")
        await ctx.message.delete()


@client.command()
async def say(ctx, *, arg):
    text = arg
    await ctx.channel.send(text)
    await ctx.message.delete()


@client.command()
async def ping(ctx):
    await ctx.reply(f'Pong! {round(client.latency * 1000)}ms')


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = [
        "It is certain.", "It is decidedly so.", "Without a doubt.",
        "Yes - definitely.", "You may rely on it.", "As I see it, yes.",
        "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
        "Reply hazy, try again.", "Ask again later.",
        "Better not tell you now.", "Cannot predict now.",
        "Concentrate and ask again.", "Don't count on it.", "My reply is no.",
        "My sources say no.", "Outlook not so good.", "Very doubtful."
    ]
    await ctx.reply(f'{random.choice(responses)}')


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=next(status)))


@client.command(aliases=['credit'])
async def credits(ctx):
    embed = discord.Embed(colour=discord.Colour.orange())
    embed.set_author(name='Credits')
    embed.add_field(name='Created by Toricane#6391',
                    value='"Thank you for using my bot!" - Toricane',
                    inline=False)
    embed.add_field(name='Hosted by Repl.it',
                    value='https://repl.it/@Toricane/Perseverance-Bot#main.py',
                    inline=False)
    embed.add_field(name='Saved in GitHub',
                    value='https://github.com/Toricane/Perseverance-Bot/',
                    inline=False)
    embed.add_field(
        name='Tutorials Used:',
        value=
        'https://youtu.be/SPTfmiYiuok\nhttps://youtube.com/playlist?list=PLW3GfRiBCHOhfVoiDZpSz8SM_HybXRPzZ',
        inline=False)
    await ctx.send(embed=embed)


@client.command(pass_context=True)
async def help(ctx, *, arg=None):
    embed = discord.Embed(colour=discord.Colour.orange())
    arg = str(arg).lower()
    if arg == "ping":
        embed.set_author(name='Help for /ping')
        embed.add_field(name='/ping', value='Returns "Pong!"', inline=False)
        await ctx.send(embed=embed)

    elif arg == "inspire":
        embed.add_field(name='/inspire',
                        value='Send a random quote from https://zenquotes.io/',
                        inline=False)
        await ctx.send(embed=embed)

    elif arg == "hi":
        embed.add_field(name='/hi', value='Returns "Hello!"', inline=False)
        await ctx.send(embed=embed)

    elif arg == "bye":
        embed.add_field(name='/bye', value='Returns "Bye!"', inline=False)
        await ctx.send(embed=embed)

    else:
        embed.set_author(name='Help')
        embed.add_field(name='/help', value='Shows this message', inline=False)
        embed.add_field(name='/credit or /credits',
                        value='Shows the credits.',
                        inline=False)
        embed.add_field(name='/ping', value='Returns "Pong!"', inline=False)
        embed.add_field(name='/inspire',
                        value='Send a random quote from https://zenquotes.io/',
                        inline=False)
        embed.add_field(name='/hi', value='Returns "Hello!"', inline=False)
        embed.add_field(name='/bye', value='Returns "Bye!"', inline=False)
        embed.add_field(
            name='/responding on/off',
            value=
            'Toggles between replying to certain words or phrases automatically.',
            inline=False)
        embed.add_field(name='/new "text"',
                        value='Adds more encouraging messages.',
                        inline=False)
        embed.add_field(
            name='/list',
            value=
            'Only lists the encouragements that have been added from /new.',
            inline=False)
        embed.add_field(
            name='/delete number',
            value=
            'Deletes the corresponding encouraging message listed in /list.',
            inline=False)
        embed.add_field(name='/hello there',
                        value='Returns "General Kenobi!"',
                        inline=False)
        embed.add_field(name='/say "text"',
                        value='Says your text.',
                        inline=False)
        embed.add_field(name='/hello name',
                        value='Returns "Hello Name!"',
                        inline=False)
        embed.add_field(
            name='/8ball question',
            value=
            'Returns whether or not your question\'s answer is yes or no.',
            inline=False)
        embed.add_field(
            name='/kick',
            value='Kicks a member. NOTE: requires Kick Members permission.',
            inline=False)
        embed.add_field(
            name='/ban',
            value='Bans a member. NOTE: requires Ban Members permission.',
            inline=False)
        embed.add_field(
            name='/unban',
            value='Unbans a member. NOTE: requires Ban Members permission.',
            inline=False)
        embed.add_field(name='/clear or /purge number',
                        value='Deletes the number of messages. Default is 5.',
                        inline=False)
        embed.add_field(name='/perseverance',
                        value='Shows a picture of Perseverance.',
                        inline=False)

        await ctx.send(embed=embed)


@client.command()
async def perseverance(ctx):
    await ctx.reply(file=discord.File('perseverance.jpeg'))


keep_alive()
client.run(os.getenv('TOKEN'))
