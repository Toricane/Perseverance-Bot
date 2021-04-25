import asyncio

reaction = None

async def purge_msgs(ctx, amount, usere, client, method):
    global reaction
    if usere == None:
        amount = int(amount)
        
        if amount < 100:
            if method == "slash":
                await ctx.send("Removing messages...")
                await ctx.channel.purge(limit=amount + 1)
                msg = await ctx.send(f"Removed {amount} messages.", delete_after=5)
            elif method == "dpy":
                await ctx.send("Removing messages...")
                await ctx.channel.purge(limit=amount + 2)
                msg = await ctx.send(f"Removed {amount} messages.", delete_after=5)
        else:
            msg = await ctx.send(f"React to this message with 👍 to delete {amount} messages, or react with 👎 to cancel.")
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')
            def check(reaction, user):
                return user == ctx.author and (str(reaction.emoji) == '👍' or str(reaction.emoji) == '👎')

            try:
                reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)

                if str(reaction) == '👍':
                    await ctx.send("Removing messages...")
                    await ctx.channel.purge(limit=amount + 3)
                    msg = await ctx.send(f"Removed {amount} messages.")
                    await asyncio.sleep(5)
                    await msg.delete()
                elif str(reaction) == '👎':
                    msg2 = await ctx.send('Canceled.')
                    await asyncio.sleep(5)
                    try:
                        await ctx.delete()
                        await msg.delete()
                        await msg2.delete()
                    except:
                        await ctx.message.delete()
                        await msg.delete()
                        await msg2.delete()
            except asyncio.TimeoutError:
                msg2 = await ctx.send('Timed out.')
                await asyncio.sleep(5)
                await ctx.delete()
                await msg.delete()
                await msg2.delete()
                reaction = None
    else:
        amount = int(amount)
        if amount < 100:
            if method == "slash":
                await ctx.send("Removing messages...")
                await ctx.channel.purge(limit=amount + 1)
                msg = await ctx.send(f"Removed {amount} messages.", delete_after=5)
            elif method == "dpy":
                async for message in ctx.channel.history(limit=amount):
                    counter = 0
                    if str(message.author) == f"{usere.name}#{usere.discriminator}":
                        await asyncio.sleep(0.25)
                        await message.delete()
                        counter += 1
                await ctx.send(f"Removed {counter} messages from a range of {amount} messages.", delete_after=5)
        else:
            countereee = 0
            async for message in ctx.channel.history(limit=amount):
                if str(message.author) == f"{usere.name}#{usere.discriminator}":
                    countereee += 1
            msg = await ctx.send(f"React to this message with 👍 to delete {countereee} messages from `{usere}` from a range of {amount} messages, or react with 👎 to cancel.")
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')
            def check(reaction, user):
                return user == ctx.author and (str(reaction.emoji) == '👍' or str(reaction.emoji) == '👎')

            try:
                reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
                if method == "slash":
                    if str(reaction) == '👍':
                        await ctx.send("Removing messages...")
                        await ctx.channel.purge(limit=amount + 3)
                        msg = await ctx.send(f"Removed {amount} messages.")
                        await asyncio.sleep(5)
                        await msg.delete()
                    elif str(reaction) == '👎':
                        msg2 = await ctx.send('Canceled.')
                        await asyncio.sleep(5)
                        try:
                            await ctx.delete()
                            await msg.delete()
                            await msg2.delete()
                        except:
                            await ctx.message.delete()
                            await msg.delete()
                            await msg2.delete()
                elif method == "dpy":
                    if str(reaction) == '👍':
                        counter = 0
                        async for message in ctx.channel.history(limit=amount):
                            if str(message.author) == f"{usere.name}#{usere.discriminator}":
                                await asyncio.sleep(0.25)
                                await message.delete()
                                counter += 1
                        await ctx.send(f"Removed {counter} messages from a range of {amount} messages.", delete_after=5)
                    elif str(reaction) == '👎':
                        msg2 = await ctx.send('Canceled.')
                        await asyncio.sleep(5)
                        try:
                            await ctx.delete()
                            await msg.delete()
                            await msg2.delete()
                        except:
                            await ctx.message.delete()
                            await msg.delete()
                            await msg2.delete()
            except asyncio.TimeoutError:
                msg2 = await ctx.send('Timed out.')
                await asyncio.sleep(5)
                await ctx.delete()
                await msg.delete()
                await msg2.delete()
                reaction = None