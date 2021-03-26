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
        await ctx.message.delete()
    except Exception as e:
        print(str(e))