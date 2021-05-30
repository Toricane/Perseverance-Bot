from prsaw import RandomStuff
import os

api_key = f"{os.getenv('api_key')}"
rs = RandomStuff(async_mode=True, api_key=api_key)

async def ai_response(ctx, msg):
    response = await rs.get_ai_response(msg)
    await ctx.send(response)

async def get_a_joke(ctx, joke):
    response = await rs.get_joke(_type="any")
    await ctx.send(response)

async def get_image(ctx, joke, thing=None):
    if joke != None:
        response = await rs.get_image(_type=f"{thing}")
    else:
        print(joke)
        response = await rs.get_image(_type="any")
    await ctx.send(response)