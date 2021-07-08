class log():
    def __init__(self):
        self.commands = "/home/pi/Desktop/DiscordBots/Perseverance-Bot/commands.txt"
        self.errors = "/home/pi/Desktop/DiscordBots/Perseverance-Bot/errors.txt"
    
    def used(self, ctx=None, command=None, args=None):
        if not ctx == None:
            with open(self.commands, "a") as f:
                f.write(f"\n{ctx.author.name}#{ctx.author.discriminator}: \\{ctx.command} {ctx.args}")
            print(f"\n{ctx.author.name}#{ctx.author.discriminator}: \\{ctx.command} {ctx.args}")
        else:
            with open(self.commands, "a") as f:
                f.write(f"\n{command} -> {args}")
            print(f"\n{command} -> {args}")

    def error(self, ctx=None, error=None, command=None):
        if not ctx == None:
            with open(self.errors, "a") as f:
                f.write(f"\n{ctx.author.name}#{ctx.author.discriminator}: \\{ctx.command} {ctx.args} -> {error}")
            print(f"\n{ctx.author.name}#{ctx.author.discriminator}: \\{ctx.command} {ctx.args} -> {error}")
        else:
            with open(self.errors, "a") as f:
                f.write(f"\n{command} -> {error}")
            print(f"\n{command} -> {error}")
    
    def log(self, text: str):
        with open(self.commands, "a") as f:
            f.write(text)
        print(text)