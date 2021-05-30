import subprocess

list_files = subprocess.run(["pip", "install", "--upgrade", "pip"])
list_files = subprocess.run(["pip", "install", "googletrans==3.1.0a0"])
list_files = subprocess.run(["pip", "install", "prsaw"])

import os
import discord
from discord.ext import commands, tasks
import logging
import random
from replit import db
from website.keep_alive import keep_alive
import asyncio
from itertools import cycle
from discord_slash import SlashCommand
import sys
import datetime
import wikipedia as wiki
from discord_slash.utils.manage_commands import create_option, create_choice
import string
from discord.flags import Intents
import re, ast, inspect
from discord.utils import get
import youtube_dl
from pretty_help import PrettyHelp

from asteval import Interpreter

aeval = Interpreter()

from cmds.credits import show_credits
from cmds.define import pls_define
from cmds.eight_ball import answer
from cmds.embed import create_embed
from cmds.feedback import create_feedback, list_feedback, delete_feedback
from cmds.googlestuff import pls_google, pls_translate
from cmds.help import help_embeds2
from cmds.inspire import inspired
from cmds.poll import create_poll
from cmds.morse import encrypt, decrypt
from cmds.reply import maybe_reply as meply
from cmds.purge import purge_msgs
from cmds.ytactivity import group_say
from cmds.ai import ai_response, get_a_joke, get_image
from cmds.tic import tictactoe_, place_

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log',
                              encoding='utf-8',
                              mode='w')
handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix="\\",
                   intents=Intents.all(),
                   help_command=PrettyHelp(
                       color=discord.Colour.orange(),
                       page_left="◀️",
                       page_right="▶️",
                       remove="❌",
                   ))
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)
servers = len(bot.guilds)
status = cycle([
    '/help or \\help', 'your messages', '/help or \\help',
    'Never Gonna Give You Up', '/help or \\help', 'hello there!',
    '/help or \\help', f'{servers} servers'
])

guild_ids = db["id"]


@bot.event
async def on_ready():
    change_status.start()
    print(f'We have logged in as {bot.user}')
    logger.info(f'We have logged in as {bot.user}')
    timestamp = datetime.datetime.now()
    print(timestamp.strftime(r"%A, %b %d, %Y, %I:%M %p UTC"))
    logger.info(timestamp.strftime(r"%A, %b %d, %Y, %I:%M %p UTC"))
    print(f"guild_ids={guild_ids}")
    logger.info(f"guild_ids={guild_ids}")
    print(f"In {len(bot.guilds)} servers")
    logger.info(f"In {len(bot.guilds)} servers")
    with open("guilds.txt", "w") as f:
        f.write(f"{len(bot.guilds)}")
    with open("guilds.txt", "r") as f:
        servers = f.read()
        global status
        status = cycle([
            '/help or .help', 'your messages', '/help or .help',
            'Never Gonna Give You Up', '/help or .help', 'hello there!',
            '/help or .help', f'{servers} servers'
        ])


@bot.event
async def on_message(message):

    msg = message.content.lower()

    if msg == "/setup":
        if message.author.id == 721093211577385020:
            logger.info('/setup')
            ido = message.guild.id
            if ido not in db["id"]:
                ids = db["id"]
                ids.append(ido)
                db["id"] = ids
                logger.info(db["id"])
                await message.reply(
                    "Server has been set up! The bot is restarting! If the error persists, contact <@!721093211577385020> in Discord to restart the bot!"
                )
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                await message.reply(
                    "Server already setup! The bot is restarting! If the error persists, contact <@!721093211577385020> in Discord to restart the bot!"
                )
                os.execl(sys.executable, sys.executable, *sys.argv)
    if msg == "/restart" or msg == "\\restart":
        if message.author.id == 721093211577385020:
            await message.add_reaction('🆗')
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            await message.add_reaction('<:no:828741445069963274>')

    await bot.process_commands(message)


@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(
                'Thank you for inviting me! If you have any issues, DM <@!721093211577385020> or join the Discord bot server here: https://discord.gg/QFcMcCQGbU'
            )
        break
    with open("guilds.txt", "w") as f:
        f.write(f"{len(bot.guilds)}")


@bot.event
async def on_guild_remove(guild):
    ido = int(guild.id)
    ids = db["id"]
    ids.remove(ido)
    db["id"] = ids
    logger.info(db["id"])
    with open("guilds.txt", "w") as f:
        f.write(f"{len(bot.guilds)}")


