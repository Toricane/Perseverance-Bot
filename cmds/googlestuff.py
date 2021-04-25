import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from googletrans import Translator
from cmds.words import words
import asyncio

LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu'
}


def googleSearch(query):
    query = query.replace(" ", "+")
    g_clean = []
    if "http" not in query:
        url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(
            query)
    else:
        url = query
    try:
        html = requests.get(url)
        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'lxml')
            a = soup.find_all('a')
            for i in a:
                k = i.get('href')
                try:
                    m = re.search("(?P<url>https?://[^\s]+)", k)
                    n = m.group(0)
                    rul = n.split('&')[0]
                    domain = urlparse(rul)
                    if (re.search('google.com', domain.netloc)):
                        continue
                    else:
                        g_clean.append(rul)
                except:
                    continue
    except Exception as ex:
        print(str(ex))
    finally:
        del g_clean[10:100]
        return g_clean


def googleSearchImages(query):
    query = query.replace(" ", "+")
    g_clean = []
    if "http" not in query:
        url = 'https://www.google.com/search?hl=en&tbm=isch&sxsrf=ALeKk01Eh6GNz2vJrxJ-7rB-HY2SE-4xJQ%3A1615321310276&source=hp&biw=1366&bih=657&ei=3thHYNbEDpLZ-gSE-b6oCg&q={}&oq={}&gs_lcp=CgNpbWcQAzIFCAAQsQMyBQgAELEDMgUIABCxAzICCAAyBQgAELEDMgIIADIFCAAQsQMyBQgAELEDMgIIADIFCAAQsQM6BwgjEOoCECc6BAgjECc6CAgAELEDEIMBUOaYC1jTmwtgzJ0LaAFwAHgAgAFiiAHcAZIBATOYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABCg&sclient=img&ved=0ahUKEwjWq5TnhKTvAhWSrJ4KHYS8D6UQ4dUDCAc&uact=5'.format(
            query, query)
    else:
        url = query
    try:
        html = requests.get(url)
        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'lxml')
            a = soup.find_all('a')
            for i in a:
                k = i.get('href')
                try:
                    m = re.search("(?P<url>https?://[^\s]+)", k)
                    n = m.group(0)
                    rul = n.split('&')[0]
                    domain = urlparse(rul)
                    if (re.search('google.com', domain.netloc)):
                        continue
                    else:
                        g_clean.append(rul)
                except:
                    continue
    except Exception as ex:
        print(str(ex))
    finally:
        del g_clean[10:100]
        return g_clean


async def pls_google(ctx, text, results): # noqa: C901
    if words(text) == False:
        result = googleSearch(text)
        results = int(results)
        try:
            a, b, c, d, e, f, g, h, i, j = result
            alphabet = [a, b, c, d, e, f, g, h, i, j]
        except:
            a, b, c, d, e, f, g, h, i = result
            alphabet = [a, b, c, d, e, f, g, h, i]
        if results > 10:
            await ctx.send("Results must be between 1 and 10")
            return False
        await ctx.send("Results:")
        await asyncio.sleep(1)
        for x in range(0, results):
            if words(alphabet[x]) == False:
                await ctx.channel.send(alphabet[x])
                await asyncio.sleep(1)
        query = text.replace(" ", "+")
        if "http" not in query:
            url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(
                query)
        else:
            url = query
        if words(url) == False:
            await ctx.channel.send(f"URL: {url}")
    elif ctx.channel.is_nsfw() == True:
        result = googleSearch(text)
        results = int(results)
        try:
            a, b, c, d, e, f, g, h, i, j = result
            alphabet = [a, b, c, d, e, f, g, h, i, j]
        except:
            a, b, c, d, e, f, g, h, i = result
            alphabet = [a, b, c, d, e, f, g, h, i]
        if results > 10:
            await ctx.send("Results must be between 1 and 10")
            return False
        await ctx.send("Results:")
        await asyncio.sleep(1)
        for x in range(0, results):
            if words(alphabet[x]) == False:
                await ctx.channel.send(alphabet[x])
                await asyncio.sleep(1)
        query = text.replace(" ", "+")
        if "http" not in query:
            url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(
                query)
        else:
            url = query
        if words(url) == False:
            await ctx.channel.send(f"URL: {url}")
    else:
        await ctx.send("You can only search NSFW things in an NSFW channel.")


