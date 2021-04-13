import subprocess

list_files = subprocess.run(["pip", "install", "googletrans==3.1.0a0"])

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
import pyjokes
from discord_slash.utils.manage_commands import create_option, create_choice
import inspect
import string
from discord.flags import Intents

from asteval import Interpreter
aeval = Interpreter()

from cmds.credits import show_credits
from cmds.define import pls_define
from cmds.eight_ball import answer
from cmds.embed import create_embed
from cmds.feedback import create_feedback, list_feedback, delete_feedback
from cmds.googlestuff import pls_google, pls_googleimages, pls_translate
from cmds.help import help_embeds2
from cmds.inspire import inspired
from cmds.poll import create_poll
from cmds.morse import encrypt, decrypt
from cmds.reply import maybe_reply as meply

logging.basicConfig(level=logging.INFO)

client = commands.Bot(command_prefix=".", intents=Intents.all(), help_command=None)
slash = SlashCommand(client, sync_commands=True)
status = cycle([
    '/help or .help', 'your messages', '/help or .help', 'Never Gonna Give You Up',
    '/help or .help', 'hello there!'
])

guild_ids = db["id"]

@client.event
async def on_ready():
    change_status.start()
    print('We have logged in as {0.user}'.format(client))
    timestamp = datetime.datetime.now()
    print(timestamp.strftime(r"%A, %b %d, %Y, %I:%M %p UTC"))
    print(guild_ids)


@client.event
async def on_message(message):

    msg = message.content.lower()

    if msg == "/setup":
        if message.author.id == 721093211577385020:
            print('/setup')
            ido = message.guild.id
            if ido not in db["id"]:
                ids = db["id"]
                ids.append(ido)
                db["id"] = ids
                print(db["id"])
                await message.reply(
                    "Server has been set up! The bot is restarting! If the error persists, contact Toricane#0001 in Discord to restart the bot!"
                )
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                await message.reply(
                    "Server already setup! The bot is restarting! If the error persists, contact Toricane#0001 in Discord to restart the bot!"
                )
                os.execl(sys.executable, sys.executable, *sys.argv)
    if msg == "/restart" or msg == ".restart":
        if message.author.id == 721093211577385020:
            await message.add_reaction('🆗')
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            await message.add_reaction('<:no:828741445069963274>')

    await client.process_commands(message)


@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(
                'Thank you for inviting me! If you have any issues, DM Toricane#0001 or join the Discord bot server here: https://discord.gg/QFcMcCQGbU'
            )
        break


@client.event
async def on_guild_remove(guild):
    ido = int(guild.id)
    ids = db["id"]
    ids.remove(ido)
    db["id"] = ids
    print(db["id"])


@client.event
async def on_member_join(member):
    print(f'{member} has joined {member.guild.name}')
    if member.guild.id == 820419188866547712:
        role = "Shark"
        await member.add_roles(discord.utils.get(member.guild.roles,
                                                 name=role))


@client.event
async def on_member_remove(member):
    print(f'{member} has left {member.guild.name}')


@client.event
async def on_slash_command_error(ctx, error):
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


@client.event
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
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=next(status)))



@client.command()
async def inspire(ctx):
    print(f"{ctx.author.name}: .inspire")
    quoted = await inspired(ctx)
    await meply(ctx, quoted)

@slash.slash(name="inspire",
             description="The bot will send a random inspirational quote")
async def _inspire(ctx):
    await ctx.defer()
    print(f"{ctx.author.name}: /inspire")
    quoted = await inspired(ctx)
    await meply(ctx, quoted)



@client.command()
async def hi(ctx):
    await meply(ctx, "Hello!")

@slash.slash(name="hi", description="The bot will say hello to you")
async def _hi(ctx):
    await ctx.defer()
    print(f"{ctx.author.name}: /hi")
    await ctx.send('Hello!')



@client.command()
async def bye(ctx):
    print(f"{ctx.author.name}: .bye")
    await meply(ctx, "Bye!")

@slash.slash(name="bye", description="The bot will say bye to you")
async def _bye(ctx):
    print(f"{ctx.author.name}: /bye")
    await ctx.defer()
    await ctx.send('Bye!')



@client.command()
async def run(ctx, *, code):
    print(f"{ctx.author.name}: .run {code}")
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
        print(str(e))

