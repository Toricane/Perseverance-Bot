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

logging.basicConfig(level=logging.INFO)

client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)
status = cycle([
    '/help', 'your messages', '/help', 'Never Gonna Give You Up', '/help',
    'try /setup if the slash commands are not working'
])

#db["id"] = [788578597488427008, 764683397528158259]
guild_ids = db["id"]

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
        await ctx.respond()
        await ctx.send(
            'Command was not found. Be sure you did not make a typo and try again.'
        )
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=2)


@client.event
async def on_message(message):

    msg = message.content

    if db["responding"] == True:
        options = starter_encouragements
        if "encouragements" in db.keys():
            options = options + db["encouragements"]

        if any(word in msg for word in sad_words):
            if "!" not in msg and "." not in msg and "not" not in msg and "n't" not in msg and "aint" not in msg and "never" not in msg:
                await message.reply(random.choice(options))

    if msg == "/setup":
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


@slash.slash(name="inspire", description="The bot will send a random inspirational quote", guild_ids=guild_ids)
async def _inspire(ctx):
    quote = await get_quote()
    await ctx.respond()
    await ctx.send(quote)


@slash.slash(name="hi", description="The bot will say hello to you", guild_ids=guild_ids)
async def _hi(ctx):
    await ctx.respond()
    await ctx.send('Hello!')


@slash.slash(name="bye", description="The bot will say bye to you", guild_ids=guild_ids)
async def _bye(ctx):
    await ctx.respond()
    await ctx.send('Bye!')


@slash.slash(name="list", description="Lists the encouraging messages", guild_ids=guild_ids)
async def _list(ctx):
    encouragements = []
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
    await ctx.respond()
    await ctx.send(encouragements)


@slash.slash(name="delete",
             description="Deletes an encouraging message, /list to see",
             options=[
                 manage_commands.create_option(
                     name="index",
                     description="The encouraging message's position in the list that you want to delete, try /list to see",
                     option_type=3,
                     required=True)
             ],
             guild_ids=guild_ids)
async def _delete(ctx, argone):
    encouragements = []
    if "encouragements" in db.keys():
        index = int(argone) - 1
        delete_encouragment(index)
        encouragements = db["encouragements"]
    await ctx.respond()
    await ctx.send(encouragements)


@slash.slash(name="new",
             description="Add a new encouraging message",
             options=[
                 manage_commands.create_option(
                     name="message",
                     description="Add it here",
                     option_type=3,
                     required=True)
             ],
             guild_ids=guild_ids)
async def _new(ctx, argone):
    encouraging_message = argone
    update_encouragements(encouraging_message)
    await ctx.respond()
    await ctx.send(f'New encouraging message added: {encouraging_message}')


@slash.slash(name="clear", description="Delete messages", guild_ids=guild_ids)
@commands.has_permissions(manage_messages=True)
async def _clear(ctx, amount=5):
    amount = int(amount)
    await ctx.channel.purge(limit=amount + 1)
    await ctx.respond()
    await ctx.send(f"Removed {amount} messages.")
    await asyncio.sleep(3)
    await ctx.channel.purge(limit=2)


@slash.slash(name="kick", description="Kicks a member", guild_ids=guild_ids)
@commands.has_permissions(kick_members=True)
async def _kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.respond()
    await ctx.send(f"Kicked {member} because {reason}.")


@slash.slash(name="ban", description="Bans a member", guild_ids=guild_ids)
@commands.has_permissions(ban_members=True)
async def _ban(ctx, member: discord.Member, *, reason=None):
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


@slash.slash(name="credits",
             description="Shows the credits",
             guild_ids=guild_ids)
async def _credits(ctx):
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
async def _help(ctx, argone):
    embed = discord.Embed(colour=discord.Colour.orange())
    arg = str(argone).lower()
    if arg == "ping":
        embed.set_author(name='Help for /ping')
        embed.add_field(name='/ping', value='Returns "Pong!"', inline=False)
        await ctx.respond()
        await ctx.send(embed=embed)

    elif arg == "inspire":
        embed.add_field(name='/inspire',
                        value='send a random quote from https://zenquotes.io/',
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
            'Only lists the encouragements that have been added from .new.',
            inline=False)
        embed.add_field(
            name='/delete number',
            value='Deletes the corsending encouraging message listed in .list.',
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

        await ctx.respond()
        await ctx.send(embed=embed)


@slash.slash(name="perseverance", description="Shows a photo of Perseverance", guild_ids=guild_ids)
async def _perseverance(ctx):
    await ctx.respond()
    await ctx.send(file=discord.File('perseverance.jpeg'))


keep_alive()
client.run(os.getenv('TOKEN'))
