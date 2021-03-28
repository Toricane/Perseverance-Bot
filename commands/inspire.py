import aiohttp
import json


async def get_quote():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://zenquotes.io/api/random') as resp:
            json_data = json.loads(await resp.text())
            quote = '"' + json_data[0]['q'] + '" - ' + json_data[0]['a']
            return (quote)


async def inspire(ctx):
    print(f"{ctx.author.name}: /inspire")
    await ctx.defer()
    quote = await get_quote()
    await ctx.send(quote)
