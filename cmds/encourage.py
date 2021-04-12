from replit import db
import asyncio
from cmds.words import words

if "responding" not in db.keys():
    db["responding"] = True


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragment(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements


async def responses_list(ctx):
    encouragements = []
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
    length = len(encouragements)
    await ctx.send("List of responses:")
    for x in range(0, length):
        await ctx.channel.send(f"{x+1}. {encouragements[x]}")
        asyncio.sleep(1)


async def response_delete(ctx, number):
    if "encouragements" in db.keys():
        number -= 1
        delete_encouragment(number)
    await responses_list(ctx)


async def new_response(ctx, message):
    if words(message) == False:
        update_encouragements(message)
        await ctx.send(f'New encouraging message added: {message}')
        await responses_list(ctx)
    else:
        await ctx.add_reaction('<:no:828741445069963274>')


def sad_words_list():
    sad_words = [
    "sad", "sorrow", "depressed", "unhappy", "angry", "miserable", "depressing",
    "bitter", "dismal", "heartbroken", "melancholy", "mournful", "pessimistic",
    "somber", "sorrowful", "sorry", "wistful", "bereaved", "cheerless",
    "dejected", "despairing", "despondent", "disconsolate", "distressed",
    "doleful", "down in dumps", "down in mouth", "downcast", "forlorn",
    "gloomy", "glum", "grief-stricken", "grieved", "heartsick", "heavyhearted",
    "hurting", "in doldrums", "in grief", "in the dumps", "languishing",
    "low-spirited", "lugubrious", "morbid", "morose", "out of sorts",
    "pensive", "sick at heart", "troubled", "weeping", "woebegone"
]
    return sad_words