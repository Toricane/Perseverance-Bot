def used(command=None, ctx=None, error=None):
    if not ctx == None:
        with open("/home/pi/Desktop/DiscordBots/Perseverance-Bot/commands.txt", "a") as f:
            f.write(f"\n{ctx.author.name}#{ctx.author.discriminator}: {command} -> {error}")
        print(f"\n{ctx.author.name}#{ctx.author.discriminator}: {command} -> {error}")
    else:
        with open("/home/pi/Desktop/DiscordBots/Perseverance-Bot/commands.txt", "a") as f:
            f.write(f"\n{command} -> {error}")
        print(f"\n{command} -> {error}")

def error(error=None, command=None, ctx=None):
    if not ctx == None:
        with open("/home/pi/Desktop/DiscordBots/Perseverance-Bot/errors.txt", "a") as f:
            f.write(f"\n{ctx.author.name}#{ctx.author.discriminator}: {command} -> {error}")
        print(f"\n{ctx.author.name}#{ctx.author.discriminator}: {command} -> {error}")
    else:
        with open("/home/pi/Desktop/DiscordBots/Perseverance-Bot/errors.txt", "a") as f:
            f.write(f"\n{command} -> {error}")
        print(f"\n{command} -> {error}")