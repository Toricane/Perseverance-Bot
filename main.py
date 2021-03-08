import subprocess

list_files = subprocess.run(["pip", "install", "pynacl"])

list_files = subprocess.run(
    ["pip", "install", "-U", "discord-py-slash-command"])

list_files = subprocess.run(["pip", "install", "googlesearch-python"])

list_files = subprocess.run(["pip", "install", "lxml"])

list_files = subprocess.run(["pip", "install", "metadata-parser"])

list_files = subprocess.run(["pip", "install", "wikipedia"])

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
from discord_slash import SlashCommand
from discord_slash.utils import manage_commands
import sys
import datetime
import wikipedia
import pyjokes
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse


def googleSearch(query):
    g_clean = []
    if "http" not in query:
        url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(query)
    else:
        url = query
    try:
        html = requests.get(url)
        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'lxml')
            a = soup.find_all('a')
            for i in a:
                k = i.get('href')
                try:
                    m = re.search("(?P<url>https?://[^\s]+)", k)
                    n = m.group(0)
                    rul = n.split('&')[0]
                    domain = urlparse(rul)
                    if (re.search('google.com', domain.netloc)):
                        continue
                    else:
                        g_clean.append(rul)
                except:
                    continue
    except Exception as ex:
        print(str(ex))
    finally:
        del g_clean[10:100]
        return g_clean


logging.basicConfig(level=logging.INFO)

client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)
status = cycle([
    '/help help', 'your messages', '/help help', 'Never Gonna Give You Up', '/help help',
    'try /setup if the slash commands are not working'
])

#db["id"] = [788578597488427008, 764683397528158259]
guild_ids = db["id"]

