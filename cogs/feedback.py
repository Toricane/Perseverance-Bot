import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from cmds.feedback import create_feedback, list_feedback, delete_feedback

from log import log
l = log()

class Feedback(commands.Cog, description="Give feedback for the bot!"):
    def __init__(self, bot):
        self.bot = bot
    
    # commands:
    @commands.command(aliases=["fb"], help="Send feedback for the bot!")
    async def feedback(self, ctx, *, feedback):
        l.used(ctx)
        await create_feedback(ctx, feedback)


    @cog_ext.cog_slash(
        name="feedback",
        description="Give feedback!",
        options=[
            create_option(name="feedback",
                        description="Type member here",
                        option_type=3,
                        required=True)
        ],
    )
    async def _feedback(self, ctx, feedback):
        l.used(ctx)
        await create_feedback(ctx, feedback)


    @commands.command(aliases=["fblist"], help="List the feedback.")
    async def feedbacklist(ctx):
        l.used(ctx)
        await ctx.send("List of feedbacks:")
        await list_feedback(ctx)


    @cog_ext.cog_slash(name="feedbacklist", description="List feedback!")
    async def _feedbacklist(self, ctx):
        l.used(ctx)
        await ctx.defer()
        await ctx.send("List of feedbacks:")
        await list_feedback(ctx)


    @commands.command(aliases=["fbclear"], help="Clear or delete feedback!\nRequires you to be Toricane#0818.\nTo find the number to delete, try using `/list` or `.list`.")
    async def feedbackclear(self, ctx, number=None):
        l.used(ctx)
        await delete_feedback(ctx, number)


    @cog_ext.cog_slash(
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
    async def _feedbackclear(self, ctx, number=None):
        l.used(ctx)
        await ctx.defer()
        await delete_feedback(ctx, number)


def setup(bot):
    bot.add_cog(Feedback(bot))