async def pls_googleimages(ctx, text, results): # noqa: C901
    if words(text) == False:
        result = googleSearchImages(text)
        results = int(results)
        try:
            a, b, c, d, e, f, g, h, i, j = result
            alphabet = [a, b, c, d, e, f, g, h, i, j]
        except:
            a, b, c, d, e, f, g, h, i = result
            alphabet = [a, b, c, d, e, f, g, h, i]
        if results > 10:
            await ctx.send("Results must be between 1 and 10")
            return False
        await ctx.send("Results:")
        await asyncio.sleep(1)
        for x in range(0, results):
            if words(alphabet[x]) == False:
                await ctx.channel.send(alphabet[x])
                await asyncio.sleep(1)
        query = text.replace(" ", "+")
        if "http" not in query:
            url = 'https://www.google.com/search?hl=en&tbm=isch&sxsrf=ALeKk01Eh6GNz2vJrxJ-7rB-HY2SE-4xJQ%3A1615321310276&source=hp&biw=1366&bih=657&ei=3thHYNbEDpLZ-gSE-b6oCg&q={}&oq={}&gs_lcp=CgNpbWcQAzIFCAAQsQMyBQgAELEDMgUIABCxAzICCAAyBQgAELEDMgIIADIFCAAQsQMyBQgAELEDMgIIADIFCAAQsQM6BwgjEOoCECc6BAgjECc6CAgAELEDEIMBUOaYC1jTmwtgzJ0LaAFwAHgAgAFiiAHcAZIBATOYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABCg&sclient=img&ved=0ahUKEwjWq5TnhKTvAhWSrJ4KHYS8D6UQ4dUDCAc&uact=5'.format(
                query, query)
        else:
            url = query
        if words(url) == False:
            await ctx.channel.send(f"URL: {url}")
    elif ctx.channel.is_nsfw() == True:
        result = googleSearchImages(text)
        results = int(results)
        try:
            a, b, c, d, e, f, g, h, i, j = result
            alphabet = [a, b, c, d, e, f, g, h, i, j]
        except:
            a, b, c, d, e, f, g, h, i = result
            alphabet = [a, b, c, d, e, f, g, h, i]
        if results > 10:
            await ctx.send("Results must be between 1 and 10")
            return False
        await ctx.send("Results:")
        await asyncio.sleep(1)
        for x in range(0, results):
            if words(alphabet[x]) == False:
                await ctx.channel.send(alphabet[x])
                await asyncio.sleep(1)
        query = text.replace(" ", "+")
        if "http" not in query:
            url = 'https://www.google.com/search?hl=en&tbm=isch&sxsrf=ALeKk01Eh6GNz2vJrxJ-7rB-HY2SE-4xJQ%3A1615321310276&source=hp&biw=1366&bih=657&ei=3thHYNbEDpLZ-gSE-b6oCg&q={}&oq={}&gs_lcp=CgNpbWcQAzIFCAAQsQMyBQgAELEDMgUIABCxAzICCAAyBQgAELEDMgIIADIFCAAQsQMyBQgAELEDMgIIADIFCAAQsQM6BwgjEOoCECc6BAgjECc6CAgAELEDEIMBUOaYC1jTmwtgzJ0LaAFwAHgAgAFiiAHcAZIBATOYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABCg&sclient=img&ved=0ahUKEwjWq5TnhKTvAhWSrJ4KHYS8D6UQ4dUDCAc&uact=5'.format(
                query, query)
        else:
            url = query
        if words(url) == False:
            await ctx.channel.send(f"URL: {url}")
    else:
        await ctx.send("You can only search NSFW things in an NSFW channel.")


async def pls_translate(ctx, text, output_lang, input_lang):
    if words(text) == False:
        if input_lang == None:
            try:
                output_lang2 = output_lang
                translator = Translator()
                translated = translator.translate(text, dest=output_lang2)
                await ctx.send(f"{translated.text}")
            except Exception as e:
                print(str(e))
                await ctx.send("ERROR")
                await ctx.send("Make sure that your output_lang is one of these:")
                await ctx.send(f"{LANGUAGES}")
        else:
            try:
                output_lang2 = output_lang
                input_lang2 = input_lang
                translator = Translator()
                translated = translator.translate(text,
                                                src=input_lang2,
                                                dest=output_lang2)
                await ctx.send(f"{translated.text}")
            except Exception as e:
                print(str(e))
                await ctx.send("ERROR")
                await ctx.send(
                    "Make sure that your output_lang or input_lang is one of these:"
                )
                await ctx.send(f"{LANGUAGES}")
    elif ctx.channel.is_nsfw() == True:
        if input_lang == None:
            try:
                output_lang2 = output_lang
                translator = Translator()
                translated = translator.translate(text, dest=output_lang2)
                await ctx.send(f"{translated.text}")
            except Exception as e:
                print(str(e))
                await ctx.send("ERROR")
                await ctx.send("Make sure that your output_lang is one of these:")
                await ctx.send(f"{LANGUAGES}")
        else:
            try:
                output_lang2 = output_lang
                input_lang2 = input_lang
                translator = Translator()
                translated = translator.translate(text,
                                                src=input_lang2,
                                                dest=output_lang2)
                await ctx.send(f"{translated.text}")
            except Exception as e:
                print(str(e))
                await ctx.send("ERROR")
                await ctx.send(
                    "Make sure that your output_lang or input_lang is one of these:"
                )
                await ctx.send(f"{LANGUAGES}")
    else:
        await ctx.send("You can only search NSFW things in an NSFW channel.")