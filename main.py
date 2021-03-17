# NOTE TO SELF: Don't keep this open before you put your laptop to sleep, close first, then close the laptop
# Otherwise, the bot will stop automatically

import subprocess

list_files = subprocess.run(["pip", "install", "googletrans==3.1.0a0"])

import os
import aiohttp
import json
import discord
import discord.ext as ext
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
from googletrans import Translator
from PyDictionary import PyDictionary

LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu'
}


def googleSearch(query):
    query = query.replace(" ", "+")
    g_clean = []
    if "http" not in query:
        url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(
            query)
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


def googleSearchImages(query):
    query = query.replace(" ", "+")
    g_clean = []
    if "http" not in query:
        url = 'https://www.google.com/search?hl=en&tbm=isch&sxsrf=ALeKk01Eh6GNz2vJrxJ-7rB-HY2SE-4xJQ%3A1615321310276&source=hp&biw=1366&bih=657&ei=3thHYNbEDpLZ-gSE-b6oCg&q={}&oq={}&gs_lcp=CgNpbWcQAzIFCAAQsQMyBQgAELEDMgUIABCxAzICCAAyBQgAELEDMgIIADIFCAAQsQMyBQgAELEDMgIIADIFCAAQsQM6BwgjEOoCECc6BAgjECc6CAgAELEDEIMBUOaYC1jTmwtgzJ0LaAFwAHgAgAFiiAHcAZIBATOYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABCg&sclient=img&ved=0ahUKEwjWq5TnhKTvAhWSrJ4KHYS8D6UQ4dUDCAc&uact=5'.format(
            query, query)
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

banana = discord.Client()
client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)
status = cycle([
    '/help help', 'your messages', '/help help', 'Never Gonna Give You Up',
    '/help help', 'try /setup if the slash commands are not working'
])

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


def reci(hello, there):
    return f"{there}/{hello}"


async def get_quote():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://zenquotes.io/api/random') as resp:
            json_data = json.loads(await resp.text())
            quote = '"' + json_data[0]['q'] + '" - ' + json_data[0]['a']
            return (quote)


@client.event
async def on_ready():
    await banana.wait_until_ready()
    change_status.start()
    print('We have logged in as {0.user}'.format(client))
    timestamp = datetime.datetime.now()
    print(timestamp.strftime(r"%A, %b %d, %Y, %I:%M %p UTC"))


@client.event
async def on_message(message):

    msg = message.content.lower()

    if db["responding"] == True:
        if "encouragements" in db.keys():
            options = db["encouragements"]

        if any(word in msg for word in sad_words):
            if "!" not in msg and "." not in msg and "not" not in msg and "n't" not in msg and "aint" not in msg and "never" not in msg:
                await message.reply(random.choice(options))

        mention = f'<@!{client.user.id}>'
        if mention in msg:
            await message.reply("You mentioned me!")

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
    if msg == "/restart":
        idea = message.author.id
        if idea == 721093211577385020:
            await message.reply("Restarting...")
            await message.reply(
                "Please wait up to 5 minutes, usually takes 1 minute.")
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            await message.reply("You're not my creator, go away.")
            await message.reply("Wait, how did you know about this?")


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
    if member.guild.id == 820419188866547712:
        role = "Shark"
        await member.add_roles(discord.utils.get(member.guild.roles, name=role))


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
    print(f"{ctx.author.name}: /hi")
    await ctx.respond()
    await ctx.send('Hello!')


@slash.slash(name="bye",
             description="The bot will say bye to you",
             guild_ids=guild_ids)
async def _bye(ctx):
    print(f"{ctx.author.name}: /bye")
    await ctx.respond()
    await ctx.send('Bye!')


@slash.slash(name="list",
             description="Lists the encouraging messages",
             guild_ids=guild_ids)
