from replit import db

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
        await ctx.send(f"{x+1}. {encouragements[x]}")


async def response_delete(ctx, number):
    encouragements = []
    if "encouragements" in db.keys():
        number -= 1
        delete_encouragment(number)
        encouragements = db["encouragements"]
    await responses_list(ctx)


async def new_response(ctx, message):
    update_encouragements(message)
    encouragements = []
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
    await ctx.send(f'New encouraging message added: {message}')
    await responses_list(ctx)


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