@bot.event
async def on_member_join(member):
    logger.info(f'{member} has joined {member.guild.name}')
    if member.guild.id == 820419188866547712:
        role = "Shark"
        await member.add_roles(discord.utils.get(member.guild.roles,
                                                 name=role))


@bot.event
async def on_member_remove(member):
    logger.info(f'{member} has left {member.guild.name}')


@bot.event
async def on_slash_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        perms_missing = error.missing_perms
        perms_missing = f"{perms_missing}"
        perms_missing = perms_missing.strip("[]'")
        perms_missing = perms_missing.replace("_", " ")
        await ctx.send(
            f"You don't have `{perms_missing}` permissions to run this command, {ctx.author.mention}."
        )
    else:
        raise error


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        perms_missing = error.missing_perms
        perms_missing = f"{perms_missing}"
        perms_missing = perms_missing.strip("[]'")
        perms_missing = perms_missing.replace("_", " ")
        await ctx.send(
            f"You don't have {perms_missing} permissions to run this command, {ctx.author.mention}."
        )
    else:
        raise error


@tasks.loop(seconds=15)
async def change_status():
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=next(status)))


@bot.command(help="Gives a random inspirational quote.")
async def inspire(ctx):
    logger.info(f"{ctx.author.name}: .inspire")
    quoted = await inspired(ctx)
    await meply(ctx, quoted)


@slash.slash(name="inspire",
             description="The bot will send a random inspirational quote")
async def _inspire(ctx):
    await ctx.defer()
    logger.info(f"{ctx.author.name}: /inspire")
    quoted = await inspired(ctx)
    await ctx.send(quoted)


@bot.command(help="The bot will say hello to you!")
async def hi(ctx):
    await meply(ctx, "Hello!")


@slash.slash(name="hi", description="The bot will say hello to you")
async def _hi(ctx):
    await ctx.defer()
    logger.info(f"{ctx.author.name}: /hi")
    await ctx.send('Hello!')


@bot.command(help="The bot will say bye to you.")
async def bye(ctx):
    logger.info(f"{ctx.author.name}: .bye")
    await meply(ctx, "Bye!")


@slash.slash(name="bye", description="The bot will say bye to you")
async def _bye(ctx):
    logger.info(f"{ctx.author.name}: /bye")
    await ctx.defer()
    await ctx.send('Bye!')


@bot.command(help="Get an AI response!")
async def ai(ctx, *, msg):
    if "shark" in msg:
        await ctx.send("Sharks are the BEST!")
    else:
        await ai_response(ctx, msg)


@slash.slash(name="ai",
             description="Get AI response!",
             options=[
                 create_option(name="msg",
                               description="Your message",
                               option_type=3,
                               required=True)
             ])
async def _ai(ctx, msg):
    if "shark" in msg:
        await ctx.send("Sharks are the BEST!")
    else:
        await ai_response(ctx, msg)


@bot.command(help="Run some code!\nRequires you to be Toricane#0818.")
async def run(ctx, *, code):
    logger.info(f"{ctx.author.name}: .run {code}")
    try:
        if ctx.author.id == 721093211577385020:
            res = eval(code)
            if inspect.isawaitable(res):
                await ctx.send(await res)
            else:
                await ctx.send(res)
            await asyncio.sleep(1)
            await ctx.channel.purge(limit=1)
        else:
            await ctx.message.add_reaction('<:no:828741445069963274>')
    except Exception as e:
        logger.info(str(e))


@slash.slash(name="run",
             description="Run some code",
             options=[
                 create_option(name="code",
                               description="Add it here",
                               option_type=3,
                               required=True)
             ])
async def _run(ctx, code):
    logger.info(f"{ctx.author.name}: /run {code}")
    try:
        if ctx.author.id == 721093211577385020:
            res = eval(code)
            if inspect.isawaitable(res):
                await ctx.send(await res)
            else:
                await ctx.send(res)
        else:
            await ctx.send("No.")
    except Exception as e:
        logger.info(str(e))


@bot.command(aliases=["pfp"], help="View someone's profile picture")
async def avatar(ctx, member: discord.Member):
    logger.info(f"{ctx.author.name}: .avatar {member}")
    try:
        embed = discord.Embed(colour=discord.Colour.orange())
        url = member.avatar_url
        embed.add_field(name=f'{member}', value='Avatar:', inline=False)
        embed.set_image(url=url)
        await ctx.send(embed=embed)
    except Exception as e:
        logger.info(str(e))