@slash.slash(
    name="run",
    description="Run some code",
    options=[
        create_option(name="code",
                                      description="Add it here",
                                      option_type=3,
                                      required=True)
    ],
)
async def _run(ctx, code):
    print(f"{ctx.author.name}: /run {code}")
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
        print(str(e))



@client.command(aliases=["pfp"])
async def avatar(ctx, member: discord.Member):
    print(f"{ctx.author.name}: .avatar {member}")
    try:
        embed = discord.Embed(colour=discord.Colour.orange())
        url = member.avatar_url
        embed.add_field(name=f'{member}', value='Avatar:', inline=False)
        embed.set_image(url=url)
        await ctx.send(embed=embed)
    except Exception as e:
        print(str(e))

@slash.slash(
    name="avatar",
    description="View someone's avatar picture",
    options=[
        create_option(name="member",
                                      description="Add the member here",
                                      option_type=6,
                                      required=True)
    ],
)
async def _avatar(ctx, member: discord.Member):
    print(f"{ctx.author.name}: /avatar {member}")
    try:
        embed = discord.Embed(colour=discord.Colour.orange())
        url = member.avatar_url
        embed.add_field(name=f'{member}', value='Avatar:', inline=False)
        embed.set_image(url=url)
        await ctx.send(embed=embed)
    except Exception as e:
        print(str(e))



@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=5):
    print(f"{ctx.author.name}: .purge {amount}")
    amount = int(amount)
    if amount < 100:
        await ctx.send("Removing messages...")
        await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(f"Removed {amount} messages.")
        await asyncio.sleep(5)
        await msg.delete()
    else:
        msg = await ctx.send(f"React to this message with 👍 to delete {amount} messages.")
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '👍'

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('Timed out.')
        else:
            await ctx.send("Removing messages...")
            await ctx.channel.purge(limit=amount + 3)
            msg = await ctx.send(f"Removed {amount} messages.")
            await asyncio.sleep(5)
            await msg.delete()

@slash.slash(name="purge", description="Delete messages")
@commands.has_permissions(manage_messages=True)
async def _purge(ctx, amount=5):
    print(f"{ctx.author.name}: /purge {amount}")
    await ctx.defer()
    amount = int(amount)
    await ctx.send("Removing messages...")
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.channel.send(f"Removed {amount} messages.")
    await asyncio.sleep(5)
    await msg.delete()



@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    print(f"{ctx.author.name}: .kick {member} {reason}")
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member} because {reason}.")

@slash.slash(name="kick", description="Kicks a member")
@commands.has_permissions(kick_members=True)
async def _kick(ctx, member: discord.Member, *, reason=None):
    print(f"{ctx.author.name}: /kick {member} {reason}")
    await ctx.defer()
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member} because {reason}.")



@client.command(aliases=["wiki"], description="Searches for something on wikipedia")
async def wikipedia(ctx, text: str, results: int=1, lines: int=5):
    print(f"{ctx.author.name}: .wikipedia {text} {results} {lines}")
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
        print(e)
        await ctx.send(
            "ERROR, there may be too many to choose from, or a module error.")
        await ctx.send(f"ERROR: {e}")

@slash.slash(
    name="wikipedia",
    description="Searches for something on Wikipedia",
    options=[
        create_option(
            name="text",
            description="What do you want to search?",
            option_type=3,
            required=True),
        create_option(
            name="results",
            description=
            "How many results should you randomly recieve 1 result from? Default is 5.",
            option_type=3,
            required=False),
        create_option(
            name="lines",
            description="How many lines do you want? Default is 10.",
            option_type=4,
            required=False)
    ],
)
async def _wikipedia(ctx, text, results=1, lines=5):
    print(f"{ctx.author.name}: /wikipedia {text} {results} {lines}")
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
        print(e)
        await ctx.send(
            "ERROR, there may be too many to choose from, or a module error.")
        await ctx.send(f"ERROR: {e}")



@client.command()
async def joke(ctx):
    print(f"{ctx.author.name}: .joke")
    await ctx.send(pyjokes.get_joke())

@slash.slash(name="joke", description="Gives you a joke")
async def _joke(ctx):
    print(f"{ctx.author.name}: /joke")
    await ctx.defer()
    await ctx.send(pyjokes.get_joke())



@client.command()
async def google(ctx, text, results=5):
    print(f"{ctx.author.name}: .google {text} {results}")
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
    print(f"{ctx.author.name}: /google {text} {results}")
    await ctx.defer()
    await pls_google(ctx, text, results)



