from discord_slash.utils.manage_commands import remove_all_commands_in
from replit import db
import asyncio

guild_ids = db["id"]

async def func():
    for guild in guild_ids:
        await remove_all_commands_in(811277990913769523, "token", guild_id=guild)
        print("done")
    

# async def func():
#     await remove_all_commands_in(811277990913769523, "Token goes here", guild_id=820419188866547712)
#     print("done")

asyncio.run(func())