@slash.slash(
    name="avatar",
    description="View someone's profile picture",
    options=[
        create_option(name="member",
                      description="Add the member here",
                      option_type=6,
                      required=True)
    ],
)
async def _avatar(ctx, member: discord.Member):
    logger.info(f"{ctx.author.name}: /avatar {member}")
    try:
        embed = discord.Embed(colour=discord.Colour.orange())
        url = member.avatar_url
        embed.add_field(name=f'{member}', value='Avatar:', inline=False)
        embed.set_image(url=url)
        await ctx.send(embed=embed)
    except Exception as e:
        logger.info(str(e))


@bot.command(aliases=["act"], help="Play games in the vc!")
async def activities(ctx, *, activity_type):
    number = None
    if activity_type.lower() == "youtube together":
        number = "755600276941176913"
        await group_say(ctx, number)
    elif activity_type.lower() in "betrayal.io":
        number = "773336526917861400"
        await group_say(ctx, number)
    elif activity_type.lower() in "poker night":
        number = "755827207812677713"
        await group_say(ctx, number)
    elif activity_type.lower() in "fishington.io":
        number = "814288819477020702"
        await group_say(ctx, number)
    elif activity_type.lower() in "chess":
        number = "832012682520428625"
        await group_say(ctx, number)
    else:
        await ctx.send("Invalid activity.")


@slash.slash(name="activities",
             description="Do stuff",
             options=[{
                 "name":
                 "activity_type",
                 "description":
                 "Type of activity.",
                 "required":
                 True,
                 "type":
                 3,
                 "choices": [
                     {
                         "name": "YouTube Together",
                         "value": "755600276941176913"
                     },
                     {
                         "name": "Betrayal.io",
                         "value": "773336526917861400"
                     },
                     {
                         "name": "Poker Night",
                         "value": "755827207812677713"
                     },
                     {
                         "name": "Fishington.io",
                         "value": "814288819477020702"
                     },
                     {
                         "name": "Chess",
                         "value": "832012682520428625"
                     },
                 ]
             }])
async def _activities(ctx, activity_type):
    await group_say(ctx, activity_type)


@bot.command(help="Delete some messages!\nDefault 5.\nRequires Manage Messages permission to use.")
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=5, user: discord.Member = None):
    logger.info(f"{ctx.author.name}: .purge {amount}")
    await purge_msgs(ctx, amount, usere=user, client=bot, method="dpy")


@slash.slash(name="purge",
             description="Delete messages",
             options=[
                 create_option(
                     name="amount",
                     description="Amount or range of messages to delete",
                     option_type=4,
                     required=True),
                 create_option(name="user",
                               description="Who's messages to delete",
                               option_type=6,
                               required=False)
             ])
@commands.has_permissions(manage_messages=True)
async def _purge(ctx, amount=5, user=None):
    logger.info(f"{ctx.author.name}: /purge {amount}")
    await ctx.defer()
    await purge_msgs(ctx, amount, usere=user, client=bot, method="dpy")


@bot.command(aliases=["wiki"],
             description="Searches for something on wikipedia",
             help="Search anything on Wikipedia!\nResults is set to 1 as default.\nLines is set to 5 as default.\n\nMore than one result will make the bot choose one at random.")
async def wikipedia(ctx, text: str, results: int = 1, lines: int = 5):
    logger.info(f"{ctx.author.name}: .wikipedia {text} {results} {lines}")
    result = wiki.search(text, results)
    try:
        end = random.choice(result)
        info = wiki.summary(end, lines)
        if len(info) <= 2000:
            await ctx.send(info)
        else:
            await ctx.send("The message is too long, please use fewer lines.")
    except IndexError:
        await ctx.send("No results found.")
    except discord.errors.NotFound:
        await ctx.send("Please try again.")
    except Exception as e:
        logger.info(e)
        await ctx.send(
            "ERROR, there may be too many to choose from, or a module error.")
        await ctx.send(f"ERROR: {e}")


@slash.slash(
    name="wikipedia",
    description="Searches for something on Wikipedia",
    options=[
        create_option(name="text",
                      description="What do you want to search?",
                      option_type=3,
                      required=True),
        create_option(
            name="results",
            description=
            "How many results should you randomly recieve 1 result from? Default is 5.",
            option_type=3,
            required=False),
        create_option(name="lines",
                      description="How many lines do you want? Default is 10.",
                      option_type=4,
                      required=False)
    ],
)
async def _wikipedia(ctx, text, results=1, lines=5):
    logger.info(f"{ctx.author.name}: /wikipedia {text} {results} {lines}")
    await ctx.defer()
    result = wiki.search(text, results)
    try:
        end = random.choice(result)
        info = wiki.summary(end, lines)
        if len(info) <= 2000:
            await ctx.send(info)
        else:
            await ctx.send("The message is too long, please use less lines.")
    except IndexError:
        await ctx.send("No results found.")
    except discord.errors.NotFound:
        await ctx.send("Please try again.")
    except Exception as e:
        logger.info(e)
        await ctx.send(
            "ERROR, there may be too many to choose from, or a module error.")
        await ctx.send(f"ERROR: {e}")