sad_words = [
    "sad", "depressed", "unhappy", "angry", "miserable", "depressing",
    "bitter", "dismal", "heartbroken", "melancholy", "mournful", "pessimistic",
    "somber", "sorrowful", "sorry", "wistful", "bereaved", "cheerless",
    "dejected", "despairing", "despondent", "disconsolate", "distressed",
    "doleful", "down in dumps", "down in mouth", "downcast", "forlorn",
    "gloomy", "glum", "grief-stricken", "grieved", "heartsick", "heavyhearted",
    "hurting", "in doldrums", "in grief", "in the dumps", "languishing",
    "low-spirited", "lugubrious", "morbid", "morose", "out of sorts",
    "pensive", "sick at heart", "troubled", "weeping", "woebegone"
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
    timestamp = datetime.datetime.now()
    print(timestamp.strftime(r"%A, %b %d, %Y, %I:%M %p UTC"))


@client.event
async def on_message(message):

    msg = message.content

    if db["responding"] == True:
        if "encouragements" in db.keys():
            options = db["encouragements"]

        if any(word in msg for word in sad_words):
            if "!" not in msg and "." not in msg and "not" not in msg and "n't" not in msg and "aint" not in msg and "never" not in msg:
                await message.reply(random.choice(options))

    if msg == "/setup":
        print('/setup')
        ido = message.guild.id
        if ido not in db["id"]:
            ids = db["id"]
            ids.append(ido)
            db["id"] = ids
            print(db["id"])
            await message.reply(
                "Server has been set up! The bot is restarting! If the error persists, contact Toricane#6391 in Discord to restart the bot!"
            )
            slash = SlashCommand(client, sync_commands=True)
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            await message.reply(
                "Server already setup! The bot is restarting! If the error persists, contact Toricane#6391 in Discord to restart the bot!"
            )
            slash = SlashCommand(client, sync_commands=True)
            os.execl(sys.executable, sys.executable, *sys.argv)


@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(
                'Thank you for inviting me! Try /setup if the commands still don\'t work after 5 minutes.'
            )
            ido = int(guild.id)
            ids = db["id"]
            ids.append(ido)
            db["id"] = ids
            print(db["id"])
            slash = SlashCommand(client, sync_commands=True)
        break
    os.execl(sys.executable, sys.executable, *sys.argv)


@client.event
async def on_guild_remove(guild):
    ido = int(guild.id)
    ids = db["id"]
    ids.remove(ido)
    db["id"] = ids
    print(db["id"])
    slash = SlashCommand(client, sync_commands=True)
    os.execl(sys.executable, sys.executable, *sys.argv)


@client.event
async def on_member_join(member):
    print(f'{member} has joined a server!')


@client.event
async def on_member_remove(member):
    print(f'{member} has left a server.')


@slash.slash(name="inspire",
             description="The bot will send a random inspirational quote",
             guild_ids=guild_ids)
async def _inspire(ctx):
    print(f"{ctx.author.name}: /inspire")
    quote = await get_quote()
    await ctx.respond()
    await ctx.send(quote)


@slash.slash(name="hi",
             description="The bot will say hello to you",
             guild_ids=guild_ids)
async def _hi(ctx):
    print("/hi")
    await ctx.respond()
    await ctx.send('Hello!')


@slash.slash(name="bye",
             description="The bot will say bye to you",
             guild_ids=guild_ids)
async def _bye(ctx):
    print("/bye")
    await ctx.respond()
    await ctx.send('Bye!')


@slash.slash(name="list",
             description="Lists the encouraging messages",
             guild_ids=guild_ids)
async def _list(ctx):
    print("/list")
    encouragements = []
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
    await ctx.respond()
    await ctx.send(f'{encouragements}')


@slash.slash(
    name="delete",
    description="Deletes an encouraging message, /list to see",
    options=[
        manage_commands.create_option(
            name="index",
            description=
            "The encouraging message's position in the list that you want to delete, try /list to see",
            option_type=3,
            required=True)
    ],
    guild_ids=guild_ids)
async def _delete(ctx, argone):
    encouragements = []
    if "encouragements" in db.keys():
        index = int(argone) - 1
        print(f"/delete {index}")
        delete_encouragment(index)
        encouragements = db["encouragements"]
    await ctx.respond()
    await ctx.send(encouragements)


@slash.slash(name="new",
             description="Add a new encouraging message",
             options=[
                 manage_commands.create_option(name="message",
                                               description="Add it here",
                                               option_type=3,
                                               required=True)
             ],
             guild_ids=guild_ids)
async def _new(ctx, argone):
    print(f"/new {argone}")
    encouraging_message = argone
    update_encouragements(encouraging_message)
    await ctx.respond()
    await ctx.send(f'New encouraging message added: {encouraging_message}')


@slash.slash(name="clear", description="Delete messages", guild_ids=guild_ids)
@commands.has_permissions(manage_messages=True)
async def _clear(ctx, amount=5):
    print(f"/clear {amount}")
    amount = int(amount)
    await ctx.channel.purge(limit=amount + 1)
    await ctx.respond()
    await ctx.send(f"Removed {amount} messages.")
    await asyncio.sleep(3)
    await ctx.channel.purge(limit=2)


@slash.slash(name="kick", description="Kicks a member", guild_ids=guild_ids)
@commands.has_permissions(kick_members=True)
async def _kick(ctx, member: discord.Member, *, reason=None):
    print(f"/kick {member} {reason}")
    await member.kick(reason=reason)
    await ctx.respond()
    await ctx.send(f"Kicked {member} because {reason}.")


@slash.slash(
    name="wikipedia",
    description="Searches for something on Wikipedia",
    options=[
        manage_commands.create_option(
            name="text",
            description="What do you want to search?",
            option_type=3,
            required=True),
        manage_commands.create_option(
            name="results",
            description=
            "How many results should you randomly recieve 1 result from? Default is 5.",
            option_type=3,
            required=False),
        manage_commands.create_option(
            name="lines",
            description="How many lines do you want? Default is 10.",
            option_type=3,
            required=False)
    ],
    guild_ids=guild_ids)
async def _wikipedia(ctx, text, results=1, lines=5):
    print(f"/wikipedia {text} {lines}")
    result = wikipedia.search(text, results)
    try:
        end = random.choice(result)
        info = wikipedia.summary(end, int(lines))
        if len(info) <= 2000:
            await ctx.respond()
            await ctx.send(f"{info}")
        else:
            await ctx.respond()
            await ctx.send("The message is too long, please use less lines.")
    except IndexError:
        await ctx.respond()
        await ctx.send("No results found.")
    except discord.errors.NotFound:
        await ctx.respond()
        await ctx.send("Please try again.")



@slash.slash(name="joke", description="Gives you a joke", guild_ids=guild_ids)
async def _joke(ctx):
    await ctx.respond()
    await ctx.send(f"{pyjokes.get_joke()}")


@slash.slash(name="google",
             description="Search anything on Google!",
             options=[
                 manage_commands.create_option(name="text",
                                               description="Search it here",
                                               option_type=3,
                                               required=True),
                 manage_commands.create_option(name="results",
                                               description="How many results? Max is 10 and default is 5",
                                               option_type=3,
                                               required=False)
             ],
             guild_ids=guild_ids)
async def _google(ctx, text, results=5):
    result = googleSearch(text)
    hello = True
    try:
        a,b,c,d,e,f,g,h,i,j = result
    except:
        a,b,c,d,e,f,g,h,i = result
        hello = False
    if results == 1:
        await ctx.respond()
        await ctx.send(f"{a}")
    elif results == 2:
        await ctx.respond()
        await ctx.send(f"{a}")
        await ctx.send(f"{b}")
    elif results == 3:
        await ctx.respond()
        await ctx.send(f"{a}")
        await ctx.send(f"{b}")
        await ctx.send(f"{c}")
    elif results == 4:
        await ctx.respond()
        await ctx.send(f"{a}")
        await ctx.send(f"{b}")
        await ctx.send(f"{c}")
        await ctx.send(f"{d}")
    elif results == 5:
        await ctx.respond()
        await ctx.send(f"{a}")
        await ctx.send(f"{b}")
        await ctx.send(f"{c}")
        await ctx.send(f"{d}")
        await ctx.send(f"{e}")
    elif results == 6:
        await ctx.respond()
        await ctx.send(f"{a}")
        await ctx.send(f"{b}")
        await ctx.send(f"{c}")
        await ctx.send(f"{d}")
        await ctx.send(f"{e}")
        await ctx.send(f"{f}")
    elif results == 7:
        await ctx.respond()
        await ctx.send(f"{a}")
        await ctx.send(f"{b}")
        await ctx.send(f"{c}")
        await ctx.send(f"{d}")
        await ctx.send(f"{e}")
        await ctx.send(f"{f}")
        await ctx.send(f"{g}")
    elif results == 8:
        await ctx.respond()
        await ctx.send(f"{a}")
        await ctx.send(f"{b}")
        await ctx.send(f"{c}")
        await ctx.send(f"{d}")
        await ctx.send(f"{e}")
        await ctx.send(f"{f}")
        await ctx.send(f"{g}")
        await ctx.send(f"{h}")
    elif results == 9:
        await ctx.respond()
        await ctx.send(f"{a}")
        await ctx.send(f"{b}")
        await ctx.send(f"{c}")
        await ctx.send(f"{d}")
        await ctx.send(f"{e}")
        await ctx.send(f"{f}")
        await ctx.send(f"{g}")
        await ctx.send(f"{h}")
        await ctx.send(f"{i}")
    elif results == 10 and hello == True:
        await ctx.respond()
        await ctx.send(f"{a}")
        await ctx.send(f"{b}")
        await ctx.send(f"{c}")
        await ctx.send(f"{d}")
        await ctx.send(f"{e}")
        await ctx.send(f"{f}")
        await ctx.send(f"{g}")
        await ctx.send(f"{h}")
        await ctx.send(f"{i}")
        await ctx.send(f"{j}")
    else:
        await ctx.respond()
        await ctx.send("ERROR")
        await ctx.send("Make sure the results parameter is between 1 and 10 inclusive.")
        await ctx.send("This could also mean that Google does not have enough results available. Make sure you made no typos.")


@slash.slash(name="ban", description="Bans a member", guild_ids=guild_ids)
@commands.has_permissions(ban_members=True)
async def _ban(ctx, member: discord.Member, *, reason=None):
    print(f"/ban {member} {reason}")
    await member.ban(reason=reason)
    await ctx.respond()
    await ctx.send(f"Banned {member.mention} because {reason}.")


@slash.slash(name="unban",
             description="Unbans a member",
             options=[
                 manage_commands.create_option(
                     name="member",
                     description="Add the member name here",
                     option_type=3,
                     required=True)
             ],
             guild_ids=guild_ids)
@commands.has_permissions(ban_members=True)
async def _unban(ctx, argone):
    print(f"/unban {argone}")
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = argone.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name,
                                               member_discriminator):
            await ctx.guild.unban(user)
            person = f"{user.name}#{user.discriminator}"
            await ctx.respond()
            await ctx.send(f"Unbanned {person}.")
            return


