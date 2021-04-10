import discord


async def show_credits(ctx):
    embed = discord.Embed(colour=discord.Colour.orange())
    embed.set_author(name='Credits')
    embed.add_field(name='Created by Toricane#0001',
                    value='"Thank you for using my bot!" - Toricane',
                    inline=False)
    embed.add_field(name='Hosted by Repl.it',
                    value='https://repl.it/@Toricane/Perseverance-Bot#main.py',
                    inline=False)
    embed.add_field(name='Saved in GitHub',
                    value='https://github.com/Toricane/Perseverance-Bot/',
                    inline=False)
    embed.add_field(
        name='Tutorials Used:',
        value=
        'https://youtu.be/SPTfmiYiuok\nhttps://youtube.com/playlist?list=PLW3GfRiBCHOhfVoiDZpSz8SM_HybXRPzZ',
        inline=False)
    embed.add_field(
        name='Documentations Used:',
        value=
        'https://discordpy.readthedocs.io/en/latest/\nhttps://discord-py-slash-command.readthedocs.io/en/latest/',
        inline=False)
    embed.add_field(
        name='Website:',
        value=
        'https://perseverance-bot.toricane.repl.co/',
        inline=False)
    embed.add_field(
        name='Invite the bot!',
        value=
        'Click [here](https://discord.com/api/oauth2/authorize?client_id=811277990913769523&permissions=3691244614&scope=bot%20applications.commands)',
        inline=False)
    await ctx.send(embed=embed)