@bot.command(help="Gives a random joke.")
async def joke(ctx, *, joke=None):
    logger.info(f"{ctx.author.name}: .joke")
    if joke == None:
        await get_a_joke(ctx, joke)
    else:
        if "aww" in joke:
            await get_a_joke(ctx, joke, "aww")
        elif "duck" in joke:
            await get_a_joke(ctx, joke, "duck")
        elif "dog" in joke:
            await get_a_joke(ctx, joke, "dog")
        elif "cat" in joke:
            await get_a_joke(ctx, joke, "cat")
        elif "hold" in joke:
            await get_a_joke(ctx, joke, "holdup")
        elif "dankmeme" or "dank meme" in joke:
            await get_a_joke(ctx, joke, "dankmemes")
        elif "harrypotter" or "harry potter" in joke:
            await get_a_joke(ctx, joke, "harrypottermemes")
        elif "meme" in joke:
            await get_a_joke(ctx, joke, "memes")
        elif "art" in joke:
            await get_a_joke(ctx, joke, "art")
        elif "facepalm" or "face palm" in joke:
            await get_a_joke(ctx, joke, "facepalm")
        else:
            await ctx.send("Invalid option.")


@slash.slash(name="joke", description="Gives you a joke")
async def _joke(ctx):
    logger.info(f"{ctx.author.name}: /joke")


@bot.command()
async def image(ctx, *, joke=None):
    if joke != None:
        if "aww" in joke:
            await get_image(ctx, joke, "aww")
        elif "duck" in joke:
            await get_image(ctx, joke, "duck")
        elif "dog" in joke:
            await get_image(ctx, joke, "dog")
        elif "cat" in joke:
            await get_image(ctx, joke, "cat")
        elif "hold" in joke:
            await get_image(ctx, joke, "holdup")
        elif "dankmeme" or "dank meme" in joke:
            await get_image(ctx, joke, "dankmemes")
        elif "harrypotter" or "harry potter" in joke:
            await get_image(ctx, joke, "harrypottermemes")
        elif "meme" in joke:
            await get_image(ctx, joke, "memes")
        elif "art" in joke:
            await get_image(ctx, joke, "art")
        elif "facepalm" or "face palm" in joke:
            await get_image(ctx, joke, "facepalm")
        else:
            await ctx.send("Invalid option.")
    else:
        await get_image(ctx, joke)


@bot.command(help="Google anything with this command!")
async def google(ctx, text, results=5):
    logger.info(f"{ctx.author.name}: .google {text} {results}")
    await pls_google(ctx, text, results)


@slash.slash(
    name="google",
    description="Search anything on Google!",
    options=[
        create_option(name="text",
                      description="Search it here",
                      option_type=3,
                      required=True),
        create_option(
            name="results",
            description="How many results? Max is 10 and default is 5",
            option_type=3,
            required=False)
    ],
)
async def _google(ctx, text, results=5):
    logger.info(f"{ctx.author.name}: /google {text} {results}")
    await ctx.defer()
    await pls_google(ctx, text, results)


@bot.command(help="Translate text on Google Translate!\nOutput language is set to English as default.\nInput language is set to Detect Language as default.")
async def translate(ctx, text, output_lang="en", input_lang=None):
    logger.info(
        f"{ctx.author.name}: /translate {text} {output_lang} {input_lang}")
    await pls_translate(ctx, text, output_lang, input_lang)


@slash.slash(
    name="translate",
    description="Translate anything on Google Translate!",
    options=[
        create_option(name="text",
                      description="Search it here",
                      option_type=3,
                      required=True),
        create_option(name="output_lang",
                      description="First 2 letters of output lang, default en",
                      option_type=3,
                      required=False),
        create_option(
            name="input_lang",
            description="First 2 letters of input_lang, default automatic",
            option_type=3,
            required=False)
    ],
)
async def _translate(ctx, text, output_lang="en", input_lang=None):
    logger.info(
        f"{ctx.author.name}: /translate {text} {output_lang} {input_lang}")
    await ctx.defer()
    await pls_translate(ctx, text, output_lang, input_lang)