async def _list(ctx):
    print(f"{ctx.author.name}: /list")
    encouragements = []
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
    await ctx.respond()
    length = len(encouragements)
    await ctx.send("List of responses:")
    for x in range(0, length):
        await ctx.send(f"{x+1}. {encouragements[x]}")


@slash.slash(
    name="delete",
    description="Deletes an encouraging message, /list to see",
    options=[
        manage_commands.create_option(
            name="number",
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
        print(f"{ctx.author.name}: /delete {argone}")
        delete_encouragment(index)
        encouragements = db["encouragements"]
    await ctx.respond()
    length = len(encouragements)
    await ctx.send("List of responses:")
    for x in range(0, length):
        await ctx.send(f"{x+1}. {encouragements[x]}")


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
    print(f"{ctx.author.name}: /new {argone}")
    encouraging_message = argone
    update_encouragements(encouraging_message)
    encouragements = []
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
    await ctx.respond()
    await ctx.send(f'New encouraging message added: {encouraging_message}')
    await ctx.respond()
    length = len(encouragements)
    await ctx.send("List of responses:")
    for x in range(0, length):
        await ctx.send(f"{x+1}. {encouragements[x]}")


@slash.slash(name="purge", description="Delete messages", guild_ids=guild_ids)
@commands.has_permissions(manage_messages=True)
async def _purge(ctx, amount=5):
    print(f"{ctx.author.name}: /purge {amount}")
    amount = int(amount)
    await ctx.channel.purge(limit=amount + 1)
    await ctx.respond()
    await ctx.send(f"Removed {amount} messages.")
    await asyncio.sleep(3)
    await ctx.channel.purge(limit=2)


@client.event
async def on_slash_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.respond()
        await ctx.send(
            f"You don't have the required permissions to run this command, {ctx.author.mention}."
        )


@slash.slash(name="kick", description="Kicks a member", guild_ids=guild_ids)
@commands.has_permissions(kick_members=True)
async def _kick(ctx, member: discord.Member, *, reason=None):
    print(f"{ctx.author.name}: /kick {member} {reason}")
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
    print(f"{ctx.author.name}: /wikipedia {text} {lines}")
    result = wikipedia.search(text, results)
    await ctx.respond()
    try:
        end = random.choice(result)
        info = wikipedia.summary(end, int(lines))
        if len(info) <= 2000:
            await ctx.send(info)
        else:
            await ctx.send("The message is too long, please use less lines.")
    except IndexError:
        await ctx.send("No results found.")
    except discord.errors.NotFound:
        await ctx.send("Please try again.")
    except Exception as e:
        print(e)
        await ctx.send(
            "ERROR, there may be too many to choose from, or a module error.")


@slash.slash(name="joke", description="Gives you a joke", guild_ids=guild_ids)
async def _joke(ctx):
    print(f"{ctx.author.name}: /joke")
    await ctx.respond()
    await ctx.send(pyjokes.get_joke())


@slash.slash(
    name="google",
    description="Search anything on Google!",
    options=[
        manage_commands.create_option(name="text",
                                      description="Search it here",
                                      option_type=3,
                                      required=True),
        manage_commands.create_option(
            name="results",
            description="How many results? Max is 10 and default is 5",
            option_type=3,
            required=False)
    ],
    guild_ids=guild_ids)
async def _google(ctx, text, results=5):
    print(f"{ctx.author.name}: /google {text} {results}")
    result = googleSearch(text)
    results = int(results)
    try:
        a, b, c, d, e, f, g, h, i, j = result
        alphabet = [a, b, c, d, e, f, g, h, i, j]
    except:
        a, b, c, d, e, f, g, h, i = result
        alphabet = [a, b, c, d, e, f, g, h, i]
    await ctx.respond()
    if results > 10:
        await ctx.send("Results must be between 1 and 10")
        return False
    for x in range(0, results):
        await ctx.send(alphabet[x])
    query = text.replace(" ", "+")
    if "http" not in query:
        url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(
            query)
    else:
        url = query
    await ctx.send(f"URL: {url}")


@slash.slash(
    name="googleimages",
    description="Search images on Google!",
    options=[
        manage_commands.create_option(name="text",
                                      description="Search it here",
                                      option_type=3,
                                      required=True),
        manage_commands.create_option(
            name="results",
            description="How many results? Max is 10 and default is 5",
            option_type=3,
            required=False)
    ],
    guild_ids=guild_ids)
async def _googleimages(ctx, text, results=5):
    print(f"{ctx.author.name}: /googleimages {text} {results}")
    result = googleSearchImages(text)
    results = int(results)
    try:
        a, b, c, d, e, f, g, h, i, j = result
        alphabet = [a, b, c, d, e, f, g, h, i, j]
    except:
        a, b, c, d, e, f, g, h, i = result
        alphabet = [a, b, c, d, e, f, g, h, i]
    await ctx.respond()
    if results > 10:
        await ctx.send("Results must be between 1 and 10")
        return False
    for x in range(0, results):
        await ctx.send(alphabet[x])
    query = text.replace(" ", "+")
    if "http" not in query:
        url = 'https://www.google.com/search?hl=en&tbm=isch&sxsrf=ALeKk01Eh6GNz2vJrxJ-7rB-HY2SE-4xJQ%3A1615321310276&source=hp&biw=1366&bih=657&ei=3thHYNbEDpLZ-gSE-b6oCg&q={}&oq={}&gs_lcp=CgNpbWcQAzIFCAAQsQMyBQgAELEDMgUIABCxAzICCAAyBQgAELEDMgIIADIFCAAQsQMyBQgAELEDMgIIADIFCAAQsQM6BwgjEOoCECc6BAgjECc6CAgAELEDEIMBUOaYC1jTmwtgzJ0LaAFwAHgAgAFiiAHcAZIBATOYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABCg&sclient=img&ved=0ahUKEwjWq5TnhKTvAhWSrJ4KHYS8D6UQ4dUDCAc&uact=5'.format(
            query, query)
    else:
        url = query
    await ctx.send(f"URL: {url}")


@slash.slash(
    name="translate",
    description="Translate anything on Google Translate!",
    options=[
        manage_commands.create_option(name="text",
                                      description="Search it here",
                                      option_type=3,
                                      required=True),
        manage_commands.create_option(
            name="output_lang",
            description="First 2 letters of output lang, default en",
            option_type=3,
            required=False),
        manage_commands.create_option(
            name="input_lang",
            description="First 2 letters of input_lang, default automatic",
            option_type=3,
            required=False)
    ],
    guild_ids=guild_ids)
async def _translate(ctx, text, output_lang="en", input_lang=None):
    print(f"{ctx.author.name}: /translate {text} {output_lang} {input_lang}")
    if input_lang == None:
        try:
            output_lang2 = output_lang
            translator = Translator()
            translated = translator.translate(text, dest=output_lang2)
            await ctx.respond()
            await ctx.send(f"{translated.text}")
        except Exception as e:
            print(str(e))
            await ctx.respond()
            await ctx.send("ERROR")
            await ctx.send("Make sure that your output_lang is one of these:")
            await ctx.send(f"{LANGUAGES}")
    else:
        try:
            output_lang2 = output_lang
            input_lang2 = input_lang
            translator = Translator()
            translated = translator.translate(text,
                                              src=input_lang2,
                                              dest=output_lang2)
            await ctx.respond()
            await ctx.send(f"{translated.text}")
        except Exception as e:
            print(str(e))
            await ctx.respond()
            await ctx.send("ERROR")
            await ctx.send(
                "Make sure that your output_lang or input_lang is one of these:"
            )
            await ctx.send(f"{LANGUAGES}")


@slash.slash(name="define",
             description="Define any word in English!",
             options=[
                 manage_commands.create_option(name="word",
                                               description="Type it here",
                                               option_type=3,
                                               required=True)
             ],
             guild_ids=guild_ids)
async def _define(ctx, word):  # noqa: C901
    try:
        print(f"{ctx.author.name}: /define {word}")
        dictionary = PyDictionary()
        if "bonk" not in word.lower():
            defined = dictionary.meaning(f"{word}")
            await ctx.respond()
            if defined.get('Noun', 99) != 99:
                bye1 = defined['Noun']
                await ctx.send("Noun meaning(s):")
                for i in range(0, len(bye1)):
                    await asyncio.sleep(0.5)
                    await ctx.send(f"{i+1}. {bye1[i]}")
            if defined.get('Verb', 99) != 99:
                bye2 = defined['Verb']
                await ctx.send("Verb meaning(s):")
                for i in range(0, len(bye2)):
                    await asyncio.sleep(0.5)
                    await ctx.send(f"{i+1}. {bye2[i]}")
            if defined.get('Pronoun', 99) != 99:
                bye3 = defined['Pronoun']
                await ctx.send("Pronoun meaning(s):")
                for i in range(0, len(bye3)):
                    await asyncio.sleep(0.5)
                    await ctx.send(f"{i+1}. {bye3[i]}")
            if defined.get('Adjective', 99) != 99:
                bye4 = defined['Adjective']
                await ctx.send("Adjective meaning(s):")
                for i in range(0, len(bye4)):
                    await asyncio.sleep(0.5)
                    await ctx.send(f"{i+1}. {bye4[i]}")
            if defined.get('Adverb', 99) != 99:
                bye5 = defined['Adverb']
                await ctx.send("Adverb meaning(s):")
                for i in range(0, len(bye5)):
                    await asyncio.sleep(0.5)
                    await ctx.send(f"{i+1}. {bye5[i]}")
            if defined.get('Preposition', 99) != 99:
                bye6 = defined['Preposition']
                await ctx.send("Preposition meaning(s):")
                for i in range(0, len(bye6)):
                    await asyncio.sleep(0.5)
                    await ctx.send(f"{i+1}. {bye6[i]}")
            if defined.get('Conjunction', 99) != 99:
                bye7 = defined['Conjunction']
                await ctx.send("Conjunction meaning(s):")
                for i in range(0, len(bye7)):
                    await asyncio.sleep(0.5)
                    await ctx.send(f"{i+1}. {bye7[i]}")
            if defined.get('Interjection', 99) != 99:
                bye8 = defined['Interjection']
                await ctx.send("Interjection meaning(s):")
                for i in range(0, len(bye8)):
                    await asyncio.sleep(0.5)
                    await ctx.send(f"{i+1}. {bye8[i]}")
            if defined.get('Numeral', 99) != 99:
                bye9 = defined['Numeral']
                await ctx.send("Numeral meaning(s):")
                for i in range(0, len(bye9)):
                    await asyncio.sleep(0.5)
                    await ctx.send(f"{i+1}. {bye9[i]}")
            if defined.get('Article', 99) != 99:
                bye10 = defined['Article']
                await ctx.send("Article meaning(s):")
                for i in range(0, len(bye10)):
                    await asyncio.sleep(0.5)
                    await ctx.send(f"{i+1}. {bye10[i]}")
            if defined.get('Determiner', 99) != 99:
                bye11 = defined['Determiner']
                await ctx.send("Determiner meaning(s):")
                for i in range(0, len(bye11)):
                    await asyncio.sleep(0.5)
                    await ctx.send(f"{i+1}. {bye11[i]}")
        else:
            pass
    except Exception as e:
        print(str(e))
        print(str(e))
        print(str(e))
        await ctx.send("ERROR: Is this not a word? Are you misspelling it?")


@slash.slash(name="reverse",
             description="Reverses your text",
             options=[
                 manage_commands.create_option(name="text",
                                               description="Type it here",
                                               option_type=3,
                                               required=True)
             ],
             guild_ids=guild_ids)
async def _reverse(ctx, text):
    await ctx.respond()
    await ctx.send(text[::-1])


@slash.slash(name="reciprocal",
             description="Sends a reciprocal of a fraction",
             options=[
                 manage_commands.create_option(name="fraction",
                                               description="Type it here",
                                               option_type=3,
                                               required=True)
             ],
             guild_ids=guild_ids)
async def _reciprocal(ctx, fraction):
    fr1, fr2 = fraction.split("/")
    print(f"{ctx.author.name}: /reciprocal")
    Reci = reci(fr1, fr2)
    await ctx.respond()
    await ctx.send(f"{Reci}")


@slash.slash(name="nick",
             description="Sends a reciprocal of a fraction",
             options=[
                 manage_commands.create_option(name="member",
                                               description="Type member here",
                                               option_type=6,
                                               required=True),
                 manage_commands.create_option(name="nick",
                                               description="Type new nick here",
                                               option_type=3,
                                               required=True)
             ],
             guild_ids=guild_ids)
@commands.has_permissions(manage_nicknames=True)
async def _nick(ctx, member: discord.Member, nick):
    await ctx.respond()
    try:
        await member.edit(nick=nick)
        await ctx.send(f'Nickname was changed for {member.mention}.')
    except Exception as e:
        print(str(e))


@slash.slash(name="addrole", description="Adds a role", guild_ids=guild_ids)
@commands.has_permissions(manage_roles=True)
async def _addrole(ctx, member: discord.Member, role: discord.Role):
    await ctx.respond()
    await member.add_roles(role)
    await ctx.send(f"{member.mention} got the {role} role.")


@slash.slash(name="removerole", description="Removes a role", guild_ids=guild_ids)
@commands.has_permissions(manage_roles=True)
async def _removerole(ctx, member: discord.Member, role: discord.Role):
    await ctx.respond()
    await member.remove_roles(role)
    await ctx.send(f"{member.mention} lost the {role} role.")


@slash.slash(name="feedback",
             description="Give feedback!",
             options=[
                 manage_commands.create_option(name="feedback",
                                               description="Type member here",
                                               option_type=3,
                                               required=True)
             ],
             guild_ids=guild_ids)
async def _feedback(ctx, feedback):
    await ctx.respond()
    idea = ctx.author.id
    with open("feedback.txt", "a+") as file:
        file.write(f"{idea}§{feedback}\n")
    await ctx.send(f"You submitted the following feedback: {feedback}")


@slash.slash(name="feedbacklist",
             description="List feedback!",
             guild_ids=guild_ids)
async def _feedbacklist(ctx):
    await ctx.respond()
    with open("feedback.txt", "r") as file:
        for line in file:
            idea, feedback = line.split("§")
            print(idea)
            try:
                user = await banana.fetch_user(int(idea))
                await ctx.send(f"{user}: {feedback}")
            except Exception as e:
                print(str(e))


@slash.slash(name="ban", description="Bans a member", guild_ids=guild_ids)
@commands.has_permissions(ban_members=True)
async def _ban(ctx, member: discord.Member, *, reason=None):
    print(f"{ctx.author.name}: /ban {member} {reason}")
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
    print(f"{ctx.author.name}: /unban {argone}")
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
    print(f"{ctx.author.name}: /hello {argone}")
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
                 manage_commands.create_option(name="text",
                                               description="Say your message",
                                               option_type=3,
                                               required=True)
             ],
             guild_ids=guild_ids)
async def _say(ctx, text):
    print(f"{ctx.author.name}: /say {text}")
    await ctx.respond()
    await ctx.channel.send(text)
    await ctx.message.delete()


@slash.slash(name="ping",
             description="This returns the bot latency",
             guild_ids=guild_ids)
async def _ping(ctx):
    print(f"{ctx.author.name}: /ping")
    await ctx.respond()
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms.')


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
    print(f"{ctx.author.name}: /8ball {question}")
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
    await ctx.send(random.choice(responses))


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=next(status)))


