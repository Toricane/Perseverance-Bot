from cmds.reply import maybe_reply
import discord

async def create_feedback(ctx, feedback):
    idea = ctx.author.mention
    with open("cmds/feedback.txt", "a+") as file:
        file.write(f"{idea}§{feedback}\n")
    try:
        await ctx.send(f"You submitted the following feedback: {feedback}", hidden=True)
    except TypeError:
        await maybe_reply(ctx, f"You submitted the following feedback: {feedback}")


async def list_feedback(ctx):
    with open("cmds/feedback.txt", "r") as file:
        x = 0
        for line in file:
            x += 1
            idea, feedback = line.split("§")
            try:
                await ctx.channel.send(f"{x}. {idea}: {feedback}", allowed_mentions=discord.AllowedMentions.none())
            except Exception as e:
                print(str(e))


async def delete_feedback(ctx, number):
    idea = ctx.author.id
    if idea == 721093211577385020:
        if number == None:
            open("cmds/feedback.txt", "w").close()
            await ctx.send("Cleared all of the feedback.")
        else:
            a_file = open("cmds/feedback.txt", "r")
            lines = a_file.readlines()
            a_file.close()

            new_file = open("cmds/feedback.txt", "w")
            for index, line in enumerate(lines):
                if index != (number - 1):
                    new_file.write(line)
            new_file.close()
            await ctx.send(f"Deleted line #{number}.")
            await ctx.channel.send("List of feedbacks now:")
            await list_feedback(ctx)