@bot.command(aliases=["def"], help="Define any word in English.")
async def define(ctx, word):
    logger.info(f"{ctx.author.name}: .define {word}")
    await pls_define(ctx, word)


@slash.slash(
    name="define",
    description="Define any word in English!",
    options=[
        create_option(name="word",
                      description="Type it here",
                      option_type=3,
                      required=True)
    ],
)
async def _define(ctx, word):  # noqa: C901
    await ctx.defer()
    logger.info(f"{ctx.author.name}: /define {word}")
    await pls_define(ctx, word)


@bot.command(aliases=["r", "rev"], help="Reverse your text!")
async def reverse(ctx, *, text):
    await ctx.send(text[::-1])


@slash.slash(
    name="reverse",
    description="Reverses your text",
    options=[
        create_option(name="text",
                      description="Type it here",
                      option_type=3,
                      required=True)
    ],
)
async def _reverse(ctx, text):
    await ctx.defer()
    await ctx.send(text[::-1])


@bot.command(aliases=["reci"], help="Get a reciprocal of a fraction!")
async def reciprocal(ctx, *, fraction):
    logger.info(f"{ctx.author.name}: .reciprocal {fraction}")
    fr1, fr2 = fraction.split("/")
    await ctx.send(f"{fr2}/{fr1}")


@slash.slash(
    name="reciprocal",
    description="Sends a reciprocal of a fraction",
    options=[
        create_option(name="fraction",
                      description="Type it here",
                      option_type=3,
                      required=True)
    ],
)
async def _reciprocal(ctx, fraction):
    logger.info(f"{ctx.author.name}: /reciprocal")
    fr1, fr2 = fraction.split("/")
    await ctx.send(f"{fr2}/{fr1}")


@bot.command(aliases=["nickname"], help="Change someone's nickname.\nRequires Manage Nicknames permission.")
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, *, nick):
    try:
        await member.edit(nick=nick)
        await ctx.send(f'Nickname was changed for {member.mention}.')
    except Exception as e:
        logger.info(str(e))
        await ctx.send("ERROR: is the member in the server?")


@slash.slash(
    name="nick",
    description="Sends a reciprocal of a fraction",
    options=[
        create_option(name="member",
                      description="Type member here",
                      option_type=6,
                      required=True),
        create_option(name="nick",
                      description="Type new nick here",
                      option_type=3,
                      required=True)
    ],
)
@commands.has_permissions(manage_nicknames=True)
async def _nick(ctx, member: discord.Member, nick):
    try:
        await member.edit(nick=nick)
        await ctx.send(f'Nickname was changed for {member.mention}.')
    except Exception as e:
        logger.info(str(e))
        await ctx.send("ERROR: is the member in the server?")


@bot.command(aliases=["fb"], help="Send feedback for the bot!")
async def feedback(ctx, *, feedback):
    logger.info(f"{ctx.author.name}: .feedback {feedback}")
    await create_feedback(ctx, feedback)


@slash.slash(
    name="feedback",
    description="Give feedback!",
    options=[
        create_option(name="feedback",
                      description="Type member here",
                      option_type=3,
                      required=True)
    ],
)
async def _feedback(ctx, feedback):
    logger.info(f"{ctx.author.name}: /feedback {feedback}")
    await create_feedback(ctx, feedback)


@bot.command(aliases=["fblist"], help="List the feedback.")
async def feedbacklist(ctx):
    logger.info(f"{ctx.author.name}: .feedbacklist")
    await ctx.send("List of feedbacks:")
    await list_feedback(ctx)


@slash.slash(name="feedbacklist", description="List feedback!")
async def _feedbacklist(ctx):
    logger.info(f"{ctx.author.name}: /feedbacklist")
    await ctx.defer()
    await ctx.send("List of feedbacks:")
    await list_feedback(ctx)


@bot.command(aliases=["fbclear"], help="Clear or delete feedback!\nRequires you to be Toricane#0818.\nTo find the number to delete, try using `/list` or `.list`.")
async def feedbackclear(ctx, number=None):
    logger.info(f"{ctx.author.name}: /feedbackclear {number}")
    await delete_feedback(ctx, number)


@slash.slash(
    name="feedbackclear",
    description="Clears all of the feedback or the chosen one",
    options=[
        create_option(
            name="number",
            description=
            "The feedback message position in the list that you want to clear, try /feedbacklist to see",
            option_type=4,
            required=False)
    ],
)
async def _feedbackclear(ctx, number=None):
    logger.info(f"{ctx.author.name}: /feedbackclear {number}")
    await ctx.defer()
    await delete_feedback(ctx, number)


