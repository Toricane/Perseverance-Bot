import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
import youtube_dl, asyncio
from discord.utils import get

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address':
    '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {'options': '-vn'}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options),
                   data=data)



class VC(commands.Cog, description="Voice channel related commands!"):
    def __init__(self, bot):
        self.bot = bot
    
    # commands: play, stop
    @commands.command(help="Play a song in the VC!")
    async def play(self, ctx, *, url=None):
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send("You are not connected to a voice channel")
            return
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        await voice.disconnect()
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        if url != None:
            """Plays from a url (almost anything youtube_dl supports)"""

            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
                ctx.voice_client.play(player,
                                    after=lambda e: print('Player error: %s' % e)
                                    if e else None)

            url_thumb = f"https://i.ytimg.com/vi/{url.replace('https://www.youtube.com/watch?v=', '')}/maxresdefault.jpg"

            embed = discord.Embed(colour=discord.Colour.orange())
            embed.add_field(
                name="▶️ Now playing",
                value=
                f"[{player.title}]({url}) [<@{ctx.author.id}>]\nJoin VC <#{channel.id}>",
                inline=False)
            if "https://www.youtube.com/watch?v=" in url:
                embed.set_thumbnail(url=url_thumb)
            embed.set_footer(
                text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}.")
            await ctx.send(embed=embed)
            while ctx.voice_client.is_playing() == True:
                await asyncio.sleep(1)
            await asyncio.sleep(1)
            await voice.disconnect()

            embed = discord.Embed(colour=discord.Colour.orange())
            embed.add_field(name="⏹️ Stopped and left",
                            value=f"<#{channel.id}>",
                            inline=False)
            embed.set_footer(
                text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}.")
            await ctx.send(embed=embed)

        else:
            await ctx.send("Please send a URL in the command!")
    

    @cog_ext.cog_slash(name="_play", description="Play a song in the VC!")
    async def _play(self, ctx, *, url=None):
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send("You are not connected to a voice channel")
            return
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        await voice.disconnect()
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        if url != None:
            """Plays from a url (almost anything youtube_dl supports)"""

            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
                ctx.voice_client.play(player,
                                    after=lambda e: print('Player error: %s' % e)
                                    if e else None)

            url_thumb = f"https://i.ytimg.com/vi/{url.replace('https://www.youtube.com/watch?v=', '')}/maxresdefault.jpg"

            embed = discord.Embed(colour=discord.Colour.orange())
            embed.add_field(
                name="▶️ Now playing",
                value=
                f"[{player.title}]({url}) [<@{ctx.author.id}>]\nJoin VC <#{channel.id}>",
                inline=False)
            if "https://www.youtube.com/watch?v=" in url:
                embed.set_thumbnail(url=url_thumb)
            embed.set_footer(
                text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}.")
            await ctx.send(embed=embed)
            while ctx.voice_client.is_playing() == True:
                await asyncio.sleep(1)
            await asyncio.sleep(1)
            await voice.disconnect()

            embed = discord.Embed(colour=discord.Colour.orange())
            embed.add_field(name="⏹️ Stopped and left",
                            value=f"<#{channel.id}>",
                            inline=False)
            embed.set_footer(
                text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}.")
            await ctx.send(embed=embed)

        else:
            await ctx.send("Please send a URL in the command!")


    @commands.command(help="Stop a song from playing in the VC, and make the bot leave!")
    async def stop(self, ctx):
        await ctx.send(ctx)
        try:
            channelid = ctx.message.author.voice.channel.id
            await ctx.voice_client.disconnect()
            embed = discord.Embed(colour=discord.Colour.orange())
            embed.add_field(name="⏹️ Stopped and left",
                            value=f"<#{channelid}>",
                            inline=False)
            embed.set_footer(
                text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}.")
            await ctx.send(embed=embed)
        except:
            if ctx.author.voice == None:
                await ctx.send("You are not in a voice channel!")
            else:
                await ctx.send("The bot is not in a voice channel!")
    

    @cog_ext.cog_slash(name="stop", description="Stop a song from playing in the VC, and make the bot leave!")
    async def _stop(self, ctx):
        await ctx.send(ctx)
        try:
            channelid = ctx.message.author.voice.channel.id
            await ctx.voice_client.disconnect()
            embed = discord.Embed(colour=discord.Colour.orange())
            embed.add_field(name="⏹️ Stopped and left",
                            value=f"<#{channelid}>",
                            inline=False)
            embed.set_footer(
                text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}.")
            await ctx.send(embed=embed)
        except:
            if ctx.author.voice == None:
                await ctx.send("You are not in a voice channel!")
            else:
                await ctx.send("The bot is not in a voice channel!")


def setup(bot):
    bot.add_cog(VC(bot))