@client.command(aliases=["gpics"])
async def googleimages(ctx, text, results: int=5):
    print(f"{ctx.author.name}: /googleimages {text} {results}")
    await pls_googleimages(ctx, text, results)

@slash.slash(
    name="googleimages",
    description="Search images on Google!",
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
async def _googleimages(ctx, text, results=5):
    print(f"{ctx.author.name}: /googleimages {text} {results}")
    await ctx.defer()
    await pls_googleimages(ctx, text, results)



@client.command()
async def translate(ctx, text, output_lang="en", input_lang=None):
    print(f"{ctx.author.name}: /translate {text} {output_lang} {input_lang}")
    await pls_translate(ctx, text, output_lang, input_lang)

@slash.slash(
    name="translate",
    description="Translate anything on Google Translate!",
    options=[
        create_option(name="text",
                                      description="Search it here",
                                      option_type=3,
                                      required=True),
        create_option(
            name="output_lang",
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
    print(f"{ctx.author.name}: /translate {text} {output_lang} {input_lang}")
    await ctx.defer()
    await pls_translate(ctx, text, output_lang, input_lang)



@client.command(aliases=["def"])
async def define(ctx, word):
    print(f"{ctx.author.name}: .define {word}")
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
    print(f"{ctx.author.name}: /define {word}")
    await pls_define(ctx, word)



@client.command(aliases=["r", "rev"])
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



@client.command(aliases=["reci"])
async def reciprocal(ctx, *, fraction):
    print(f"{ctx.author.name}: .reciprocal {fraction}")
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
    print(f"{ctx.author.name}: /reciprocal")
    await ctx.defer()
    fr1, fr2 = fraction.split("/")
    await ctx.send(f"{fr2}/{fr1}")



@client.command(aliases=["nickname"])
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, *, nick):
    try:
        await member.edit(nick=nick)
        await ctx.send(f'Nickname was changed for {member.mention}.')
    except Exception as e:
        print(str(e))
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
        print(str(e))
        await ctx.send("ERROR: is the member in the server?")



@client.command(aliases=["ar"])
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member, role: discord.Role):
    print(f"{ctx.author.name}: .addrole {member} {role}")
    await member.add_roles(role)
    await ctx.send(f"{member.mention} got the {role} role.")

@slash.slash(name="addrole", description="Adds a role")
@commands.has_permissions(manage_roles=True)
async def _addrole(ctx, member: discord.Member, role: discord.Role):
    await ctx.defer()
    await member.add_roles(role)
    await ctx.send(f"{member.mention} got the {role} role.")



@client.command(aliases=["rr"])
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, member: discord.Member, role: discord.Role):
    print(f"{ctx.author.name}: .removerole {member} {role}")
    await member.remove_roles(role)
    await ctx.send(f"{member.mention} lost the {role} role.")

@slash.slash(name="removerole", description="Removes a role")
@commands.has_permissions(manage_roles=True)
async def _removerole(ctx, member: discord.Member, role: discord.Role):
    await ctx.defer()
    await member.remove_roles(role)
    await ctx.send(f"{member.mention} lost the {role} role.")



@client.command(aliases=["fb"])
async def feedback(ctx, *, feedback):
    await ctx.defer()
    print(f"{ctx.author.name}: .feedback {feedback}")
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
    print(f"{ctx.author.name}: /feedback {feedback}")
    await ctx.defer()
    await create_feedback(ctx, feedback)



@client.command(aliases=["fblist"])
async def feedbacklist(ctx):
    print(f"{ctx.author.name}: .feedbacklist")
    await ctx.send("List of feedbacks:")
    await list_feedback(ctx)

@slash.slash(name="feedbacklist", description="List feedback!")
async def _feedbacklist(ctx):
    print(f"{ctx.author.name}: /feedbacklist")
    await ctx.defer()
    await ctx.send("List of feedbacks:")
    await list_feedback(ctx)



@client.command(aliases=["fbclear"])
async def feedbackclear(ctx, number=None):
    print(f"{ctx.author.name}: /feedbackclear {number}")
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
    print(f"{ctx.author.name}: /feedbackclear {number}")
    await ctx.defer()
    await delete_feedback(ctx, number)



@client.command()
async def poll(ctx, question, choices, mention=None):  # noqa: C901
    print(f"{ctx.author.name}: /poll {question} {choices} {mention}")
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
    print(f"{ctx.author.name}: /poll {question} {choices} {mention}")
    await ctx.defer()
    try:
        await create_poll(ctx, question, choices, mention)
    except Exception as e:
        print(str(e))



@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    print(f"{ctx.author.name}: /ban {member} {reason}")
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention} because {reason}.")

