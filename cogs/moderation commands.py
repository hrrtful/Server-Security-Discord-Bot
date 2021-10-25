import json

import discord
import time
from discord.ext import commands
from Tools.utils import getGuildPrefix, getConfig, updateConfig


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(usage="[#channel/id]")
    @commands.has_permissions(manage_messages=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f"{channel.mention} locked!")

    @commands.command(usage="[#channel/id]")
    @commands.has_permissions(manage_messages=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f"{channel.mention} unlocked!")

    @commands.command(name="kick",
                      usage="<member> [reason]")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        if member.id == ctx.author.id:
            await ctx.send("You cannot kick yourself!")
            return

        await member.kick(reason=reason)

        await ctx.message.delete()
        kick = discord.Embed(description=f"**A member has been kicked.**\n\n"
                                          f"Moderator: {ctx.author.mention}\n"
                                          f"Member: {member.mention}", colour=discord.Colour.blue())
        kick.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=kick)

    @commands.command(usage="<member> [reason]")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        if member.id == ctx.author.id:
            await ctx.send("You cannot ban yourself!")
            return

        await member.ban(reason=reason, delete_message_days=0)
        ban = discord.Embed(description=f"**A member has been banned.**\n\n"
                                        f"Moderator: {ctx.author.mention}\n"
                                        f"Member: {member.mention}", colour=discord.Colour.blue())
        ban.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=ban)

    @commands.command(usage="<id>")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, user_id: int):
        user = await self.client.fetch_user(user_id)
        await ctx.guild.unban(user)
        unban = discord.Embed(description=f"**A user has been unbanned.**\n\n"
                                          f"Moderator: {ctx.author.mention}\n"
                                          f"Member: {user.mention}", colour=discord.Colour.blue())
        await ctx.send(embed=unban)

    @commands.command(usage="number")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=0):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"I have cleared **{amount}** messages.", delete_after=3)

    @commands.command(usage="<member> [reason]")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, *, reason="No reason provided"):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True,
                                              read_messages=False)
        mute = discord.Embed(description=f"**A member has been muted.**\n\n"
                                         f"Moderator: {ctx.author.mention}\n"
                                         f"Member: {member.mention}", colour=discord.Colour.blue())
        mute.add_field(name="Reason", value=reason)
        await member.add_roles(mutedRole, reason=reason)
        await ctx.send(embed=mute)

    @commands.command(usage="<member>")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

        await member.remove_roles(mutedRole)
        unmute = discord.Embed(description=f"**A member has been unmuted.**\n\n"
                                           f"Moderator: {ctx.author.mention}\n"
                                           f"Member: {member.mention}", colour=discord.Colour.blue())
        await ctx.send(embed=unmute)


    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def nuke(self, ctx):
        channelthings = [ctx.channel.category, ctx.channel.position]
        await ctx.channel.clone()
        await ctx.channel.delete()
        nukedchannel = channelthings[0].text_channels[-1]
        await nukedchannel.edit(position=channelthings[1])
        await nukedchannel.send(f"Channel was nuked by {ctx.author.mention}")

    @commands.command(usage="add/remove <member> <role>")
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, addORremove, member: discord.Member, role: discord.Role):

        addORremove = addORremove.lower()

        if addORremove == 'add':

            if role == ctx.author.top_role:
                return await ctx.send("That role has the same position as your top role!")

            if role in member.roles:
                return await ctx.send("The member already has this role assigned!")

            if role.position >= ctx.guild.me.top_role.position:
                return await ctx.send(f"This role is higher than my role, move it to the top!")

            await member.add_roles(role)
            await ctx.send(f"I have added {member.mention} the role {role.mention}")

        if addORremove == 'remove':

            if role == ctx.author.top_role:
                return await ctx.send("That role has the same position as your top role!")

            if role not in member.roles:
                return await ctx.send("The member does not have this role!")

            if role.position >= ctx.guild.me.top_role.position:
                return await ctx.send(f"This role is higher than my role, move it to the top!")

            await member.remove_roles(role)
            await ctx.send(f"I have removed {member.mention} the role {role.mention}")


def setup(client):
    client.add_cog(Moderation(client))
