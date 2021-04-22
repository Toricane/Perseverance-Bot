import discord

help_dict_list = {
    "8ball" : ["Ask the magic 8ball some yes or no questions.", "`/8ball question`\n`.8ball question`"],
    "addrole" : ["Add a role to a member.\nRequires Manage Roles permission.", "`/addrole @username @role`\n`.addrole @username @role`", "`.ar`"],
    "avatar" : ["Get someone's profile picture", "`/avatar @username`\n`.avatar @username`", "`.pfp`"],
    "ban" : ["Ban someone.\nRequires Ban Users permission.", "`/ban @username optional_reason`\n`.ban @username \"optional_reason\"`"],
    "binarytotext" : ["Convert binary numbers to text.", "`/binarytotext binary_numbers`\n`.binarytotext binary_numbers`", "`.btt`"],
    "bye" : ["The bot will say bye to you.", "`/bye`\n`.bye`"],
    "credits" : ["Displays the credits", "`/credits`\n`.credits`"],
    "define" : ["Define any word.", "`/define word`\n`.define word`", "`.def`"],
    "delete" : ["Deletes an encouraging message.\nRequires you to be Toricane#0001.", "`/delete number`\n`.delete number`", "`.del`"],
    "dm" : ["DM someone in the server.", "`/dm @username \"message\"`\n`.dm @username \"message\"`"],
    "embed" : ["Create an embed using the bot!", "`/embed title text optional_color`\n`.embed \"title\" \"text\" optional_color`"],
    "feedback" : ["Send feedback for the bot!", "`/feedback text`\n`.feedback text`", "`.fb`"],
    "feedbackclear" : ["Clear or delete feedback!\nRequires you to be Toricane#0001.\nTo find the number to delete, try using `/list` or `.list`.", "`/feedbackclear optional_number`\n`.feedbackclear optional_number`", "`.fbclear`"],
    "feedbacklist" : ["List the feedback.", "`/feedbacklist`\n`.feedbacklist`", "`.fblist`"],
    "google" : ["Google anything with this command!", "`/google text optional_results_as_number`\n`.google \"text\" optional_results_as_number`"],
    "googleimages" : ["Google images with this command!", "`/googleimages text optional_results_as_number`\n`.googleimages \"text\" optional_results_as_number`", "`.gpics`"],
    "hello" : ["The bot will say hello to you!", "`/hello`\n`.hello`"],
    "help" : ["Shows this help message", "`/help command_name`\n`.help command_name`", "`.h`"],
    "hi" : ["Say hello to someone through the bot!", "`/hi @username`\n`.hi @username`"],
    "inspire" : ["Gives a random quote.", "`/inspire`\n`.inspire`"],
    "invite" : ["Get the invite link for the bot!", "`/invite`\n`.invite`"],
    "joke" : ["Gives a random programming joke.", "`/joke`\n`.joke`"],
    "kick" : ["Kick a member.\nRequires Kick Members permission.", "`/kick @username reason`\n`.kick @username \"reason\"`"],
    "list" : ["Lists the encouraging messages.", "`/list`\n`.list`"],
    "morsetotext" : ["Get text from morse code.", "`/morsetotext morse_code`\n`.morsetotext morse_code`", "`.mtt`"],
    "new" : ["Create a new encouraging message!", "`/new encouraging_message`\n`.new encouraging_message`"],
    "nick" : ["Change someone's nickname.\nRequires Manage Nicknames permission.", "`/nick @username new_nickname`\n`.nick @username \"new_nickname\"`"],
    "password" : ["Generate a strong, random password.", "`/password length dm_True_or_False`\n`.password length dm_True_or_False`", "`.pw`\n`.pass`"],
    "perseverance" : ["Shows the bot's profile picture.", "`/perseverance`\n`.perseverance`"],
    "ping" : ["Returns pong with the latency in milliseconds.", "`/ping`\n`.ping`"],
    "poll" : ["Create a quick and easy poll!\nSeparate the choices with \"/\".", "`/poll question choices optional_mention`\n`.poll \"question\" \"choices\" optional_mention`", "`.cmd`"],
    "purge" : ["Delete some messages!\nDefault 5.", "`/purge optional_amount`\n`.purge optional_amount`"],
    "reciprocal" : ["Get a reciprocal of a fraction!", "`/reciprocal fraction`\n`.reciprocal fraction`", "`.reci`"],
    "removerole" : ["Remove a role from someone.\nRequires Manage Roles permission.", "`/removerole @username @role`\n`.removerole @username @role`", "`.rr`"],
    "reverse" : ["Reverse your text!", "`/reverse text`\n`.reverse text`", "`.r`\n`.rev`"],
    "run" : ["Run some code!\nRequires you to be Toricane#0001.", "`/run code`\n`.run code`"],
    "say" : ["Make the bot say anything!", "`/say text`\n`.say text`"],
    "texttobinary" : ["Convert text to binary!", "`/texttobinary text`\n`.texttobinary text`", "`.ttb`"],
    "texttomorse" : ["Convert text to morse!", "`/texttomorse text`\n`.texttomorse text`", "`.ttm`"],
    "translate" : ["Translate text on Google Translate!\nOutput language is set to English as default.\nInput language is set to Detect Language as default.", "`/translate text optional_output_lang optional_input_lang`\n`.translate \"text\" optional_output_lang optional_input_lang`"],
    "unban" : ["Unban someone.\nRequires Ban Members permission.", "`/unban @username`\n`.unban @username`"],
    "wikipedia" : ["Search anything on Wikipedia!\nResults is set to 1 as default.\nLines is set to 5 as default.\n\nMore than one result will\nmake the bot choose one at random.", "`/wikipedia text optional_results optional_lines_as_number`\n`.wikipedia \"text\" optional_results optional_lines_as_number`", "`.wiki`"]
}


