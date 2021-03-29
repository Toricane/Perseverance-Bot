import discord


async def create_embed(ctx, title, text, color="default"):
    colory = color.lower()
    if colory == "red":
        colory = discord.Colour.red()
    elif colory == "orange":
        colory = discord.Colour.orange()
    elif colory == "yellow":
        colory = discord.Colour.yellow()
    elif colory == "green":
        colory = discord.Colour.green()
    elif colory == "blue":
        colory = discord.Colour.blue()
    elif colory == "indigo":
        colory = discord.Colour.dark_blue()
    elif colory == "purple":
        colory = discord.Colour.purple()
    elif colory == "default":
        colory = discord.Colour.default()
    else:
        colory = discord.Colour.random()

    embed = discord.Embed(colour=colory)
    embed.add_field(name=title, value=text, inline=False)

    await ctx.send(embed=embed)
