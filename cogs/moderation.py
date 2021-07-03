import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from log import used, error

class Moderation(commands.Cog, description="Moderation tools for your server!"):
    def __init__(self, bot):
        self.bot = bot
    
    # addrole:
    @commands.command(aliases=["ar"], help="Add a role to a member.\nRequires Manage Roles permission.")
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, member: discord.Member, role: discord.Role):
        await used(f"{ctx.author.name}#{ctx.author.discriminator}: \\addrole {member} {role}")
        await member.add_roles(role)
        await ctx.send(f"{member.mention} got the {role} role.")

    @cog_ext.cog_slash(name="addrole", description="Adds a role")
    @commands.has_permissions(manage_roles=True)
    async def _addrole(self, ctx: SlashContext, member: discord.Member, role: discord.Role):
        await used(f"{ctx.author.name}#{ctx.author.discriminator}: /addrole {member} {role}")
        await member.add_roles(role)
        await ctx.send(f"{member.mention} got the {role} role.")

    # removerole:
    @commands.command(aliases=["rr"], help="Remove a role from someone.\nRequires Manage Roles permission.")
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, member: discord.Member, role: discord.Role):
        await used(f"{ctx.author.name}#{ctx.author.discriminator}: \\removerole {member} {role}")
        await member.remove_roles(role)
        await ctx.send(f"{member.mention} lost the {role} role.")

    @cog_ext.cog_slash(name="removerole", description="Removes a role")
    @commands.has_permissions(manage_roles=True)
    async def _removerole(self, ctx: SlashContext, member: discord.Member, role: discord.Role):
        await used(f"{ctx.author.name}#{ctx.author.discriminator}: /removerole {member} {role}")
        await member.remove_roles(role)
        await ctx.send(f"{member.mention} lost the {role} role.")

    # kick:
    @commands.command(help="Kick a member.\nRequires Kick Members permission.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await used(f"{ctx.author.name}#{ctx.author.discriminator}: \\kick {member} {reason}")
        await member.kick(reason=f"{ctx.author.name}#{ctx.author.discriminator}: {reason}")
        await ctx.send(f"{ctx.author.name}#{ctx.author.discriminator} kicked {member.mention} because {reason}.")

    @cog_ext.cog_slash(name="kick", description="Kicks a member")
    @commands.has_permissions(kick_members=True)
    async def _kick(self, ctx: SlashContext, member: discord.Member, *, reason=None):
        await used(f"{ctx.author.name}#{ctx.author.discriminator}: /kick {member} {reason}")
        await member.kick(reason=f"{ctx.author.name}#{ctx.author.discriminator}: {reason}")
        await ctx.send(f"{ctx.author.name}#{ctx.author.discriminator} kicked {member.mention} because {reason}.")

    # ban:
    @commands.command(help="Ban someone.\nRequires Ban Users permission.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await used(f"{ctx.author.name}#{ctx.author.discriminator}: \\ban {member} {reason}")
        await member.ban(reason=f"{ctx.author.name}#{ctx.author.discriminator}: {reason}")
        await ctx.send(f"{ctx.author.name}#{ctx.author.discriminator} banned {member.mention} because {reason}.")

    @cog_ext.cog_slash(name="ban", description="Bans a member")
    @commands.has_permissions(ban_members=True)
    async def _ban(self, ctx: SlashContext, member: discord.Member, reason=None):
        await used(f"{ctx.author.name}#{ctx.author.discriminator}: /ban {member} {reason}")
        await member.ban(reason=f"{ctx.author.name}#{ctx.author.discriminator}: {reason}")
        await ctx.send(f"{ctx.author.name}#{ctx.author.discriminator} banned {member.mention} because {reason}.")

    #unban:
    @commands.command(help="Unban someone.\nRequires Ban Members permission.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member):
        await used(f"{ctx.author.name}#{ctx.author.discriminator}: \\unban {member}")
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name,
                                                member_discriminator):
                await ctx.guild.unban(user)
                person = f"{user.name}#{user.discriminator}"
                await ctx.send(f"Unbanned {person}.")
                return

    @cog_ext.cog_slash(
        name="unban",
        description="Unbans a member",
        options=[
            create_option(name="member",
                        description="Add the member name here",
                        option_type=3,
                        required=True)
        ],
    )
    @commands.has_permissions(ban_members=True)
    async def _unban(self, ctx, member):
        await used(f"{ctx.author.name}#{ctx.author.discriminator}: /unban {member}")
        await ctx.defer()
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name,
                                                member_discriminator):
                await ctx.guild.unban(user)
                person = f"{user.name}#{user.discriminator}"
                await ctx.send(f"Unbanned {person}.")
                return
    
    # nick:
    @commands.command(aliases=["nickname"], help="Change someone's nickname.\nRequires Manage Nicknames permission.")
    @commands.has_permissions(manage_nicknames=True)
    async def nick(ctx, member: discord.Member, *, nick):
        await used(f"{ctx.author.name}#{ctx.author.discriminator}: \\nick {member} {nick}")
        try:
            await member.edit(nick=nick)
            await ctx.send(f'Nickname was changed for {member.mention}.')
        except Exception:
            await ctx.send("I am missing `Manage Nicknames` permission.")

    @cog_ext.cog_slash(
        name="nick",
        description="Sends a reciprocal of a fraction",
        options=[
            create_option(name="member",
                        description="Type member here",
                        option_type=6,
                        required=True),
            create_option(name="nick",
                        description="Type new nick here",
                        option_type=3,
                        required=True)
        ],
    )
    @commands.has_permissions(manage_nicknames=True)
    async def _nick(ctx, member: discord.Member, nick):
        await used(f"{ctx.author.name}#{ctx.author.discriminator}: /nick {member} {nick}")
        try:
            await member.edit(nick=nick)
            await ctx.send(f'Nickname was changed for {member.mention}.')
        except Exception:
            await ctx.send("I am missing `Manage Nicknames` permission.")


def setup(bot):
    bot.add_cog(Moderation(bot))