import subprocess

list_files = subprocess.run(["pip", "install", "googletrans==3.1.0a0"])

import os
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
from discord_slash.utils.manage_commands import create_option, create_choice
import inspect
import string

from commands.credits import show_credits
from commands.define import define
from commands.eight_ball import answer
from commands.embed import create_embed
from commands.encourage import responses_list, response_delete, new_response, sad_words_list
from commands.feedback import create_feedback, list_feedback, delete_feedback
from commands.googlestuff import pls_google, pls_googleimages, pls_translate
from commands.help import help_embeds
from commands.inspire import inspire
from commands.poll import create_poll

logging.basicConfig(level=logging.INFO)

client = commands.Bot(command_prefix=".", intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)
status = cycle([
    '/help help', 'your messages', '/help help', 'Never Gonna Give You Up',
    '/help help', 'try /setup if the slash commands are not working'
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

    if db["responding"] == True:
        if "encouragements" in db.keys():
            options = db["encouragements"]

        if any(word in msg for word in sad_words_list()):
            if "!" not in msg and "." not in msg and "not" not in msg and "n't" not in msg and "aint" not in msg and "never" not in msg:
                await message.reply(random.choice(options))

        mention = f'<@!{client.user.id}>'
        if mention in msg:
            await message.reply("You mentioned me!")

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
        if message.author.id == 721093211577385020:
            await message.reply("Restarting...")
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            await message.reply("You're not my creator, go away.")
            await message.reply("Wait, how did you know about this?")


@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(
                'Thank you for inviting me! If you have any issues, DM Toricane#6391 or join the Discord bot server here: https://discord.gg/QFcMcCQGbU'
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
    print(f'{member} has joined a server!')
    if member.guild.id == 820419188866547712:
        role = "Shark"
        await member.add_roles(discord.utils.get(member.guild.roles,
                                                 name=role))


@client.event
async def on_member_remove(member):
    print(f'{member} has left a server.')


@client.event
async def on_slash_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send(
            f"You don't have the required permissions to run this command, {ctx.author.mention}."
        )
    else:
        await ctx.send(f"ERROR: {error}")
        print(error)


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=next(status)))


@slash.slash(name="inspire",
             description="The bot will send a random inspirational quote")
async def _inspire(ctx):
    await inspire(ctx)


@slash.slash(name="hi", description="The bot will say hello to you")
async def _hi(ctx):
    print(f"{ctx.author.name}: /hi")
    await ctx.defer()
    await ctx.send('Hello!')


@slash.slash(
    name="bye",
    description="The bot will say bye to you",
)
async def _bye(ctx):
    print(f"{ctx.author.name}: /bye")
    await ctx.defer()
    await ctx.send('Bye!')


@slash.slash(
    name="list",
    description="Lists the encouraging messages",
)
async def _list(ctx):
    await ctx.defer()
    print(f"{ctx.author.name}: /list")
    await responses_list(ctx)


@slash.slash(
    name="delete",
    description="Deletes an encouraging message, /list to see",
    options=[
        manage_commands.create_option(
            name="number",
            description=
            "The encouraging message's position in the list that you want to delete, try /list to see",
            option_type=4,
            required=True)
    ],
)
async def _delete(ctx, number):
    print(f"{ctx.author.name}: /delete {number}")
    await ctx.defer()
    await response_delete(ctx, number)


@slash.slash(
    name="new",
    description="Add a new encouraging message",
    options=[
        manage_commands.create_option(name="message",
                                      description="Add it here",
                                      option_type=3,
                                      required=True)
    ],
)
async def _new(ctx, message):
    print(f"{ctx.author.name}: /new {message}")
    await ctx.defer()
    await new_response(ctx, message)


@slash.slash(
    name="run",
    description="Run some code",
    options=[
        manage_commands.create_option(name="code",
                                      description="Add it here",
                                      option_type=3,
                                      required=True)
    ],
)
async def _run(ctx, *, code):
    try:
        if ctx.author.id == 721093211577385020:
            res = eval(code)
            if inspect.isawaitable(res):
                await ctx.send(await res)
            else:
                await ctx.send(await res)
        else:
            await ctx.send("No.")
    except Exception as e:
        print(str(e))


@slash.slash(
    name="avatar",
    description="View someone's avatar picture",
    options=[
        manage_commands.create_option(name="member",
                                      description="Add the member here",
                                      option_type=6,
                                      required=True)
    ],
)
async def _avatar(ctx, member: discord.Member):
    try:
        embed = discord.Embed(colour=discord.Colour.orange())
        url = member.avatar_url
        embed.add_field(name=f'{member}', value='Avatar:', inline=False)
        embed.set_image(url=url)
        await ctx.send(embed=embed)
    except Exception as e:
        print(str(e))


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


@slash.slash(name="kick", description="Kicks a member")
@commands.has_permissions(kick_members=True)
async def _kick(ctx, member: discord.Member, *, reason=None):
    print(f"{ctx.author.name}: /kick {member} {reason}")
    await ctx.defer()
    await member.kick(reason=reason)
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
            option_type=4,
            required=False)
    ],
)
async def _wikipedia(ctx, text, results=1, lines=5):
    print(f"{ctx.author.name}: /wikipedia {text} {lines}")
    await ctx.defer()
    result = wikipedia.search(text, results)
    try:
        end = random.choice(result)
        info = wikipedia.summary(end, lines)
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