@slash.slash(name="ban", description="Bans a member")
@commands.has_permissions(ban_members=True)
async def _ban(ctx, member: discord.Member, reason=None):
    print(f"{ctx.author.name}: /ban {member} {reason}")
    await member.ban(reason=reason)
    await ctx.defer()
    await ctx.send(f"Banned {member.mention} because {reason}.")



@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, member):
    print(f"{ctx.author.name}: .unban {member}")
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name,
                                               member_discriminator):
            await ctx.guild.unban(user)
            person = f"{user.name}#{user.discriminator}"
            await ctx.send(f"Unbanned {person}.")
            return

@slash.slash(
    name="unban",
    description="Unbans a member",
    options=[
        create_option(name="member",
                                      description="Add the member name here",
                                      option_type=3,
                                      required=True)
    ],
)
@commands.has_permissions(ban_members=True)
async def _unban(ctx, member):
    print(f"{ctx.author.name}: /unban {member}")
    await ctx.defer()
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name,
                                               member_discriminator):
            await ctx.guild.unban(user)
            person = f"{user.name}#{user.discriminator}"
            await ctx.send(f"Unbanned {person}.")
            return



@client.command()
async def hello(ctx, *, name):
    print(f"{ctx.author.name}: .hello {name}")
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
        create_option(
            name="name",
            description='Put either "there" or the name',
            option_type=3,
            required=True)
    ],
)
async def _hello(ctx, name):
    await ctx.defer()
    print(f"{ctx.author.name}: /hello {name}")
    name = name.capitalize()
    if name == "There":
        await ctx.send("General Kenobi!")
    else:
        await ctx.send(f"Hello {name}!")



@client.command()
async def say(ctx, *, text):
    print(f"{ctx.author.name}: .say {text}")
    await ctx.send(text)
    await ctx.message.delete()

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
    print(f"{ctx.author.name}: /say {text}")
    msg = await ctx.send(text)
    await msg.delete()
    await ctx.channel.send(text)



@client.command()
async def ping(ctx):
    print(f"{ctx.author.name}: /ping")
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms.')

@slash.slash(name="ping", description="This returns the bot latency")
async def _ping(ctx):
    print(f"{ctx.author.name}: .ping")
    await ctx.defer()
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms.')



@client.command(aliases=["8ball"])
async def eightball(ctx, *, question):
    print(f"{ctx.author.name}: .8ball {question}")
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
    print(f"{ctx.author.name}: /8ball {question}")
    await ctx.defer()
    await ctx.send(answer())



@client.command()
async def invite(ctx):
    print(f"{ctx.author.name}: .invite")
    embed = discord.Embed(colour=discord.Colour.orange())
    embed.add_field(
        name='Invite the bot!',
        value=
        'Click [here](https://discord.com/api/oauth2/authorize?client_id=811277990913769523&permissions=3691244614&scope=bot%20applications.commands)',
        inline=False)
    await ctx.send(embed=embed)

@slash.slash(name="invite", description="Shows the invite link for the bot")
async def _invite(ctx):
    print(f"{ctx.author.name}: /invite")
    embed = discord.Embed(colour=discord.Colour.orange())
    embed.add_field(
        name='Invite the bot!',
        value=
        'Click [here](https://discord.com/api/oauth2/authorize?client_id=811277990913769523&permissions=3691244614&scope=bot%20applications.commands)',
        inline=False)
    await ctx.defer()
    await ctx.send(embed=embed)



@client.command()
async def perseverance(ctx):
    print(f"{ctx.author.name}: .perseverance")
    await ctx.send("Profile Picture:")
    await ctx.send(file=discord.File('preservation.png'))

@slash.slash(
    name="perseverance",
    description="Shows the profile picture of Perseverance",
)
async def _perseverance(ctx):
    print(f"{ctx.author.name}: /perseverance")
    await ctx.send("Profile Picture:")
    await ctx.send(file=discord.File('preservation.png'))



