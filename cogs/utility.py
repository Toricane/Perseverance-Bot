import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

from cmds.poll import create_poll
from cmds.purge import purge_msgs
from cmds.embed import create_embed

from log import log
l = log()

class Utility(commands.Cog, description="Useful commands!"):
    def __init__(self, bot):
        self.bot = bot

    # poll:
    @commands.command(help="Create a quick and easy poll!\nSeparate the choices with \"/\".")
    async def poll(self, ctx, question, choices, mention=None):
        l.used(ctx)
        await create_poll(ctx, question, choices, mention)

    @cog_ext.cog_slash(
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
    async def _poll(self, ctx, question, choices, mention=None):
        l.used(ctx)
        try:
            await create_poll(ctx, question, choices, mention)
        except Exception:
            await ctx.send("There was an unexpected error, and the bot developer has been notified.")

    # avatar:
    @commands.command(aliases=["pfp"], help="View someone's profile picture")
    async def avatar(self, ctx, member: discord.Member):
        l.used(ctx)
        try:
            embed = discord.Embed(colour=discord.Colour.orange())
            url = member.avatar_url
            embed.add_field(name=f'{member}', value='Avatar:', inline=False)
            embed.set_image(url=url)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send("There was an unexpected error, and the bot developer has been notified.")
            l.error(ctx, e)

    @cog_ext.cog_slash(
        name="avatar",
        description="View someone's profile picture",
        options=[
            create_option(name="member",
                        description="Add the member here",
                        option_type=6,
                        required=True)
        ],
    )
    async def _avatar(self, ctx, member: discord.Member):
        l.used(ctx)
        try:
            embed = discord.Embed(colour=discord.Colour.orange())
            url = member.avatar_url
            embed.add_field(name=f'{member}', value='Avatar:', inline=False)
            embed.set_image(url=url)
            await ctx.send(embed=embed)
        except Exception as e:
            l.error(ctx, e)
            await ctx.send("There was an unexpected error, and the bot developer has been notified.")

    # purge:
    @commands.command(help="Delete some messages!\nDefault 5.\nRequires Manage Messages permission to use.")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=5, user: discord.Member = None):
        l.used(ctx)
        await purge_msgs(ctx, amount, usere=user, client=self.bot, method="dpy")

    @cog_ext.cog_slash(name="purge",
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
    async def _purge(self, ctx, amount=5, user=None):
        l.used(ctx)
        await ctx.defer()
        await purge_msgs(ctx, amount, usere=user, client=self.bot, method="slash")

    # credits:
    @commands.command(aliases=["info", "about"], help="Displays the credits.")
    async def credits(self, ctx):
        l.used(ctx)
        embed = discord.Embed(colour=discord.Colour.orange())
        embed.set_author(name='Credits')
        embed.add_field(name='Created by Toricane#0818',
                        value='"Thank you for using my bot!" - Toricane',
                        inline=False)
        embed.add_field(name='Hosted by Repl.it',
                        value='https://replit.com/@PerseveranceBot/PerseveranceBot',
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
            name='Website:',
            value=
            'https://PerseveranceBot.repl.co',
            inline=False)
        embed.add_field(
            name='Invite the bot!',
            value=
            'Click [here](https://discord.com/api/oauth2/authorize?client_id=811277990913769523&permissions=3691244614&scope=bot%20applications.commands)',
            inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="credits", description="Shows the credits")
    async def _credits(self, ctx):
        l.used(ctx)
        embed = discord.Embed(colour=discord.Colour.orange())
        embed.set_author(name='Credits')
        embed.add_field(name='Created by Toricane#0818',
                        value='"Thank you for using my bot!" - Toricane',
                        inline=False)
        embed.add_field(name='Hosted by Repl.it',
                        value='https://replit.com/@PerseveranceBot/PerseveranceBot',
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
            name='Website:',
            value=
            'https://PerseveranceBot.repl.co',
            inline=False)
        embed.add_field(
            name='Invite the bot!',
            value=
            'Click [here](https://discord.com/api/oauth2/authorize?client_id=811277990913769523&permissions=3691244614&scope=bot%20applications.commands)',
            inline=False)
        await ctx.send(embed=embed)

    # embed:
    @commands.command(help="Create an embed using the bot!")
    async def embed(self, ctx, title, text, color="default"):
        l.used(ctx)
        await create_embed(ctx, title, text, color)

    @cog_ext.cog_slash(
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
    async def _embed(self, ctx, title, text, color="default"):
        l.used(ctx)
        await create_embed(ctx, title, text, color)

    # invite:
    @commands.command(help="Get the invite link for the bot!")
    async def invite(self, ctx):
        l.used(ctx)
        embed = discord.Embed(colour=discord.Colour.orange())
        embed.add_field(
            name='Invite the bot!',
            value=
            'Click [here](https://discord.com/api/oauth2/authorize?client_id=811277990913769523&permissions=3691244614&scope=bot%20applications.commands)',
            inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="invite", description="Shows the invite link for the bot")
    async def _invite(self, ctx):
        l.used(ctx)
        embed = discord.Embed(colour=discord.Colour.orange())
        embed.add_field(
            name='Invite the bot!',
            value=
            'Click [here](https://discord.com/api/oauth2/authorize?client_id=811277990913769523&permissions=3691244614&scope=bot%20applications.commands)',
            inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Utility(bot))