@bot.command(help="Create a quick and easy poll!\nSeparate the choices with \"/\".")
async def poll(ctx, question, choices, mention=None):  # noqa: C901
    logger.info(f"{ctx.author.name}: /poll {question} {choices} {mention}")
    await create_poll(ctx, question, choices, mention)


@slash.slash(
    name="poll",
    description="Create a poll!",
    options=[
        create_option(name="question",
                      description="What is your question?",
                      option_type=3,
                      required=True),
        create_option(
            name="choices",
            description="What are the choices? Separate them using /.",
            option_type=3,
            required=True),
        create_option(name="mention",
                      description="What role to mention",
                      option_type=8,
                      required=False)
    ],
)
async def _poll(ctx, question, choices, mention=None):  # noqa: C901
    logger.info(f"{ctx.author.name}: /poll {question} {choices} {mention}")
    await ctx.defer()
    try:
        await create_poll(ctx, question, choices, mention)
    except Exception as e:
        logger.info(str(e))


@bot.command(help="Say hello to someone!")
async def hello(ctx, *, name):
    logger.info(f"{ctx.author.name}: .hello {name}")
    name = name.capitalize()
    if name == "There":
        await ctx.send("General Kenobi!")
    else:
        await ctx.send(f"Hello {name}!")
        await ctx.message.delete()


@slash.slash(
    name="hello",
    description="Say hello to someone",
    options=[
        create_option(name="name",
                      description='Put either "there" or the name',
                      option_type=3,
                      required=True)
    ],
)
async def _hello(ctx, name):
    await ctx.defer()
    logger.info(f"{ctx.author.name}: /hello {name}")
    name = name.capitalize()
    if name == "There":
        await ctx.send("General Kenobi!")
    else:
        await ctx.send(f"Hello {name}!")


@bot.command(help="Make the bot say anything!")
async def say(ctx, *, text):
    logger.info(f"{ctx.author.name}: .say {text}")
    await ctx.send(text, allowed_mentions=discord.AllowedMentions.none())
    await ctx.message.delete()
    logger.info(f"{ctx.author.name}: .say {text}")


@slash.slash(
    name="say",
    description="Make the bot say anything",
    options=[
        create_option(name="text",
                      description="Say your message",
                      option_type=3,
                      required=True)
    ],
)
async def _say(ctx, text):
    logger.info(f"{ctx.author.name}: /say {text}")
    msg = await ctx.send(text, allowed_mentions=discord.AllowedMentions.none())
    await msg.delete()
    await ctx.channel.send(text,
                           allowed_mentions=discord.AllowedMentions.none())


@bot.command(help="Returns pong with the latency in milliseconds.")
async def ping(ctx):
    logger.info(f"{ctx.author.name}: /ping")
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms.')


@slash.slash(name="ping", description="This returns the bot latency")
async def _ping(ctx):
    logger.info(f"{ctx.author.name}: .ping")
    await ctx.defer()
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms.')


@bot.command(aliases=["8ball"], help="Ask a question, and the bot tells your fortune.")
async def eightball(ctx, *, question):
    logger.info(f"{ctx.author.name}: .8ball {question}")
    await ctx.send(answer())


@slash.slash(
    name="8ball",
    description="Ask a question, and the bot tells your fortune.",
    options=[
        create_option(name="question",
                      description="Enter your question here",
                      option_type=3,
                      required=True)
    ],
)
async def _8ball(ctx, question):
    logger.info(f"{ctx.author.name}: /8ball {question}")
    await ctx.defer()
    await ctx.send(answer())


@bot.command(help="Get the invite link for the bot!")
async def invite(ctx):
    logger.info(f"{ctx.author.name}: .invite")
    embed = discord.Embed(colour=discord.Colour.orange())
    embed.add_field(
        name='Invite the bot!',
        value=
        'Click [here](https://discord.com/api/oauth2/authorize?client_id=811277990913769523&permissions=3691244614&scope=bot%20applications.commands)',
        inline=False)
    await ctx.send(embed=embed)


@slash.slash(name="invite", description="Shows the invite link for the bot")
async def _invite(ctx):
    logger.info(f"{ctx.author.name}: /invite")
    embed = discord.Embed(colour=discord.Colour.orange())
    embed.add_field(
        name='Invite the bot!',
        value=
        'Click [here](https://discord.com/api/oauth2/authorize?client_id=811277990913769523&permissions=3691244614&scope=bot%20applications.commands)',
        inline=False)
    await ctx.defer()
    await ctx.send(embed=embed)


