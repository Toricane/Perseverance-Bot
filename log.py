async def used(command=None, ctx=None, error=None):
    if not ctx == None:
        with open("commands.txt", "a") as f:
            f.write(f"\n{ctx.author.name}#{ctx.author.discriminator}: {command} -> {error}")
    else:
        with open("commands.txt", "a") as f:
            f.write(f"\n{command}")

async def error(error=None, command=None, ctx=None):
    if not ctx == None:
        with open("errors.txt", "a") as f:
            f.write(f"\n{ctx.author.name}#{ctx.author.discriminator}: {command} -> {error}")
    else:
        with open("errors.txt", "a") as f:
            f.write(f"\n{error}")