async def get_command_help_embed(ctx, command):
    command = command.lower()
    list_cmd = help_dict_list.get(command)
    description = list_cmd[0]
    usage = list_cmd[1]
    try:
        aliases = list_cmd[2]
    except Exception:
        aliases = None
    embed = discord.Embed(colour=discord.Colour.orange())
    embed.set_author(name=f"Info about {command}", icon_url=f"{ctx.guild.icon_url}")
    embed.add_field(name="Description:", value=f"{description}", inline=True)
    embed.add_field(name="How to use:", value=f"{usage}", inline=True)
    if aliases != None:
        embed.add_field(name="Aliases:", value=f"{aliases}", inline=True)
    embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}.")
    
    await ctx.send(embed=embed)


async def get_all_help(ctx):
    embed = discord.Embed(colour=discord.Colour.orange())
    embed.add_field(name="<:perseverance:828089686399778856>  List of Commands", value="Use `.help command` or `/help command` to know more about a specific command!\n**Important Links:**\n[Invite the Bot](https://discord.com/api/oauth2/authorize?client_id=811277990913769523&permissions=3691244614&scope=bot%20applications.commands) | [Discord](https://discord.gg/QFcMcCQGbU) | [Website](https://PerseveranceBot.repl.co)")
    embed.add_field(name="<:mod:830265633542635550>  Moderation:", value="`addrole`, `removerole`, `kick`, `ban`, `unban`", inline=False)
    embed.add_field(name="<:fun:831018113293746187>  Fun:", value="`8ball`, `hi`, `hello`, `bye`, `joke`, `inspire`", inline=False)
    embed.add_field(name="<:google:831015776893927454>  Google Related:", value="`google`, `googleimages`, `translate`, `define`, `wikipedia`", inline=False)
    embed.add_field(name="<:text:831021740259147856>  Text Related:", value="`morsetotext`, `texttomorse`, `binarytotext`, `texttobinary`, `say`, `reciprocal`, `password`, `reverse`", inline=False)
    embed.add_field(name="<:useful:831028975698444288>  Utility:", value="`poll`, `avatar`, `purge`, `credits`, `embed`, `nick`, `invite`", inline=False)
    embed.add_field(name="<:feedback:831205687152345148>  Feedback:", value="`feedback`, `feedbacklist`", inline=False)
    embed.add_field(name="<:miscellaneous:831207806719361065>  Miscellaneous:", value="`ping`, `perseverance`", inline=False)
    embed.set_footer(text="The prefix for the bot is both \".\" and \"/\".")
    await ctx.send(embed=embed)

async def help_embeds2(ctx, command):
    try:
        if command != None and any(map(command.__contains__,list(help_dict_list.keys()))):
            command = command.lower()
            command = command.replace(" ", "")
            await get_command_help_embed(ctx, command)
        else:
            await get_all_help(ctx)
            
    except Exception as e:
        raise e

all_commands = [""" 
  addrole       x
  avatar        x
  ban           x
  binarytotext  x
  bye           x
  credits       x
  define        x
  delete        x
  eightball     x
  embed         x
  feedback      x
  feedbackclear x
  feedbacklist  x
  google        x
  googleimages  x
  hello         x
  help          x
  hi            x
  inspire       x
  invite        x
  joke          x
  kick          x
  list          x
  morsetotext   x
  new           x
  nick          x
  password      x
  perseverance  x
  ping          x
  poll          x
  purge         x
  reciprocal    x
  removerole    x
  reverse       x
  say           x
  texttobinary  x
  texttomorse   x
  translate     x
  unban         x
  wikipedia     x
  """]