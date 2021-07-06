#! /usr/bin/python3

from dotenv import load_dotenv
load_dotenv()

import os
import discord
from discord.ext import commands, tasks
import asyncio
from itertools import cycle
from discord_slash import SlashCommand
import sys
import datetime
from discord_slash.utils.manage_commands import create_option
from discord.flags import Intents
import inspect
from discord.utils import get
import youtube_dl
from pretty_help import PrettyHelp

from cogwatch import Watcher

from cmds.feedback import create_feedback, list_feedback, delete_feedback
from cmds.ytactivity import group_say

from log import used, error

ending_note = "Type \help command for more info on a command.\nYou can also type \help category for more info on a category.\nCategories are cAsE sEnSiTiVe.\n\nThe bot also has / commands, try them out!"

bot = commands.Bot(command_prefix="\\",
                   intents=Intents.all(),
                   case_insensitive=True,
                   help_command=PrettyHelp(
                       color=discord.Colour.orange(),
                       page_left="◀️",
                       page_right="▶️",
                       remove="❌",
                       no_category="Miscellaneous",
                       ending_note=ending_note
                   ))
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)
servers = len(bot.guilds)
status = cycle([
    '\\help', 'your messages', '\\help',
    'Never Gonna Give You Up', '\\help', 'hello there!',
    '\\help', f'{servers} servers'
])

guild_ids = [824862561328562176]


@bot.event
async def on_ready():
    change_status.start()
    print(f'We have logged in as {bot.user}')
    used(f'We have logged in as {bot.user}')
    timestamp = datetime.datetime.now()
    print(timestamp.strftime(r"%A, %b %d, %Y, %I:%M %p PDT"))
    used(timestamp.strftime(r"%A, %b %d, %Y, %I:%M %p PDT"))
    print(f"guild_ids={guild_ids}")
    used(f"guild_ids={guild_ids}")
    print(f"In {len(bot.guilds)} servers")
    used(f"In {len(bot.guilds)} servers")
    with open("/home/pi/Desktop/DiscordBots/Perseverance-Bot/guilds.txt", "w") as f:
        f.write(f"{len(bot.guilds)}")
    with open("/home/pi/Desktop/DiscordBots/Perseverance-Bot/guilds.txt", "r") as f:
        servers = f.read()
        global status
        status = cycle([
            '\\help', 'your messages', '\\help',
            'Never Gonna Give You Up', '\\help', 'hello there!',
            '\\help', f'{servers} servers'
        ])
    watcher = Watcher(bot, path="/home/pi/Desktop/DiscordBots/Perseverance-Bot/cogs", preload=True)
    await watcher.start()

@bot.event
async def on_message(message):

    msg = message.content.lower()

    if msg == "/restart" or msg == "\\restart":
        if message.author.id == 721093211577385020:
            await message.add_reaction('🆗')
            await bot.change_presence(status=discord.Status.invisible)
            await asyncio.sleep(1)
            os.system("python3 main.py")
            sys.exit(0)
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
    with open("/home/pi/Desktop/DiscordBots/Perseverance-Bot/guilds.txt", "w") as f:
        f.write(f"{len(bot.guilds)}")


@bot.event
async def on_guild_remove(guild):
    with open("/home/pi/Desktop/DiscordBots/Perseverance-Bot/guilds.txt", "w") as f:
        f.write(f"{len(bot.guilds)}")


@bot.event
async def on_member_join(member):
    used(f'{member} has joined {member.guild.name}')
    if member.guild.id == 820419188866547712:
        role = "Shark"
        await member.add_roles(discord.utils.get(member.guild.roles,
                                                 name=role))


@bot.event
async def on_member_remove(member):
    used(f'{member} has left {member.guild.name}')


@bot.event
async def on_slash_command_error(ctx, ex):
    if isinstance(ex, discord.ext.commands.errors.MissingPermissions):
        perms_missing = error.missing_perms
        perms_missing = f"{perms_missing}"
        perms_missing = perms_missing.strip("[]'")
        perms_missing = perms_missing.replace("_", " ")
        await ctx.send(
            f"You don't have `{perms_missing}` permissions to run this command, {ctx.author.mention}."
        )
    else:
        raise ex


@bot.event
async def on_command_error(ctx, ex):
    if isinstance(ex, discord.ext.commands.errors.MissingPermissions):
        perms_missing = ex.missing_perms
        perms_missing = f"{perms_missing}"
        perms_missing = perms_missing.strip("[]'")
        perms_missing = perms_missing.replace("_", " ")
        await ctx.send(
            f"You don't have {perms_missing} permissions to run this command, {ctx.author.mention}."
        )
    elif isinstance(ex, commands.errors.BadArgument):
        await ctx.send("Please format your message properly.")
    elif isinstance(ex, commands.errors.CommandNotFound):
        pass
    else:
        await ctx.send("There was an unexpected error, and the bot developer has been notified.")
        error(ex)
        channel = await bot.fetch_channel('852959272399798323')
        guild = ctx.guild.name
        command = ctx.command
        embed = discord.Embed(colour=discord.Colour.orange())
        embed.add_field(name=f"ERROR running `{command}` in guild `{guild}`", value=f"{ex}", inline=False)
        await channel.send(embed=embed)


@tasks.loop(seconds=15)
async def change_status():
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=next(status)))


