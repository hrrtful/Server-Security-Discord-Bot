import discord
import datetime
import asyncio

from Tools.utils import getConfig, getGuildPrefix, guild_owner_only, updateConfig
from Tools.logMessage import sendLogMessage
from discord.ext import commands


class Panicmode(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            try:
                data = getConfig(message.guild.id)
                panicmode = data["panicmode"]
                whitelist = data["whitelist"]
                owner = data["owner"]
                logChannel = data["logChannel"]
                panicpunishment = data["panicpunishment"]
                if panicmode is True:
                    if message.author.id == 882901345466724373:
                        return
                    if message.author.id in whitelist:
                        return
                    if message.author.id == owner:
                        return
                    await message.delete()
                    if panicpunishment == "kick":
                        await message.author.kick(reason="Server Security Panic-Mode")
                        time = datetime.datetime.now()
                        now = round(time.timestamp())
                        embed = discord.Embed(title=f"{message.author} has been kicked", colour=discord.Colour.blue())
                        embed.add_field(name="Reason", value=f"Server Security Panic-Mode", inline=False)
                        embed.add_field(name="User ID", value=f"{message.author.id}", inline=False)
                        embed.add_field(name="Date", value=f"<t:{now}:F>", inline=False)
                        await sendLogMessage(self, event=message, channel=logChannel, embed=embed)

                    if panicpunishment == "ban":
                        await message.author.ban(reason="Server Security Panic-Mode")
                        time = datetime.datetime.now()
                        now = round(time.timestamp())
                        embed = discord.Embed(title=f"{message.author} has been banned", colour=discord.Colour.blue())
                        embed.add_field(name="Reason", value=f"Server Security Panic-Mode", inline=False)
                        embed.add_field(name="User ID", value=f"{message.author.id}", inline=False)
                        embed.add_field(name="Date", value=f"<t:{now}:F>", inline=False)
                        await sendLogMessage(self, event=message, channel=logChannel, embed=embed)

                    if panicpunishment == "mute":
                        mutedRole = discord.utils.get(message.guild.roles, name="Muted")
                        await message.author.add_roles(mutedRole)
                        time = datetime.datetime.now()
                        now = round(time.timestamp())
                        embed = discord.Embed(title=f"{message.author} has been silenced", colour=discord.Colour.blue())
                        embed.add_field(name="Reason", value=f"Server Security Panic-Mode", inline=False)
                        embed.add_field(name="User ID", value=f"{message.author.id}", inline=False)
                        embed.add_field(name="Date", value=f"<t:{now}:F>", inline=False)
                        await sendLogMessage(self, event=message, channel=logChannel, embed=embed)
                        await asyncio.sleep(3600)
                        await message.author.remove_roles(mutedRole)
            except AttributeError:
                pass
        except discord.errors.NotFound:
            pass




def setup(client):
    client.add_cog(Panicmode(client))