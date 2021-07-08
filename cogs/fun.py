import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, context
from discord_slash.utils.manage_commands import create_option
from cmds.ai import get_a_joke, get_image, ai_response
from cmds.inspire import inspired

from log import log
l = log()

import random

responses = [
    "It is certain.", "It is decidedly so.", "Without a doubt.",
    "Yes - definitely.", "You may rely on it.", "As I see it, yes.",
    "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
    "send hazy, try again.", "Ask again later.", "Better not tell you now.",
    "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.",
    "My response is no.", "My sources say no.", "Outlook not so good.",
    "Very doubtful."
]

def answer():
    return random.choice(responses)

class Fun(commands.Cog, description="Funny commands!"):
    def __init__(self, bot):
        self.bot = bot
    
    # 8ball:
    @commands.command(name="8ball", help="Ask a question, and the bot tells your fortune.")
    async def a8ball(self, ctx, question):
        l.used(ctx)
        await ctx.send(answer())


    @cog_ext.cog_slash(
        name="8ball",
        description="Ask a question, and the bot tells your fortune.",
        options=[
            create_option(name="question",
                        description="Enter your question here",
                        option_type=3,
                        required=True)
        ],
    )
    async def _8ball(self, ctx: SlashContext, question):
        l.used(ctx)
        await ctx.send(answer())

    # hi:
    @commands.command(help="The bot will say hello to you!")
    async def hi(self, ctx):
        l.used(ctx)
        await ctx.send("Hello!")

    @cog_ext.cog_slash(name="hi", description="The bot will say hello to you")
    async def _hi(self, ctx: SlashContext):
        l.used(ctx)
        await ctx.send('Hello!')

    # hello:
    @commands.command(help="Say hello to someone!")
    async def hello(self, ctx, *, name):
        l.used(ctx)
        name = name.capitalize()
        if name == "There":
            await ctx.send("General Kenobi!")
        else:
            await ctx.send(f"Hello {name}!")
            await ctx.message.delete()


    @cog_ext.cog_slash(
        name="hello",
        description="Say hello to someone",
        options=[
            create_option(name="name",
                        description='Put either "there" or the name',
                        option_type=3,
                        required=True)
        ],
    )
    async def _hello(self, ctx: SlashContext, name):
        l.used(ctx)
        name = name.capitalize()
        if name == "There":
            await ctx.send("General Kenobi!")
        else:
            await ctx.send(f"Hello {name}!")

    # bye:
    @commands.command(help="The bot will say bye to you.")
    async def bye(self, ctx):
        l.used(ctx)
        await ctx.send("Bye!")


    @cog_ext.cog_slash(name="bye", description="The bot will say bye to you")
    async def _bye(self, ctx: SlashContext):
        l.used(ctx)
        await ctx.send('Bye!')

    # joke:
    @commands.command(help="Gives a random joke.")
    async def joke(self, ctx, *, joke=None):
        l.used(ctx)
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

    @cog_ext.cog_slash(name="joke", description="Gives you a joke")
    async def _joke(self, ctx: SlashContext, joke=None):
        l.used(ctx)
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

    # image:
    @commands.command(help="Searches for an image!")
    async def image(self, ctx, *, text=None):
        l.used(ctx)
        if text != None:
            if "aww" in text:
                await get_image(ctx, text, "aww")
            elif "duck" in text:
                await get_image(ctx, text, "duck")
            elif "dog" in text:
                await get_image(ctx, text, "dog")
            elif "cat" in text:
                await get_image(ctx, text, "cat")
            elif "hold" in text:
                await get_image(ctx, text, "holdup")
            elif "dankmeme" or "dank meme" in text:
                await get_image(ctx, text, "dankmemes")
            elif "harrypotter" or "harry potter" in text:
                await get_image(ctx, text, "harrypottermemes")
            elif "meme" in text:
                await get_image(ctx, text, "memes")
            elif "art" in text:
                await get_image(ctx, text, "art")
            elif "facepalm" or "face palm" in text:
                await get_image(ctx, text, "facepalm")
            else:
                await ctx.send("Invalid option.")
        else:
            await get_image(ctx, text)
    
    @cog_ext.cog_slash(name="image", description="Searches for an image")
    async def _image(self, ctx: SlashContext, text=None):
        l.used(ctx)
        if text != None:
            if "aww" in text:
                await get_image(ctx, text, "aww")
            elif "duck" in text:
                await get_image(ctx, text, "duck")
            elif "dog" in text:
                await get_image(ctx, text, "dog")
            elif "cat" in text:
                await get_image(ctx, text, "cat")
            elif "hold" in text:
                await get_image(ctx, text, "holdup")
            elif "dankmeme" or "dank meme" in text:
                await get_image(ctx, text, "dankmemes")
            elif "harrypotter" or "harry potter" in text:
                await get_image(ctx, text, "harrypottermemes")
            elif "meme" in text:
                await get_image(ctx, text, "memes")
            elif "art" in text:
                await get_image(ctx, text, "art")
            elif "facepalm" or "face palm" in text:
                await get_image(ctx, text, "facepalm")
            else:
                await ctx.send("Invalid option.")
        else:
            await get_image(ctx, text)

    # ai:
    @commands.command(help="Get an AI response!")
    async def ai(self, ctx, *, msg):
        l.used(ctx)
        if "shark" in msg:
            await ctx.send("Sharks are the BEST!")
        else:
            await ai_response(ctx, msg)


    @cog_ext.cog_slash(name="ai",
                description="Get AI response!",
                options=[
                    create_option(name="msg",
                                description="Your message",
                                option_type=3,
                                required=True)
                ])
    async def _ai(self, ctx, msg):
        l.used(ctx)
        if "shark" in msg:
            await ctx.send("Sharks are the BEST!")
        else:
            await ai_response(ctx, msg)

    # inspire:
    @commands.command(help="Gives a random inspirational quote.")
    async def inspire(self, ctx):
        l.used(ctx)
        quoted = await inspired(ctx)
        await ctx.send(quoted)

    @cog_ext.cog_slash(name="inspire",
                description="The bot will send a random inspirational quote")
    async def _inspire(self, ctx: SlashContext):
        l.used(ctx)
        quoted = await inspired(ctx)
        await ctx.send(quoted)


def setup(bot):
    bot.add_cog(Fun(bot))