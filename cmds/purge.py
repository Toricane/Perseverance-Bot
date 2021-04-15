import discord
import asyncio

reaction = None

async def purge_msgs(ctx, amount, client):
    amount = int(amount)
    global reaction
    if amount < 100:
        await ctx.send("Removing messages...")
        await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(f"Removed {amount} messages.", delete_after=5)
    else:
        msg = await ctx.send(f"React to this message with 👍 to delete {amount} messages, or react with 👎 to cancel.")
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        def check(reaction, user):
            return user == ctx.author and (str(reaction.emoji) == '👍' or str(reaction.emoji) == '👎')

        try:
            print(1)
            reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
            print(reaction)
            print(user)
        except asyncio.TimeoutError:
            msg2 = await ctx.send('Timed out.')
            await asyncio.sleep(5)
            await ctx.delete()
            await msg.delete()
            await msg2.delete()
            reaction = None
        else:
            if reaction == '👍':
                await ctx.send("Removing messages...")
                await ctx.channel.purge(limit=amount + 3)
                msg = await ctx.send(f"Removed {amount} messages.")
                await asyncio.sleep(5)
                await msg.delete()
            elif reaction == '👎':
                msg2 = await ctx.send('Canceled.')
                await asyncio.sleep(5)
                await ctx.delete()
                await msg.delete()
                await msg2.delete()