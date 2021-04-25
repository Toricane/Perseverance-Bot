import requests
import discord
import os
import json

async def group_say(ctx, channel):
    print(channel.type)
    if ctx.author.voice:
        if channel.type == discord.ChannelType.voice:
            url = f"https://discord.com/api/v8/channels/{channel.id}/invites"
            api_json = {
                "max_age": 86400,
                "max_uses": 0,
                "target_application_id": "755600276941176913",
                "target_type": 2,
                "temporary": False,
                "validate": None
                }
            headers = {
                            "Authorization": f"Bot {os.getenv('TOKEN')}",
                            "Content-Type": "application/json"
                        }
            api_return = requests.post(url, json=api_json, headers=headers)
            data = json.loads(api_return.text)
            code = data["code"]
            await ctx.send(f"https://discord.gg/{code} Click on the link to join.")   
        else:
            await ctx.send(hidden=True, content="Please select a voice channel.")
    else:
        await ctx.send(hidden=True, content="You need to be in a voice channel.")