@slash.slash(name="hello",
             description="Say hello to someone",
             options=[
                 manage_commands.create_option(
                     name="name",
                     description='Put either "there" or the name',
                     option_type=3,
                     required=True)
             ],
             guild_ids=guild_ids)
async def _hello(ctx, argone):
    print(f"/hello {argone}")
    if argone.lower() == "there":
        await ctx.send("General Kenobi!")
    else:
        textx = argone.lower()
        texty = textx.capitalize()
        await ctx.respond()
        await ctx.channel.send(f"Hello {texty}!")
        await ctx.message.delete()


@slash.slash(name="say",
             description="Make the bot say anything",
             options=[
                 manage_commands.create_option(name="message",
                                               description="Say your message",
                                               option_type=3,
                                               required=True)
             ],
             guild_ids=guild_ids)
async def _say(ctx, argone):
    print(f"/say {argone}")
    text = argone
    await ctx.respond()
    await ctx.channel.send(text)
    await ctx.message.delete()


@slash.slash(name="ping",
             description="This returns the bot latency",
             options=[
                 manage_commands.create_option(
                     name="message",
                     description="This returns the bot latency",
                     option_type=3,
                     required=True)
             ],
             guild_ids=guild_ids)
async def _ping(ctx, message: str):
    print(f"/ping {message}")
    await ctx.respond()
    await ctx.send(
        f'Pong! {round(client.latency * 1000)}ms. You responded with {message}.'
    )