@client.command(aliases=["pw", "pass"])
async def password(ctx, length: int, dm=False):
    print(f"{ctx.author.name}: .password {length} {dm}")
    if dm == "true" or dm == "yes":
        dm = True
    else:
        dm=False
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
        await ctx.send("Your password was successfully DM'ed to you.", hidden=True)

@slash.slash(
    name="password",
    description="Gives you a strong password",
    options=[
        create_option(name="length",
                                      description="How long should your password be?",
                                      option_type=4,
                                      required=True),
        create_option(name="dm",
                                      description="Should I DM the password? Default True",
                                      option_type=5,
                                      required=False)
    ]
)
async def _password(ctx, length, dm=False):
    print(f"{ctx.author.name}: /password {length} {dm}")
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
        await ctx.send("Your password was successfully DM'ed to you.", hidden=True)



@client.command(aliases=["btt"])
async def binarytotext(ctx, *, text):
    ascii_string = "".join([chr(int(binary, 2)) for binary in text.split(" ")])
    await ctx.reply(f"```py\n{ascii_string}```")

@slash.slash(
    name="binarytotext",
    description="Get text from binary",
    options=[
        create_option(name="text",
                                      description="Your binary code",
                                      option_type=3,
                                      required=True)
    ]
)
async def binaryToText(ctx, text):
    await ctx.defer()
    ascii_string = "".join([chr(int(binary, 2)) for binary in text.split(" ")])
    await ctx.send(f"```py\n{ascii_string}```")



@client.command(aliases=["ttb"])
async def texttobinary(ctx, *, text):
    res = ' '.join(format(ord(i), '08b') for i in text)
    await ctx.reply(f"```py\n{res}```")

@slash.slash(
    name="texttobinary",
    description="Get binary from text",
    options=[
        create_option(name="text",
                                      description="Your binary code",
                                      option_type=3,
                                      required=True)
    ]
)
async def _texttobinary(ctx, text):
    await ctx.defer()
    res = ' '.join(format(ord(i), '08b') for i in text)
    await ctx.send(f"```py\n{res}```")



@client.command(aliases=["ttm"])
async def texttomorse(ctx, *, message):
    result = encrypt(message.upper())
    await ctx.reply(f"```py\n{result}```")

@slash.slash(
    name="texttomorse",
    description="Get morse code from text",
    options=[
        create_option(name="text",
                                      description="Your binary code",
                                      option_type=3,
                                      required=True)
    ]
)
async def _texttomorse(ctx, message):
    result = encrypt(message.upper())
    await ctx.send(f"```py\n{result}```")



@client.command(aliases=["mtt"])
async def morsetotext(ctx, *, message):
    result = decrypt(message)
    await ctx.reply(f"```py\n{result}```")

@slash.slash(
    name="morsetotext",
    description="Get text from morse code",
    options=[
        create_option(name="text",
                                      description="Your binary code",
                                      option_type=3,
                                      required=True)
    ]
)
async def _morsetotext(ctx, message):
    result = decrypt(message)
    await ctx.send(f"```py\n{result.lower()}```")



@client.command()
async def embed(ctx, title, text, color="default"):
    print(f"{ctx.author.name}: .embed {title} {text} {color}")
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
    print(f"{ctx.author.name}: /embed {title} {text} {color}")
    await ctx.defer()
    await create_embed(ctx, title, text, color)



@client.command(aliases=["info", "about"])
async def credits(ctx):
    print(f"{ctx.author.name}: .credits")
    await show_credits(ctx)

@slash.slash(name="credits", description="Shows the credits")
async def _credits(ctx):
    print(f"{ctx.author.name}: /credits")
    await ctx.defer()
    await show_credits(ctx)



@client.command(aliases=["h"])
async def help(ctx, *, command=None):
    print(f"{ctx.author.name}: .help {command}")
    await help_embeds2(ctx, command)

@slash.slash(
    name="help",
    description="Shows all the possible commands and how to use them",
    options=[
        create_option(
            name="command",
            description=
            'Will show the specific command that you want to know about, or type "help" for all the commands',
            option_type=3,
            required=False)
    ],
)
async def _help(ctx, command=None):  # noqa: C901
    print(f"{ctx.author.name}: /help {command}")
    await ctx.defer()
    await help_embeds2(ctx, command)


keep_alive()
client.run(os.getenv('TOKEN'))
