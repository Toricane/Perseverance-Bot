import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Moderation(commands.Cog, description="Moderation tools for your server!"):
    def __init__(self, bot):
        self.bot = bot
    
    # addrole:
    @commands.command(aliases=["ar"], help="Add a role to a member.\nRequires Manage Roles permission.")
    @commands.has_permissions(manage_roles=True)
    async def addrole(ctx, member: discord.Member, role: discord.Role):
        await member.add_roles(role)
        await ctx.send(f"{member.mention} got the {role} role.")

    @cog_ext.cog_slash(name="addrole", description="Adds a role")
    @commands.has_permissions(manage_roles=True)
    async def _addrole(ctx: SlashContext, member: discord.Member, role: discord.Role):
        await ctx.defer()
        await member.add_roles(role)
        await ctx.send(f"{member.mention} got the {role} role.")

    # removerole:
    @commands.command(aliases=["rr"], help="Remove a role from someone.\nRequires Manage Roles permission.")
    @commands.has_permissions(manage_roles=True)
    async def removerole(ctx, member: discord.Member, role: discord.Role):
        await member.remove_roles(role)
        await ctx.send(f"{member.mention} lost the {role} role.")

    @cog_ext.cog_slash(name="removerole", description="Removes a role")
    @commands.has_permissions(manage_roles=True)
    async def _removerole(ctx: SlashContext, member: discord.Member, role: discord.Role):
        await ctx.defer()
        await member.remove_roles(role)
        await ctx.send(f"{member.mention} lost the {role} role.")

    # kick:
    @commands.command(help="Kick a member.\nRequires Kick Members permission.")
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member} because {reason}.")

    @cog_ext.cog_slash(name="kick", description="Kicks a member")
    @commands.has_permissions(kick_members=True)
    async def _kick(ctx: SlashContext, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member} because {reason}.")

    # ban:
    @commands.command(help="Ban someone.\nRequires Ban Users permission.")
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member.mention} because {reason}.")

    @cog_ext.cog_slash(name="ban", description="Bans a member")
    @commands.has_permissions(ban_members=True)
    async def _ban(ctx: SlashContext, member: discord.Member, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member.mention} because {reason}.")

    #unban:
    @commands.command(help="Unban someone.\nRequires Ban Members permission.")
    @commands.has_permissions(ban_members=True)
    async def unban(ctx, member):
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
    async def _unban(ctx, member):
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

def setup(bot):
    bot.add_cog(Moderation(bot))