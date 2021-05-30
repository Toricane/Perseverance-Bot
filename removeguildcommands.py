from discord_slash.utils.manage_commands import remove_all_commands_in
from replit import db
import asyncio

guild_ids = db["id"]

async def func():
    for guild in guild_ids:
        await remove_all_commands_in(811277990913769523, "token", guild_id=guild)
        print("done")

asyncio.run(func())