import discord


async def help_embeds(ctx, command):  # noqa: C901
    embed = discord.Embed(colour=discord.Colour.orange())
    arg = command.lower()
    if arg == "ping":
        embed.set_author(name='Help for /ping')
        embed.add_field(name='/ping', value='Returns "Pong!"', inline=False)

    elif arg == "inspire":
        embed.add_field(
            name='/inspire',
            value='Sends a random quote from https://zenquotes.io/',
            inline=False)

    elif arg == "hi":
        embed.add_field(name='/hi', value='Returns "Hello!"', inline=False)

    elif arg == "bye":
        embed.add_field(name='/bye', value='Returns "Bye!"', inline=False)

    elif arg == "new":
        embed.add_field(name='/new text',
                        value='Adds more encouraging messages.',
                        inline=False)

    elif arg == "list":
        embed.add_field(
            name='/list',
            value=
            'Only lists the encouragements that have been added from .new.',
            inline=False)

    elif arg == "delete":
        embed.add_field(
            name='/delete number',
            value='Deletes the corsending encouraging message listed in /list.',
            inline=False)

    elif arg == "hello":
        embed.add_field(name='/hello there',
                        value='Returns "General Kenobi!"',
                        inline=False)
        embed.add_field(name='/hello name',
                        value='Returns "Hello Name!"',
                        inline=False)

    elif arg == "say":
        embed.add_field(name='/say "text"',
                        value='Says your text.',
                        inline=False)

    elif arg == "8ball":
        embed.add_field(
            name='/8ball question',
            value=
            'Returns whether or not your question\'s answer is yes or no.',
            inline=False)

    elif arg == "kick":
        embed.add_field(
            name='/kick',
            value='Kicks a member. \nNOTE: requires Kick Members permission.',
            inline=False)

    elif arg == "ban":
        embed.add_field(
            name='/ban',
            value='Bans a member. \nNOTE: requires Ban Members permission.',
            inline=False)

    elif arg == "unban":
        embed.add_field(
            name='/unban',
            value='Unbans a member. \nNOTE: requires Ban Members permission.',
            inline=False)

    elif arg == "purge" or arg == "clear":
        embed.add_field(
            name='/purge number',
            value=
            'Deletes the number of messages. Default is 5. \nNOTE: requires Manage Messages permission.',
            inline=False)

    elif arg == "perseverance":
        embed.add_field(name='/perseverance',
                        value='Shows the profile picture of Perseverance',
                        inline=False)

    elif arg == "wikipedia":
        embed.add_field(
            name='/wikipedia text results lines',
            value=
            'Search anything on Wikipedia! \nNOTE: results and lines are not required and have a default value of 1 and 5.',
            inline=False)

    elif arg == "google":
        embed.add_field(
            name='/google text results',
            value=
            'Google anything! \nNOTE: results is optional and max is 10, default is 5',
            inline=False)

    elif arg == "joke":
        embed.add_field(name='/joke',
                        value='Gives you a random joke!',
                        inline=False)

    elif arg == "invite":
        embed.add_field(
            name='Invite the bot!',
            value=
            'Click [here](https://discord.com/api/oauth2/authorize?client_id=811277990913769523&permissions=3691244614&scope=bot%20applications.commands)',
            inline=False)

    else:
        embed.set_author(name='Help')
        embed.add_field(name='/help help',
                        value='Shows this message',
                        inline=False)
        embed.add_field(name='/credits',
                        value='Shows the credits.',
                        inline=False)
        embed.add_field(name='/ping message',
                        value='Returns "Pong!"',
                        inline=False)
        embed.add_field(name='/inspire',
                        value='send a random quote from https://zenquotes.io/',
                        inline=False)
        embed.add_field(name='/hi', value='Returns "Hello!"', inline=False)
        embed.add_field(name='/bye', value='Returns "Bye!"', inline=False)
        embed.add_field(name='/new text',
                        value='Adds more encouraging messages.',
                        inline=False)
        embed.add_field(
            name='/list',
            value=
            'Only lists the encouragements that have been added from /new.',
            inline=False)
        embed.add_field(
            name='/delete number',
            value='Deletes the corsending encouraging message listed in /list.',
            inline=False)
        embed.add_field(name='/hello there',
                        value='Returns "General Kenobi!"',
                        inline=False)
        embed.add_field(name='/hello name',
                        value='Returns "Hello Name!"',
                        inline=False)
        embed.add_field(name='/say "text"',
                        value='Says your text.',
                        inline=False)
        embed.add_field(
            name='/8ball question',
            value=
            'Returns whether or not your question\'s answer is yes or no.',
            inline=False)
        embed.add_field(
            name='/kick',
            value='Kicks a member. \nNOTE: requires Kick Members permission.',
            inline=False)
        embed.add_field(
            name='/ban',
            value='Bans a member. \nNOTE: requires Ban Members permission.',
            inline=False)
        embed.add_field(
            name='/unban',
            value='Unbans a member. \nNOTE: requires Ban Members permission.',
            inline=False)
        embed.add_field(
            name='/purge number',
            value=
            'Deletes the number of messages. Default is 5. \nNOTE: requires Manage Messages permission.',
            inline=False)
        embed.add_field(name='/perseverance',
                        value='Shows the profile picture of Perseverance',
                        inline=False)
        embed.add_field(
            name='/wikipedia text lines',
            value=
            'Search anything on Wikipedia! \nNOTE: results and lines are not required and have a default value of 1 and 5.',
            inline=False)
        embed.add_field(name='/joke',
                        value='Gives you a random joke!',
                        inline=False)
        embed.add_field(
            name='Invite the bot!',
            value=
            'Click [here](https://discord.com/api/oauth2/authorize?client_id=811277990913769523&permissions=3691244614&scope=bot%20applications.commands)',
            inline=False)

    await ctx.send(embed=embed)