@slash.slash(name="8ball",
             description="Returns yes or no to your question",
             options=[
                 manage_commands.create_option(
                     name="question",
                     description="Enter your question here",
                     option_type=3,
                     required=True)
             ],
             guild_ids=guild_ids)
async def _8ball(ctx, question: str):
    print(f"/8ball {question}")
    responses = [
        "It is certain.", "It is decidedly so.", "Without a doubt.",
        "Yes - definitely.", "You may rely on it.", "As I see it, yes.",
        "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
        "send hazy, try again.", "Ask again later.",
        "Better not tell you now.", "Cannot predict now.",
        "Concentrate and ask again.", "Don't count on it.",
        "My response is no.", "My sources say no.", "Outlook not so good.",
        "Very doubtful."
    ]
    await ctx.respond()
    await ctx.send(f'{random.choice(responses)}')


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=next(status)))


@slash.slash(name="invite",
             description="Shows the invite link for the bot",
             guild_ids=guild_ids)
async def _invite(ctx):
    print("/invite")
    embed = discord.Embed(colour=discord.Colour.orange())
    embed.add_field(
        name='Invite the bot!',
        value=
        'Click [here](https://discord.com/api/oauth2/authorize?client_id=811277990913769523&permissions=4260888151&scope=bot%20applications.commands)',
        inline=False)
    await ctx.respond()
    await ctx.send(embed=embed)


@slash.slash(name="perseverance",
             description="Shows a photo of Perseverance",
             guild_ids=guild_ids)
async def _perseverance(ctx):
    await ctx.respond()
    await ctx.send(file=discord.File('perseverance.jpeg'))


@slash.slash(name="credits",
             description="Shows the credits",
             guild_ids=guild_ids)