@slash.slash(name="invite",
             description="Shows the invite link for the bot",
             guild_ids=guild_ids)
async def _invite(ctx):
    print(f"{ctx.author.name}: /invite")
    embed = discord.Embed(colour=discord.Colour.orange())
    embed.add_field(
        name='Invite the bot!',
        value=
        'Click [here](https://discord.com/api/oauth2/authorize?client_id=811277990913769523&permissions=4260888151&scope=bot%20applications.commands)',
        inline=False)
    await ctx.respond()
    await ctx.send(embed=embed)


@slash.slash(name="perseverance",
             description="Shows the profile picture of Perseverance",
             guild_ids=guild_ids)
async def _perseverance(ctx):
    print(f"{ctx.author.name}: /perseverance")
    await ctx.respond()
    await ctx.send(file=discord.File('preservation.png'))


@slash.slash(
    name="embed",
    description="Create an embed",
    options=[
        manage_commands.create_option(name="title",
                                      description="Enter your title here",
                                      option_type=3,
                                      required=True),
        manage_commands.create_option(name="text",
                                      description="Enter your text here",
                                      option_type=3,
                                      required=True),
        manage_commands.create_option(
            name="color",
            description=
            "What color should the embed be? Pick 'random' or any color from rainbow",
            option_type=3,
            required=False)
    ],
    guild_ids=guild_ids)
