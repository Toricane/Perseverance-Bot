import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from cmds.googlestuff import pls_google, pls_translate
from cmds.define import pls_define

import wikipedia as wiki
import random

class Google(commands.Cog, description="Google related commands!"):
    def __init__(self, bot):
        self.bot = bot
    
    # google:
    @commands.command(help="Google anything with this command!")
    async def google(self, ctx, *, text):
        async with ctx.typing():
            await pls_google(ctx, text, 5)

    @cog_ext.cog_slash(
        name="google",
        description="Search anything on Google!",
        options=[
            create_option(name="text",
                        description="Search it here",
                        option_type=3,
                        required=True)
        ]
    )
    async def _google(self, ctx: SlashContext, text):
        await ctx.defer()
        await pls_google(ctx, text, 5)

    # translate:
    @commands.command(help="Translate text on Google Translate!\nOutput language is set to English as default.\nInput language is set to Detect Language as default.")
    async def translate(self, ctx, text, output_lang="en", input_lang=None):
        await pls_translate(ctx, text, output_lang, input_lang)

    @cog_ext.cog_slash(
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
    async def _translate(self, ctx: SlashContext, text, output_lang="en", input_lang=None):
        await ctx.defer()
        await pls_translate(ctx, text, output_lang, input_lang)

    # define:
    @commands.command(aliases=["def"], help="Define any word in English.")
    async def define(self, ctx, word):
        await pls_define(ctx, word)

    @cog_ext.cog_slash(
        name="define",
        description="Define any word in English!",
        options=[
            create_option(name="word",
                        description="Type it here",
                        option_type=3,
                        required=True)
        ],
    )
    async def _define(self, ctx: SlashContext, word):  # noqa: C901
        await ctx.defer()
        await pls_define(ctx, word)

    # wikipedia:
    @commands.command(aliases=["wiki"],
                description="Searches for something on wikipedia",
                help="Search anything on Wikipedia!\nResults is set to 1 as default.\nLines is set to 5 as default.\n\nMore than one result will make the bot choose one at random.")
    async def wikipedia(self, ctx, text: str, results: int = 1, lines: int = 5):
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
            await ctx.send(
                "ERROR, there may be too many to choose from, or a module error.")
            await ctx.send(f"ERROR: {e}")

    @cog_ext.cog_slash(
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
    async def _wikipedia(self, ctx, text, results=1, lines=5):
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
            await ctx.send(
                "ERROR, there may be too many to choose from, or a module error.")
            await ctx.send(f"ERROR: {e}")


def setup(bot):
    bot.add_cog(Google(bot))