@bot.command(aliases=["l"])
async def load(ctx, extension=None):
    if ctx.author.id == 721093211577385020:
        if extension == None:
            try:
                for filename in os.listdir("/home/pi/Desktop/DiscordBots/Perseverance-Bot/cogs"):
                    if filename.endswith(".py"):
                        bot.load_extension(f"cogs.{filename[:-3]}")
                await ctx.send("Successfully loaded all extensions.")
            except Exception as e:
                await ctx.send(f"{e}")
        else:
            bot.load_extension(f"cogs.{extension}")
            await ctx.send(f"Successfully loaded `cogs/{extension}.py`")
    else:
        await ctx.message.add_reaction('<:no:828741445069963274>')


@bot.command(aliases=["ul"])
async def unload(ctx, extension=None):
    if ctx.author.id == 721093211577385020:
        if extension == None:
            try:
                for filename in os.listdir("/home/pi/Desktop/DiscordBots/Perseverance-Bot/cogs"):
                    if filename.endswith(".py"):
                        bot.unload_extension(f"cogs.{filename[:-3]}")
                await ctx.send("Successfully unloaded all extensions.")
            except Exception as e:
                await ctx.send(f"{e}")
        else:
            bot.unload_extension(f"cogs.{extension}")
            await ctx.send(f"Successfully unloaded `cogs/{extension}.py`")
    else:
        await ctx.message.add_reaction('<:no:828741445069963274>')


@bot.command(aliases=["rl"])
async def reload(ctx, extension=None):
    if ctx.author.id == 721093211577385020:
        if extension == None:
            try:
                for filename in os.listdir("/home/pi/Desktop/DiscordBots/Perseverance-Bot/cogs"):
                    if filename.endswith(".py"):
                        bot.unload_extension(f"cogs.{filename[:-3]}")
            except Exception as e:
                await ctx.send(f"{e}")
            try:
                for filename in os.listdir("/home/pi/Desktop/DiscordBots/Perseverance-Bot/cogs"):
                    if filename.endswith(".py"):
                        bot.load_extension(f"cogs.{filename[:-3]}")
            except Exception as e:
                await ctx.send(f"{e}")
            await ctx.send("Successfully reloaded all extensions.")
        else:
            try:
                bot.unload_extension(f"cogs.{extension}")
                bot.load_extension(f"cogs.{extension}")
                await ctx.send(f"Successfully reloaded `cogs/{extension}.py`")
            except Exception as e:
                await ctx.send(f"{e}")
    else:
        await ctx.message.add_reaction('<:no:828741445069963274>')


@bot.command(help="Run some code!\nRequires you to be Toricane#0818.")
async def run(ctx, *, code):
    used(f"{ctx.author.name}: .run {code}")
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
        used(str(e))


@slash.slash(name="run",
             description="Run some code",
             options=[
                 create_option(name="code",
                               description="Add it here",
                               option_type=3,
                               required=True)
             ])
async def _run(ctx, code):
    used(f"{ctx.author.name}: /run {code}")
    try:
        if ctx.author.id == 721093211577385020:
            res = eval(code)
            if inspect.isawaitable(res):
                await ctx.send(await res)
            else:
                await ctx.send(res)
        else:
            await ctx.message.add_reaction('<:no:828741445069963274>')
    except Exception as e:
        used(str(e))


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


@bot.command(aliases=["fb"], help="Send feedback for the bot!")
async def feedback(ctx, *, feedback):
    used(f"{ctx.author.name}: .feedback {feedback}")
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
    used(f"{ctx.author.name}: /feedback {feedback}")
    await create_feedback(ctx, feedback)


@bot.command(aliases=["fblist"], help="List the feedback.")
async def feedbacklist(ctx):
    used(f"{ctx.author.name}: .feedbacklist")
    await ctx.send("List of feedbacks:")
    await list_feedback(ctx)


@slash.slash(name="feedbacklist", description="List feedback!")
async def _feedbacklist(ctx):
    used(f"{ctx.author.name}: /feedbacklist")
    await ctx.defer()
    await ctx.send("List of feedbacks:")
    await list_feedback(ctx)


@bot.command(aliases=["fbclear"], help="Clear or delete feedback!\nRequires you to be Toricane#0818.\nTo find the number to delete, try using `/list` or `.list`.")
async def feedbackclear(ctx, number=None):
    used(f"{ctx.author.name}: /feedbackclear {number}")
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
    used(f"{ctx.author.name}: /feedbackclear {number}")
    await ctx.defer()
    await delete_feedback(ctx, number)


@bot.command(help="Returns pong with the latency in milliseconds.")
async def ping(ctx):
    used(f"{ctx.author.name}: /ping")
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms.')


@slash.slash(name="ping", description="This returns the bot latency")
async def _ping(ctx):
    used(f"{ctx.author.name}: .ping")
    await ctx.defer()
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms.')


@bot.command(help="Shows the bot's profile picture.")
async def perseverance(ctx):
    used(f"{ctx.author.name}: .perseverance")
    await ctx.send("Profile Picture:")
    await ctx.send(file=discord.File('preservation.png'))


@slash.slash(
    name="perseverance",
    description="Shows the profile picture of Perseverance",
)
async def _perseverance(ctx):
    used(f"{ctx.author.name}: /perseverance")
    await ctx.send("Profile Picture:")
    await ctx.send(file=discord.File('preservation.png'))


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
    await ctx.send(ctx)
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
async def _help(ctx):
    await ctx.send("Please use `\help` instead.")


try:
    for filename in os.listdir("/home/pi/Desktop/DiscordBots/Perseverance-Bot/cogs"):
        try:
            if filename.endswith(".py"):
                try:
                    bot.load_extension(f"cogs.{filename[:-3]}")
                except Exception:
                    print("inside")
                    raise Exception
        except Exception:
            print("middle")
            raise Exception
except Exception:
    print("outside")
    raise Exception

bot.load_extension("jishaku")

bot.run(os.getenv('TOKEN'))