async def _embed(ctx, title, text, color="default"):
    print(f"{ctx.author.name}: /embed {title} {text} {color}")
    colory = color.lower()
    if colory == "red":
        colory = discord.Colour.red()
    elif colory == "orange":
        colory = discord.Colour.orange()
    elif colory == "yellow":
        colory = discord.Colour.yellow()
    elif colory == "green":
        colory = discord.Colour.green()
    elif colory == "blue":
        colory = discord.Colour.blue()
    elif colory == "indigo":
        colory = discord.Colour.dark_blue()
    elif colory == "purple":
        colory = discord.Colour.purple()
    elif colory == "default":
        colory = discord.Colour.default()
    else:
        colory = discord.Colour.random()

    embed = discord.Embed(colour=colory)
    embed.add_field(name=title, value=text, inline=False)

    await ctx.respond()
    await ctx.send(embed=embed)


@slash.slash(name="credits",
             description="Shows the credits",
             guild_ids=guild_ids)
async def _credits(ctx):
    print(f"{ctx.author.name}: /credits")
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
        'Click [here](https://discord.com/api/oauth2/authorize?client_id=811277990913769523&permissions=2148002902&scope=bot%20applications.commands)',
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
    print(f"{ctx.author.name}: /help {argone}")
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

    elif arg == "purge" or arg == "clear":
        embed.add_field(
            name='/purge number',
            value=
            'Deletes the number of messages. Default is 5. \nNOTE: requires Manage Messages permission.',
            inline=False)
        await ctx.respond()
        await ctx.send(embed=embed)

    elif arg == "perseverance":
        embed.add_field(name='/perseverance',
                        value='Shows the profile picture of Perseverance',
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
            value=
            'Google anything! \nNOTE: results is optional and max is 10, default is 5',
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
            'Click [here](https://discord.com/api/oauth2/authorize?client_id=811277990913769523&permissions=2148002902&scope=bot%20applications.commands)',
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
            name='/purge number',
            value=
            'Deletes the number of messages. Default is 5. \nNOTE: requires Manage Messages permission.',
            inline=False)
        embed.add_field(name='/perseverance',
                        value='Shows the profile picture of Perseverance',
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
            'Click [here](https://discord.com/api/oauth2/authorize?client_id=811277990913769523&permissions=2148002902&scope=bot%20applications.commands)',
            inline=False)

        await ctx.respond()
        await ctx.send(embed=embed)


keep_alive()
client.run(os.getenv('TOKEN'))