@slash.slash(name="joke", description="Gives you a joke")
async def _joke(ctx):
    print(f"{ctx.author.name}: /joke")
    await ctx.defer()
    await ctx.send(pyjokes.get_joke())


@slash.slash(
    name="dm",
    description="DM someone!",
    options=[
        manage_commands.create_option(name="member",
                                      description="Who to DM",
                                      option_type=6,
                                      required=True),
        manage_commands.create_option(name="message",
                                      description="What to say",
                                      option_type=3,
                                      required=True)
    ],
)
async def _dm(ctx, member: discord.Member, message):
    print(f"{ctx.author.name}: /dm {member} {message}")
    await member.send(message)
    await ctx.send(f"The message was successfully sent to {member}", hidden=True)


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
)
async def _google(ctx, text, results=5):
    print(f"{ctx.author.name}: /google {text} {results}")
    await ctx.defer()
    await pls_google(ctx, text, results)


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
)
async def _googleimages(ctx, text, results=5):
    print(f"{ctx.author.name}: /googleimages {text} {results}")
    await ctx.defer()
    await pls_googleimages(ctx, text, results)


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
)
async def _translate(ctx, text, output_lang="en", input_lang=None):
    print(f"{ctx.author.name}: /translate {text} {output_lang} {input_lang}")
    await ctx.defer()
    await pls_translate(ctx, text, output_lang, input_lang)


@slash.slash(
    name="define",
    description="Define any word in English!",
    options=[
        manage_commands.create_option(name="word",
                                      description="Type it here",
                                      option_type=3,
                                      required=True)
    ],
)
async def _define(ctx, word):  # noqa: C901
    await ctx.defer()
    print(f"{ctx.author.name}: /define {word}")
    await define(ctx, word)


@slash.slash(
    name="reverse",
    description="Reverses your text",
    options=[
        manage_commands.create_option(name="text",
                                      description="Type it here",
                                      option_type=3,
                                      required=True)
    ],
)
async def _reverse(ctx, text):
    await ctx.defer()
    await ctx.send(text[::-1])