@bot.command(help="Shows the bot's profile picture.")
async def perseverance(ctx):
    logger.info(f"{ctx.author.name}: .perseverance")
    await ctx.send("Profile Picture:")
    await ctx.send(file=discord.File('preservation.png'))


@slash.slash(
    name="perseverance",
    description="Shows the profile picture of Perseverance",
)
async def _perseverance(ctx):
    logger.info(f"{ctx.author.name}: /perseverance")
    await ctx.send("Profile Picture:")
    await ctx.send(file=discord.File('preservation.png'))


@bot.command(aliases=["pw", "pass"], help="Generate a strong, random password.")
async def password(ctx, length: int, dm=False):
    logger.info(f"{ctx.author.name}: .password {length} {dm}")
    if dm == "true" or dm == "yes":
        dm = True
    else:
        dm = False
    password_characters = string.ascii_letters + string.digits + string.punctuation
    password = []
    for i in range(length):
        password.append(random.choice(password_characters))
    password = "".join(password)
    if dm == False:
        await ctx.send(f"Your password is: ```{password}```", hidden=True)
    else:
        member = ctx.author
        await member.send(f"Your password is: ```{password}```")
        await ctx.send("Your password was successfully DM'ed to you.",
                       hidden=True)


@slash.slash(name="password",
             description="Gives you a strong password",
             options=[
                 create_option(name="length",
                               description="How long should your password be?",
                               option_type=4,
                               required=True),
                 create_option(
                     name="dm",
                     description="Should I DM the password? Default True",
                     option_type=5,
                     required=False)
             ])
async def _password(ctx, length, dm=False):
    logger.info(f"{ctx.author.name}: /password {length} {dm}")
    password_characters = string.ascii_letters + string.digits + string.punctuation
    password = []
    for i in range(length):
        password.append(random.choice(password_characters))
    password = "".join(password)
    if dm == False:
        await ctx.send(f"Your password is: ```{password}```", hidden=True)
    else:
        member = ctx.author
        await member.send(f"Your password is: ```{password}```")
        await ctx.send("Your password was successfully DM'ed to you.",
                       hidden=True)


@bot.command(aliases=["btt"], help="Convert binary numbers to text.")
async def binarytotext(ctx, *, text):
    ascii_string = "".join([chr(int(binary, 2)) for binary in text.split(" ")])
    await ctx.reply(f"```py\n{ascii_string}```")


@slash.slash(name="binarytotext",
             description="Get text from binary",
             options=[
                 create_option(name="text",
                               description="Your binary code",
                               option_type=3,
                               required=True)
             ])
async def binaryToText(ctx, text):
    await ctx.defer()
    ascii_string = "".join([chr(int(binary, 2)) for binary in text.split(" ")])
    await ctx.send(f"```py\n{ascii_string}```")


@bot.command(aliases=["ttb"], help="Convert text to binary!")
async def texttobinary(ctx, *, text):
    res = ' '.join(format(ord(i), '08b') for i in text)
    await ctx.reply(f"```py\n{res}```")


@slash.slash(name="texttobinary",
             description="Get binary from text",
             options=[
                 create_option(name="text",
                               description="Your binary code",
                               option_type=3,
                               required=True)
             ])
async def _texttobinary(ctx, text):
    await ctx.defer()
    res = ' '.join(format(ord(i), '08b') for i in text)
    await ctx.send(f"```py\n{res}```")


@bot.command(aliases=["ttm"], help="Convert text to morse!")
async def texttomorse(ctx, *, message):
    result = encrypt(message.upper())
    await ctx.reply(f"```py\n{result}```")


@slash.slash(name="texttomorse",
             description="Get morse code from text",
             options=[
                 create_option(name="text",
                               description="Your binary code",
                               option_type=3,
                               required=True)
             ])
async def _texttomorse(ctx, message):
    result = encrypt(message.upper())
    await ctx.send(f"```py\n{result}```")


@bot.command(aliases=["mtt"], help="Get text from morse code.")
async def morsetotext(ctx, *, message):
    result = decrypt(message)
    await ctx.reply(f"```py\n{result}```")


@slash.slash(name="morsetotext",
             description="Get text from morse code",
             options=[
                 create_option(name="text",
                               description="Your binary code",
                               option_type=3,
                               required=True)
             ])
async def _morsetotext(ctx, message):
    result = decrypt(message)
    await ctx.send(f"```py\n{result.lower()}```")