async def _credits(ctx):
    print("/credits")
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
    embed.add_field(
        name='Documentations Used:',
        value=
        'https://discordpy.readthedocs.io/en/latest/\nhttps://discord-py-slash-command.readthedocs.io/en/latest/',
        inline=False)
    embed.add_field(
        name='Invite the bot!',
        value=
        'Click [here](https://discord.com/api/oauth2/authorize?client_id=811277990913769523&permissions=4260888151&scope=bot%20applications.commands)',
        inline=False)
    await ctx.respond()
    await ctx.send(embed=embed)


@slash.slash(
    name="help",
    description="Shows all the possible commands and how to use them",
    options=[
        manage_commands.create_option(
            name="command",
            description=
            'Will show the specific command that you want to know about, or type "help" for all the commands',
            option_type=3,
            required=True)
    ],
    guild_ids=guild_ids)
async def _help(ctx, argone):  # noqa: C901
    print(f"/help {argone}")
    embed = discord.Embed(colour=discord.Colour.orange())
    arg = str(argone).lower()
    if arg == "ping":
        embed.set_author(name='Help for /ping')
        embed.add_field(name='/ping', value='Returns "Pong!"', inline=False)
        await ctx.respond()
        await ctx.send(embed=embed)

    elif arg == "inspire":
        embed.add_field(
            name='/inspire',
            value='Sends a random quote from https://zenquotes.io/',
            inline=False)
        await ctx.respond()
        await ctx.send(embed=embed)

    elif arg == "hi":
        embed.add_field(name='/hi', value='Returns "Hello!"', inline=False)
        await ctx.respond()
        await ctx.send(embed=embed)

    elif arg == "bye":
        embed.add_field(name='/bye', value='Returns "Bye!"', inline=False)
        await ctx.respond()
        await ctx.send(embed=embed)

    elif arg == "new":
        embed.add_field(name='/new text',
                        value='Adds more encouraging messages.',
                        inline=False)
        await ctx.respond()
        await ctx.send(embed=embed)

    elif arg == "list":
        embed.add_field(
            name='/list',
            value=
            'Only lists the encouragements that have been added from .new.',
            inline=False)
        await ctx.respond()
        await ctx.send(embed=embed)

    elif arg == "delete":
        embed.add_field(
            name='/delete number',
            value='Deletes the corsending encouraging message listed in /list.',
            inline=False)
        await ctx.respond()
        await ctx.send(embed=embed)

    elif arg == "hello":
        embed.add_field(name='/hello there',
                        value='Returns "General Kenobi!"',
                        inline=False)
        embed.add_field(name='/hello name',
                        value='Returns "Hello Name!"',
                        inline=False)
        await ctx.respond()
        await ctx.send(embed=embed)

    elif arg == "say":
        embed.add_field(name='/say "text"',
                        value='Says your text.',
                        inline=False)
        await ctx.respond()
        await ctx.send(embed=embed)

    elif arg == "8ball":
        embed.add_field(
            name='/8ball question',
            value=
            'Returns whether or not your question\'s answer is yes or no.',
            inline=False)
        await ctx.respond()
        await ctx.send(embed=embed)

    elif arg == "kick":
        embed.add_field(
            name='/kick',
            value='Kicks a member. \nNOTE: requires Kick Members permission.',
            inline=False)
        await ctx.respond()
        await ctx.send(embed=embed)

    elif arg == "ban":
        embed.add_field(
            name='/ban',
            value='Bans a member. \nNOTE: requires Ban Members permission.',
            inline=False)
        await ctx.respond()
        await ctx.send(embed=embed)

    elif arg == "unban":
        embed.add_field(
            name='/unban',
            value='Unbans a member. \nNOTE: requires Ban Members permission.',
            inline=False)
        await ctx.respond()
        await ctx.send(embed=embed)

    elif arg == "clear" or arg == "purge":
        embed.add_field(
            name='/clear number',
            value=
            'Deletes the number of messages. Default is 5. \nNOTE: requires Manage Messages permission.',
            inline=False)
        await ctx.respond()
        await ctx.send(embed=embed)

    elif arg == "perseverance":
        embed.add_field(name='/perseverance',
                        value='Shows a picture of Perseverance.',
                        inline=False)
        await ctx.respond()
        await ctx.send(embed=embed)

    elif arg == "wikipedia":
        embed.add_field(
            name='/wikipedia text results lines',
            value=
            'Search anything on Wikipedia! \nNOTE: results and lines are not required and have a default value of 1 and 5.',
            inline=False)
        await ctx.respond()
        await ctx.send(embed=embed)
    elif arg == "google":
        embed.add_field(
            name='/google text results',
            value='Google anything! \nNOTE: results is optional and max is 10, default is 5',
            inline=False)
        await ctx.respond()
        await ctx.send(embed=embed)

    elif arg == "joke":
        embed.add_field(name='/joke',
                        value='Gives you a random joke!',
                        inline=False)
        await ctx.respond()
        await ctx.send(embed=embed)

    elif arg == "invite":
        embed.add_field(
            name='Invite the bot!',
            value=
            'Click [here](https://discord.com/api/oauth2/authorize?client_id=811277990913769523&permissions=4260888151&scope=bot%20applications.commands)',
            inline=False)
        await ctx.respond()
        await ctx.send(embed=embed)

    else:
        embed.set_author(name='Help')
        embed.add_field(name='/help help',
                        value='Shows this message',
                        inline=False)
        embed.add_field(name='/credits',
                        value='Shows the credits.',
                        inline=False)
        embed.add_field(name='/ping message',
                        value='Returns "Pong!"',
                        inline=False)
        embed.add_field(name='/inspire',
                        value='send a random quote from https://zenquotes.io/',
                        inline=False)
        embed.add_field(name='/hi', value='Returns "Hello!"', inline=False)
        embed.add_field(name='/bye', value='Returns "Bye!"', inline=False)
        embed.add_field(name='/new text',
                        value='Adds more encouraging messages.',
                        inline=False)
        embed.add_field(
            name='/list',
            value=
            'Only lists the encouragements that have been added from /new.',
            inline=False)
        embed.add_field(
            name='/delete number',
            value='Deletes the corsending encouraging message listed in /list.',
            inline=False)
        embed.add_field(name='/hello there',
                        value='Returns "General Kenobi!"',
                        inline=False)
        embed.add_field(name='/hello name',
                        value='Returns "Hello Name!"',
                        inline=False)
        embed.add_field(name='/say "text"',
                        value='Says your text.',
                        inline=False)
        embed.add_field(
            name='/8ball question',
            value=
            'Returns whether or not your question\'s answer is yes or no.',
            inline=False)
        embed.add_field(
            name='/kick',
            value='Kicks a member. \nNOTE: requires Kick Members permission.',
            inline=False)
        embed.add_field(
            name='/ban',
            value='Bans a member. \nNOTE: requires Ban Members permission.',
            inline=False)
        embed.add_field(
            name='/unban',
            value='Unbans a member. \nNOTE: requires Ban Members permission.',
            inline=False)
        embed.add_field(
            name='/clear number',
            value=
            'Deletes the number of messages. Default is 5. \nNOTE: requires Manage Messages permission.',
            inline=False)
        embed.add_field(name='/perseverance',
                        value='Shows a picture of Perseverance.',
                        inline=False)
        embed.add_field(
            name='/wikipedia text lines',
            value=
            'Search anything on Wikipedia! \nNOTE: results and lines are not required and have a default value of 1 and 5.',
            inline=False)
        embed.add_field(name='/joke',
                        value='Gives you a random joke!',
                        inline=False)
        embed.add_field(
            name='Invite the bot!',
            value=
            'Click [here](https://discord.com/api/oauth2/authorize?client_id=811277990913769523&permissions=4260888151&scope=bot%20applications.commands)',
            inline=False)

        await ctx.respond()
        await ctx.send(embed=embed)


keep_alive()
client.run(os.getenv('TOKEN'))
