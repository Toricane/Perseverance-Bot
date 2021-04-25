from PyDictionary import PyDictionary
import asyncio
from cmds.words import words


async def pls_define(ctx, word):  # noqa: C901
    if words(word) == False:
        dictionary = PyDictionary()
        try:
            defined = dictionary.meaning(f"{word}")
            if defined.get('Noun', 99) != 99:
                bye1 = defined['Noun']
                await ctx.send("Noun meaning(s):")
                for i in range(0, len(bye1)):
                    await asyncio.sleep(1)
                    await ctx.channel.send(f"{i+1}. {bye1[i]}")
            if defined.get('Verb', 99) != 99:
                bye2 = defined['Verb']
                await ctx.send("Verb meaning(s):")
                for i in range(0, len(bye2)):
                    await asyncio.sleep(1)
                    await ctx.channel.send(f"{i+1}. {bye2[i]}")
            if defined.get('Pronoun', 99) != 99:
                bye3 = defined['Pronoun']
                await ctx.send("Pronoun meaning(s):")
                for i in range(0, len(bye3)):
                    await asyncio.sleep(1)
                    await ctx.channel.send(f"{i+1}. {bye3[i]}")
            if defined.get('Adjective', 99) != 99:
                bye4 = defined['Adjective']
                await ctx.send("Adjective meaning(s):")
                for i in range(0, len(bye4)):
                    await asyncio.sleep(1)
                    await ctx.channel.send(f"{i+1}. {bye4[i]}")
            if defined.get('Adverb', 99) != 99:
                bye5 = defined['Adverb']
                await ctx.send("Adverb meaning(s):")
                for i in range(0, len(bye5)):
                    await asyncio.sleep(1)
                    await ctx.channel.send(f"{i+1}. {bye5[i]}")
            if defined.get('Preposition', 99) != 99:
                bye6 = defined['Preposition']
                await ctx.send("Preposition meaning(s):")
                for i in range(0, len(bye6)):
                    await asyncio.sleep(1)
                    await ctx.channel.send(f"{i+1}. {bye6[i]}")
            if defined.get('Conjunction', 99) != 99:
                bye7 = defined['Conjunction']
                await ctx.channel.send("Conjunction meaning(s):")
                for i in range(0, len(bye7)):
                    await asyncio.sleep(1)
                    await ctx.send(f"{i+1}. {bye7[i]}")
            if defined.get('Interjection', 99) != 99:
                bye8 = defined['Interjection']
                await ctx.channel.send("Interjection meaning(s):")
                for i in range(0, len(bye8)):
                    await asyncio.sleep(1)
                    await ctx.send(f"{i+1}. {bye8[i]}")
            if defined.get('Numeral', 99) != 99:
                bye9 = defined['Numeral']
                await ctx.channel.send("Numeral meaning(s):")
                for i in range(0, len(bye9)):
                    await asyncio.sleep(1)
                    await ctx.send(f"{i+1}. {bye9[i]}")
            if defined.get('Article', 99) != 99:
                bye10 = defined['Article']
                await ctx.send("Article meaning(s):")
                for i in range(0, len(bye10)):
                    await asyncio.sleep(1)
                    await ctx.channel.send(f"{i+1}. {bye10[i]}")
            if defined.get('Determiner', 99) != 99:
                bye11 = defined['Determiner']
                await ctx.send("Determiner meaning(s):")
                for i in range(0, len(bye11)):
                    await asyncio.sleep(1)
                    await ctx.channel.send(f"{i+1}. {bye11[i]}")
            else:
                pass
        except Exception:
            await ctx.send(f"`{word.capitalize()}` is not in this dictionary.")
    elif ctx.channel.is_nsfw() == True:
        dictionary = PyDictionary()
        try:
            defined = dictionary.meaning(f"{word}")
            if defined.get('Noun', 99) != 99:
                bye1 = defined['Noun']
                await ctx.send("Noun meaning(s):")
                for i in range(0, len(bye1)):
                    await asyncio.sleep(1)
                    await ctx.channel.send(f"{i+1}. {bye1[i]}")
            if defined.get('Verb', 99) != 99:
                bye2 = defined['Verb']
                await ctx.send("Verb meaning(s):")
                for i in range(0, len(bye2)):
                    await asyncio.sleep(1)
                    await ctx.channel.send(f"{i+1}. {bye2[i]}")
            if defined.get('Pronoun', 99) != 99:
                bye3 = defined['Pronoun']
                await ctx.send("Pronoun meaning(s):")
                for i in range(0, len(bye3)):
                    await asyncio.sleep(1)
                    await ctx.channel.send(f"{i+1}. {bye3[i]}")
            if defined.get('Adjective', 99) != 99:
                bye4 = defined['Adjective']
                await ctx.send("Adjective meaning(s):")
                for i in range(0, len(bye4)):
                    await asyncio.sleep(1)
                    await ctx.channel.send(f"{i+1}. {bye4[i]}")
            if defined.get('Adverb', 99) != 99:
                bye5 = defined['Adverb']
                await ctx.send("Adverb meaning(s):")
                for i in range(0, len(bye5)):
                    await asyncio.sleep(1)
                    await ctx.channel.send(f"{i+1}. {bye5[i]}")
            if defined.get('Preposition', 99) != 99:
                bye6 = defined['Preposition']
                await ctx.send("Preposition meaning(s):")
                for i in range(0, len(bye6)):
                    await asyncio.sleep(1)
                    await ctx.channel.send(f"{i+1}. {bye6[i]}")
            if defined.get('Conjunction', 99) != 99:
                bye7 = defined['Conjunction']
                await ctx.channel.send("Conjunction meaning(s):")
                for i in range(0, len(bye7)):
                    await asyncio.sleep(1)
                    await ctx.send(f"{i+1}. {bye7[i]}")
            if defined.get('Interjection', 99) != 99:
                bye8 = defined['Interjection']
                await ctx.channel.send("Interjection meaning(s):")
                for i in range(0, len(bye8)):
                    await asyncio.sleep(1)
                    await ctx.send(f"{i+1}. {bye8[i]}")
            if defined.get('Numeral', 99) != 99:
                bye9 = defined['Numeral']
                await ctx.channel.send("Numeral meaning(s):")
                for i in range(0, len(bye9)):
                    await asyncio.sleep(1)
                    await ctx.send(f"{i+1}. {bye9[i]}")
            if defined.get('Article', 99) != 99:
                bye10 = defined['Article']
                await ctx.send("Article meaning(s):")
                for i in range(0, len(bye10)):
                    await asyncio.sleep(1)
                    await ctx.channel.send(f"{i+1}. {bye10[i]}")
            if defined.get('Determiner', 99) != 99:
                bye11 = defined['Determiner']
                await ctx.send("Determiner meaning(s):")
                for i in range(0, len(bye11)):
                    await asyncio.sleep(1)
                    await ctx.channel.send(f"{i+1}. {bye11[i]}")
            else:
                pass
        except Exception:
            await ctx.send(f"`{word.capitalize()}` is not in this dictionary.")
    else:
        await ctx.send("You can only send NSFW things in NSFW channels.")