@bot.command(help="Create an embed using the bot!")
async def embed(ctx, title, text, color="default"):
    logger.info(f"{ctx.author.name}: .embed {title} {text} {color}")
    await create_embed(ctx, title, text, color)


@slash.slash(
    name="embed",
    description="Create an embed",
    options=[
        create_option(name="title",
                      description="Enter your title here",
                      option_type=3,
                      required=True),
        create_option(name="text",
                      description="Enter your text here",
                      option_type=3,
                      required=True),
        create_option(
            name="color",
            description=
            "What color should the embed be? Pick 'random' or any color from rainbow",
            option_type=3,
            required=False,
            choices=[
                create_choice(name="default", value="default"),
                create_choice(name="red", value="red"),
                create_choice(name="orange", value="orange"),
                create_choice(name="yellow", value="yellow"),
                create_choice(name="green", value="green"),
                create_choice(name="blue", value="blue"),
                create_choice(name="indigo", value="indigo"),
                create_choice(name="purple", value="purple"),
                create_choice(name="random", value="random"),
            ])
    ],
)
async def _embed(ctx, title, text, color="default"):
    logger.info(f"{ctx.author.name}: /embed {title} {text} {color}")
    await ctx.defer()
    await create_embed(ctx, title, text, color)


@bot.command(aliases=["info", "about"], help="Displays the credits.")
async def credits(ctx):
    logger.info(f"{ctx.author.name}: .credits")
    await show_credits(ctx)


@slash.slash(name="credits", description="Shows the credits")
async def _credits(ctx):
    logger.info(f"{ctx.author.name}: /credits")
    await ctx.defer()
    await show_credits(ctx)


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address':
    '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {'options': '-vn'}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options),
                   data=data)


@bot.command(help="Play a song in the VC!")
async def play(ctx, *, url=None):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await voice.disconnect()
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    if url != None:
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
            ctx.voice_client.play(player,
                                  after=lambda e: print('Player error: %s' % e)
                                  if e else None)

        url_thumb = f"https://i.ytimg.com/vi/{url.replace('https://www.youtube.com/watch?v=', '')}/maxresdefault.jpg"

        embed = discord.Embed(colour=discord.Colour.blue())
        embed.add_field(
            name="▶️ Now playing",
            value=
            f"[{player.title}]({url}) [<@{ctx.author.id}>]\nJoin VC <#{channel.id}>",
            inline=False)
        if "https://www.youtube.com/watch?v=" in url:
            embed.set_thumbnail(url=url_thumb)
        embed.set_footer(
            text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}.")
        await ctx.send(embed=embed)
        while ctx.voice_client.is_playing() == True:
            await asyncio.sleep(1)
        await asyncio.sleep(1)
        await voice.disconnect()

        embed = discord.Embed(colour=discord.Colour.blue())
        embed.add_field(name="⏹️ Stopped and left",
                        value=f"<#{channel.id}>",
                        inline=False)
        embed.set_footer(
            text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}.")
        await ctx.send(embed=embed)

    else:
        await ctx.send("Please send a URL in the command!")


@bot.command(help="Stop a song from playing in the VC, and make the bot leave!")
async def stop(ctx):
    try:
        channelid = ctx.message.author.voice.channel.id
        await ctx.voice_client.disconnect()
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.add_field(name="⏹️ Stopped and left",
                        value=f"<#{channelid}>",
                        inline=False)
        embed.set_footer(
            text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}.")
        await ctx.send(embed=embed)
    except:
        if ctx.author.voice == None:
            await ctx.send("You are not in a voice channel!")
        else:
            await ctx.send("The bot is not in a voice channel!")


@slash.slash(
    name="help",
    description="Shows all the possible commands and how to use them"
)
async def _help(ctx):  # noqa: C901
    logger.info(f"{ctx.author.name}: /help")
    await ctx.send("Please use `\help` instead.")


def source(o):
    s = inspect.getsource(o).split("\n")
    indent = len(s[0]) - len(s[0].lstrip())
    return "\n".join(i[indent:] for i in s)


source_ = source(discord.gateway.DiscordWebSocket.identify)
source_ = re.sub(r'([\'"]\$browser[\'"]:\s?[\'"]).+([\'"])',
                 r"\1Discord Android\2", source_)
m = ast.parse(source_)

loc = {}
exec(compile(m, "<string>", "exec"), discord.gateway.__dict__, loc)

discord.gateway.DiscordWebSocket.identify = loc["identify"]


bot.load_extension("cogs.moderation")


keep_alive()
bot.run(os.getenv('TOKEN'))
