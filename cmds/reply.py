import asyncio
import contextlib3 as contextlib
import discord

async def maybe_reply(ctx, content=None, embed=None, mention_author=False):
    """Replies if there is a message in between the command invoker and the bot's message."""
    await asyncio.sleep(0.05)
    with contextlib.suppress(discord.HTTPException):
        try:
            if getattr(ctx.channel,"last_message", False) != ctx.message:
                return await ctx.reply(content, mention_author=mention_author)
        except AttributeError:
            if getattr(ctx.channel,"last_message", False) != ctx:
                return await ctx.reply(content, mention_author=mention_author)
    try:
        return await ctx.send(content)
    except:
        return await ctx.reply(content, mention_author=mention_author)
