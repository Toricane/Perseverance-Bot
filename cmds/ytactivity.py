import os
import json
import aiohttp

async def get_activity(url, api_json, headers):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=api_json, headers=headers) as response:
            data = json.loads(await response.text())
            code = data["code"]
            return code


async def group_say(ctx, activity_type):
    if ctx.author.voice:
        url = f"https://discord.com/api/v8/channels/{ctx.author.voice.channel.id}/invites"
        api_json = {
            "max_age": 86400,
            "max_uses": 0,
            "target_application_id": f"{activity_type}",
            "target_type": 2,
            "temporary": False,
            "validate": None
            }
        headers = {
            "Authorization": f"Bot {os.getenv('TOKEN')}",
            "Content-Type": "application/json"
            }

        code = await get_activity(url, api_json, headers)
        if str(code) == "50013":
            await ctx.send("You must be in a Voice Channel without a member limit.")
        else:
            await ctx.send(f"https://discord.gg/{code} Click on the link to join.")
    else:
        await ctx.send("In order to use this command, you must be in a Voice Channel.")