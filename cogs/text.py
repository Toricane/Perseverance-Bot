import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
import string, random, requests

from cmds.morse import encrypt, decrypt

from log import used, error

class Text(commands.Cog, description="Text related commands!"):
    def __init__(self, bot):
        self.bot = bot
    
    # morsetotext:
    @commands.command(aliases=["mtt"], help="Get text from morse code.")
    async def morsetotext(self, ctx, *, message):
        result = decrypt(message)
        await ctx.reply(f"```py\n{result}```")

    @cog_ext.cog_slash(name="morsetotext",
                description="Get text from morse code",
                options=[
                    create_option(name="text",
                                description="Your binary code",
                                option_type=3,
                                required=True)
                ])
    async def _morsetotext(self, ctx, message):
        result = decrypt(message)
        await ctx.send(f"```py\n{result.lower()}```")

    # texttomorse:
    @commands.command(aliases=["ttm"], help="Convert text to morse!")
    async def texttomorse(self, ctx, *, message):
        result = encrypt(message.upper())
        await ctx.reply(f"```py\n{result}```")

    @cog_ext.cog_slash(name="texttomorse",
                description="Get morse code from text",
                options=[
                    create_option(name="text",
                                description="Your binary code",
                                option_type=3,
                                required=True)
                ])
    async def _texttomorse(self, ctx, message):
        result = encrypt(message.upper())
        await ctx.send(f"```py\n{result}```")

    # binarytotext:
    @commands.command(aliases=["btt"], help="Convert binary numbers to text.")
    async def binarytotext(self, ctx, *, text):
        ascii_string = "".join([chr(int(binary, 2)) for binary in text.split(" ")])
        await ctx.reply(f"```py\n{ascii_string}```")

    @cog_ext.cog_slash(name="binarytotext",
                description="Get text from binary",
                options=[
                    create_option(name="text",
                                description="Your binary code",
                                option_type=3,
                                required=True)
                ])
    async def binaryToText(self, ctx, text):
        await ctx.defer()
        ascii_string = "".join([chr(int(binary, 2)) for binary in text.split(" ")])
        await ctx.send(f"```py\n{ascii_string}```")

    # texttobinary:
    @commands.command(aliases=["ttb"], help="Convert text to binary!")
    async def texttobinary(self, ctx, *, text):
        res = ' '.join(format(ord(i), '08b') for i in text)
        await ctx.reply(f"```py\n{res}```")

    @cog_ext.cog_slash(name="texttobinary",
                description="Get binary from text",
                options=[
                    create_option(name="text",
                                description="Your binary code",
                                option_type=3,
                                required=True)
                ])
    async def _texttobinary(self, ctx, text):
        await ctx.defer()
        res = ' '.join(format(ord(i), '08b') for i in text)
        await ctx.send(f"```py\n{res}```")

    # say:
    @commands.command(help="Make the bot say anything!")
    async def say(self, ctx, *, text):
        await used(f"{ctx.author.name}#{ctx.author.discriminator}: \\say {text}")
        await ctx.send(text, allowed_mentions=discord.AllowedMentions.none())
        await ctx.message.delete()

    @cog_ext.cog_slash(
        name="say",
        description="Make the bot say anything",
        options=[
            create_option(name="text",
                        description="Say your message",
                        option_type=3,
                        required=True)
        ],
    )
    async def _say(self, ctx, text):
        used.info(f"{ctx.author.name}#{ctx.author.discriminator}: \\say {text}")
        msg = await ctx.send(text, allowed_mentions=discord.AllowedMentions.none())
        await msg.delete()
        await ctx.channel.send(text,
                            allowed_mentions=discord.AllowedMentions.none())

    # password:
    @commands.command(aliases=["pw", "pass"], help="Generate a strong, random password.")
    async def password(self, ctx, length: int, dm=False):
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

    @cog_ext.cog_slash(name="password",
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
    async def _password(self, ctx, length, dm=False):
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

    # reverse:
    @commands.command(aliases=["r", "rev"], help="Reverse your text!")
    async def reverse(self, ctx, *, text):
        await ctx.send(text[::-1])

    @cog_ext.cog_slash(
        name="reverse",
        description="Reverses your text",
        options=[
            create_option(name="text",
                        description="Type it here",
                        option_type=3,
                        required=True)
        ],
    )
    async def _reverse(self, ctx, text):
        await ctx.send(text[::-1])


def setup(bot):
    bot.add_cog(Text(bot))