@slash.slash(
    name="reciprocal",
    description="Sends a reciprocal of a fraction",
    options=[
        manage_commands.create_option(name="fraction",
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


@slash.slash(
    name="nick",
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
)
@commands.has_permissions(manage_nicknames=True)
async def _nick(ctx, member: discord.Member, nick):
    await ctx.defer()
    try:
        await member.edit(nick=nick)
        await ctx.send(f'Nickname was changed for {member.mention}.')
    except Exception as e:
        print(str(e))
        await ctx.send("ERROR: is the member in the server?")


@slash.slash(name="addrole", description="Adds a role")
@commands.has_permissions(manage_roles=True)
async def _addrole(ctx, member: discord.Member, role: discord.Role):
    await ctx.defer()
    await member.add_roles(role)
    await ctx.send(f"{member.mention} got the {role} role.")


@slash.slash(
    name="removerole",
    description="Removes a role",
)
@commands.has_permissions(manage_roles=True)
async def _removerole(ctx, member: discord.Member, role: discord.Role):
    await ctx.defer()
    await member.remove_roles(role)
    await ctx.send(f"{member.mention} lost the {role} role.")


@slash.slash(
    name="feedback",
    description="Give feedback!",
    options=[
        manage_commands.create_option(name="feedback",
                                      description="Type member here",
                                      option_type=3,
                                      required=True)
    ],
)
async def _feedback(ctx, feedback):
    print(f"{ctx.author.name}: /feedback {feedback}")
    await ctx.defer()
    await create_feedback(ctx, feedback)


@slash.slash(
    name="feedbacklist",
    description="List feedback!",
)
async def _feedbacklist(ctx):
    print(f"{ctx.author.name}: /feedbacklist")
    await ctx.defer()
    await list_feedback(ctx)


@slash.slash(
    name="feedbackclear",
    description="Clears all of the feedback or the chosen one",
    options=[
        manage_commands.create_option(
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


@slash.slash(
    name="poll",
    description="Create a poll!",
    options=[
        manage_commands.create_option(name="question",
                                      description="What is your question?",
                                      option_type=3,
                                      required=True),
        manage_commands.create_option(
            name="choices",
            description="What are the choices? Separate them using /.",
            option_type=3,
            required=True),
        manage_commands.create_option(name="mention",
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


@slash.slash(name="ban", description="Bans a member")
@commands.has_permissions(ban_members=True)
async def _ban(ctx, member: discord.Member, *, reason=None):
    print(f"{ctx.author.name}: /ban {member} {reason}")
    await member.ban(reason=reason)
    await ctx.defer()
    await ctx.send(f"Banned {member.mention} because {reason}.")


@slash.slash(
    name="unban",
    description="Unbans a member",
    options=[
        manage_commands.create_option(name="member",
                                      description="Add the member name here",
                                      option_type=3,
                                      required=True)
    ],
)
@commands.has_permissions(ban_members=True)
async def _unban(ctx, argone):
    print(f"{ctx.author.name}: /unban {argone}")
    await ctx.defer()
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = argone.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name,
                                               member_discriminator):
            await ctx.guild.unban(user)
            person = f"{user.name}#{user.discriminator}"
            await ctx.send(f"Unbanned {person}.")
            return


@slash.slash(
    name="hello",
    description="Say hello to someone",
    options=[
        manage_commands.create_option(
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
        await ctx.message.delete()


@slash.slash(
    name="say",
    description="Make the bot say anything",
    options=[
        manage_commands.create_option(name="text",
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


@slash.slash(
    name="ping",
    description="This returns the bot latency",
)
async def _ping(ctx):
    print(f"{ctx.author.name}: /ping")
    await ctx.defer()
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms.')


@slash.slash(
    name="8ball",
    description="Returns yes or no to your question",
    options=[
        manage_commands.create_option(name="question",
                                      description="Enter your question here",
                                      option_type=3,
                                      required=True)
    ],
)
async def _8ball(ctx, question):
    print(f"{ctx.author.name}: /8ball {question}")
    await ctx.defer()
    await ctx.send(answer())


@slash.slash(
    name="invite",
    description="Shows the invite link for the bot",
)
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


@slash.slash(
    name="perseverance",
    description="Shows the profile picture of Perseverance",
)
async def _perseverance(ctx):
    print(f"{ctx.author.name}: /perseverance")
    await ctx.send("Profile Picture:")
    await ctx.send(file=discord.File('preservation.png'))


@slash.slash(
    name="password",
    description="Returns yes or no to your question",
    options=[
        manage_commands.create_option(name="length",
                                      description="How long should your password be?",
                                      option_type=4,
                                      required=True),
        manage_commands.create_option(name="dm",
                                      description="Should I DM the password? Default False",
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


@slash.slash(
    name="credits",
    description="Shows the credits",
)
async def _credits(ctx):
    print(f"{ctx.author.name}: /credits")
    await ctx.defer()
    await show_credits(ctx)


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
)
async def _help(ctx, command):  # noqa: C901
    print(f"{ctx.author.name}: /help {command}")
    await ctx.defer()
    await help_embeds(ctx, command)


keep_alive()
client.run(os.getenv('TOKEN'))
