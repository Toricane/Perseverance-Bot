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

from log import log

l = log()


bot = commands.Bot(command_prefix="\\",
                   intents=Intents.all(),
                   case_insensitive=True)
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
    l.log(f'We have logged in as {bot.user}')
    timestamp = datetime.datetime.now()
    l.log(timestamp.strftime(r"%A, %b %d, %Y, %I:%M %p PDT"))
    l.log(f"guild_ids={guild_ids}")
    l.log(f"In {len(bot.guilds)} servers")
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
    l.log(f'{member} has joined {member.guild.name}')
    if member.guild.id == 820419188866547712:
        role = "Shark"
        await member.add_roles(discord.utils.get(member.guild.roles,
                                                 name=role))


@bot.event
async def on_member_remove(member):
    l.log(f'{member} has left {member.guild.name}')


@bot.event
async def on_slash_command_error(ctx, ex):
    if isinstance(ex, discord.ext.commands.errors.MissingPermissions):
        perms_missing = ex.missing_perms
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
        l.error(ctx, ex)
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


@bot.command(help="Returns pong with the latency in milliseconds.")
async def ping(ctx):
    l.used(ctx)
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms.')


@slash.slash(name="ping", description="This returns the bot latency")
async def _ping(ctx):
    l.used(ctx)
    await ctx.defer()
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms.')


@bot.command(help="Shows the bot's profile picture.")
async def perseverance(ctx):
    l.used(ctx)
    await ctx.send("Profile Picture:")
    await ctx.send(file=discord.File('preservation.png'))


@slash.slash(
    name="perseverance",
    description="Shows the profile picture of Perseverance",
)
async def _perseverance(ctx):
    l.used(ctx)
    await ctx.send("Profile Picture:")
    await ctx.send(file=discord.File('preservation.png'))


@slash.slash(
    name="help",
    description="Shows all the possible commands and how to use them"
)
async def _help(ctx):
    l.used(ctx)
    await ctx.send("Please use `\help` instead.")


class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color.orange(), description="")
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)

bot.help_command = MyHelpCommand()


try:
    for filename in os.listdir("/home/pi/Desktop/DiscordBots/Perseverance-Bot/cogs"):
        try:
            if filename.endswith(".py"):
                try:
                    bot.load_extension(f"cogs.{filename[:-3]}")
                except Exception as e:
                    print("inside")
                    raise e
        except Exception as e:
            print("middle")
            raise e
except Exception as e:
    print("outside")
    raise e

bot.load_extension("jishaku")

bot.run(os.getenv('TOKEN'))
