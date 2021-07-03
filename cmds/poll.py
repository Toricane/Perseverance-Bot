async def create_poll(ctx, question, choices, mention): # noqa: C901
    try:
        content = choices.split("/")
        if mention != None:
            if len(content) > 0:
                message = f"""
{mention.mention} {ctx.author.mention} asks: {question}

:one:: {content[0]}
"""
            if len(content) > 1:
                message = f"""
{mention.mention} {ctx.author.mention} asks: {question}

:one:: {content[0]}
:two:: {content[1]}
"""
            if len(content) > 2:
                message = f"""
{mention.mention} {ctx.author.mention} asks: {question}

:one:: {content[0]}
:two:: {content[1]}
:three:: {content[2]}
"""
            if len(content) > 3:
                message = f"""
{mention.mention} {ctx.author.mention} asks: {question}

:one:: {content[0]}
:two:: {content[1]}
:three:: {content[2]}
:four:: {content[3]}
"""
            if len(content) > 4:
                message = f"""
{mention.mention} {ctx.author.mention} asks: {question}

:one:: {content[0]}
:two:: {content[1]}
:three:: {content[2]}
:four:: {content[3]}
:five:: {content[4]}
"""
            if len(content) > 5:
                message = f"""
{mention.mention} {ctx.author.mention} asks: {question}

:one:: {content[0]}
:two:: {content[1]}
:three:: {content[2]}
:four:: {content[3]}
:five:: {content[4]}
:six:: {content[5]}
"""
            if len(content) > 6:
                message = f"""
{mention.mention} {ctx.author.mention} asks: {question}

:one:: {content[0]}
:two:: {content[1]}
:three:: {content[2]}
:four:: {content[3]}
:five:: {content[4]}
:six:: {content[5]}
:seven:: {content[6]}
"""
            if len(content) > 7:
                message = f"""
{mention.mention} {ctx.author.mention} asks: {question}

:one:: {content[0]}
:two:: {content[1]}
:three:: {content[2]}
:four:: {content[3]}
:five:: {content[4]}
:six:: {content[5]}
:seven:: {content[6]}
:seven:: {content[7]}
"""
            if len(content) > 8:
                message = f"""
{mention.mention} {ctx.author.mention} asks: {question}

:one:: {content[0]}
:two:: {content[1]}
:three:: {content[2]}
:four:: {content[3]}
:five:: {content[4]}
:six:: {content[5]}
:seven:: {content[6]}
:seven:: {content[7]}
:seven:: {content[8]}
"""
            if len(content) > 9:
                message = f"""
{mention.mention} {ctx.author.mention} asks: {question}

:one:: {content[0]}
:two:: {content[1]}
:three:: {content[2]}
:four:: {content[3]}
:five:: {content[4]}
:six:: {content[5]}
:seven:: {content[6]}
:seven:: {content[7]}
:seven:: {content[8]}
:seven:: {content[9]}
"""
        else:
            if len(content) > 0:
                message = f"""
{ctx.author.mention} asks: {question}

:one:: {content[0]}
"""
            if len(content) > 1:
                message = f"""
{ctx.author.mention} asks: {question}

:one:: {content[0]}
:two:: {content[1]}
"""
            if len(content) > 2:
                message = f"""
{ctx.author.mention} asks: {question}

:one:: {content[0]}
:two:: {content[1]}
:three:: {content[2]}
"""
            if len(content) > 3:
                message = f"""
{ctx.author.mention} asks: {question}

:one:: {content[0]}
:two:: {content[1]}
:three:: {content[2]}
:four:: {content[3]}
"""
            if len(content) > 4:
                message = f"""
{ctx.author.mention} asks: {question}

:one:: {content[0]}
:two:: {content[1]}
:three:: {content[2]}
:four:: {content[3]}
:five:: {content[4]}
"""
            if len(content) > 5:
                message = f"""
{ctx.author.mention} asks: {question}

:one:: {content[0]}
:two:: {content[1]}
:three:: {content[2]}
:four:: {content[3]}
:five:: {content[4]}
:six:: {content[5]}
"""
            if len(content) > 6:
                message = f"""
{ctx.author.mention} asks: {question}

:one:: {content[0]}
:two:: {content[1]}
:three:: {content[2]}
:four:: {content[3]}
:five:: {content[4]}
:six:: {content[5]}
:seven:: {content[6]}
"""
            if len(content) > 7:
                message = f"""
{ctx.author.mention} asks: {question}

:one:: {content[0]}
:two:: {content[1]}
:three:: {content[2]}
:four:: {content[3]}
:five:: {content[4]}
:six:: {content[5]}
:seven:: {content[6]}
:eight:: {content[7]}
"""
            if len(content) > 8:
                message = f"""
{ctx.author.mention} asks: {question}

:one:: {content[0]}
:two:: {content[1]}
:three:: {content[2]}
:four:: {content[3]}
:five:: {content[4]}
:six:: {content[5]}
:seven:: {content[6]}
:eight:: {content[7]}
:nine:: {content[8]}
"""
            if len(content) > 9:
                message = f"""
{ctx.author.mention} asks: {question}

:one:: {content[0]}
:two:: {content[1]}
:three:: {content[2]}
:four:: {content[3]}
:five:: {content[4]}
:six:: {content[5]}
:seven:: {content[6]}
:eight:: {content[7]}
:nine:: {content[8]}
:ten:: {content[9]}
"""

        messgae = await ctx.send(message)
        if len(content) > 0:
            await messgae.add_reaction("1️⃣")
        if len(content) > 1:
            await messgae.add_reaction("2️⃣")
        if len(content) > 2:
            await messgae.add_reaction("3️⃣")
        if len(content) > 3:
            await messgae.add_reaction("4️⃣")
        if len(content) > 4:
            await messgae.add_reaction("5️⃣")
        if len(content) > 5:
            await messgae.add_reaction("6️⃣")
        if len(content) > 6:
            await messgae.add_reaction("7️⃣")
        if len(content) > 7:
            await messgae.add_reaction("8️⃣")
        if len(content) > 8:
            await messgae.add_reaction("9️⃣")
        if len(content) > 9:
            await messgae.add_reaction("🔟")
    except Exception as e:
        print(str(e))