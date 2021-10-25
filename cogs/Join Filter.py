import discord
from discord.ext import commands
from Tools.utils import getConfig, getGuildPrefix, updateConfig
from datetime import datetime
from Tools.logMessage import sendLogMessage


class AntiRaid(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        data = getConfig(member.guild.id)
        punishment = data["punishment"]
        logChannel = data["logChannel"]
        if data["joinfilter"] is True:
            if data["botfilter"] is True:
                if member.bot:
                    if punishment == "kick":
                        punishment = "kicked"
                        await member.kick(reason=f"Server Security Join-Filter | Bot joined the server")

                    if punishment == "ban":
                        punishment = "banned"
                        await member.ban(reason=f"Server Security Join-Filter | Bot joined the server")

                    if punishment == "none":
                        pass

                    time = datetime.datetime.now()
                    now = round(time.timestamp())
                    embed = discord.Embed(title=f"{member} has been {punishment}", color=discord.Colour.blue())
                    embed.add_field(name="Reason", value=f"Server Security Join-Filter | Bot joined the server", inline=False)
                    embed.add_field(name="Date", value=f"<t:{now}:F>\n", inline=False)
                    embed.set_thumbnail(url=member.avatar_url)
                    await sendLogMessage(self, event=member, embed=embed, channel=logChannel)

                else:
                    pass

            if data["avatarfilter"] is True:
                if member.avatar == None:
                    if punishment == "kick":
                        punishment = "kicked"
                        await member.kick(reason="Server Security Join-Filter | User has no custom avatar")
                        try:
                            await member.send("Server Security Join-Filter |  You need a custom profile picture to join the server!")
                        except discord.errors.Forbidden:
                            return
                    if punishment == "ban":
                        punishment = "banned"
                        await member.ban(reason="Server Security Join-Filter | User has no custom avatar")
                        try:
                            await member.send("Server Security Join-Filter | You need a custom profile picture to join the server!")
                        except discord.errors.Forbidden:
                            return
                    if punishment == "none":
                        pass

                    time = datetime.datetime.now()
                    now = round(time.timestamp())
                    embed = discord.Embed(title=f"{member} has been {punishment}", color=discord.Colour.blue())
                    embed.add_field(name="Reason", value=f"Server Security Join-Filter | User has no custom avatar", inline=False)
                    embed.add_field(name="Date", value=f"<t:{now}:F>\n", inline=False)
                    embed.set_thumbnail(url=member.avatar_url)
                    await sendLogMessage(self, event=member, embed=embed, channel=logChannel)
                else:
                    pass

            if data["autoban"] is True:
                await member.ban(reason="Server Security | Auto-Ban")

                time = datetime.datetime.now()
                now = round(time.timestamp())
                embed = discord.Embed(title=f"{member} has been banned", color=discord.Colour.blue())
                embed.add_field(name="Reason", value=f"Server Security Join-Filter | Auto-Ban",
                                inline=False)
                embed.add_field(name="Date", value=f"<t:{now}:F>\n", inline=False)
                embed.set_thumbnail(url=member.avatar_url)
                await sendLogMessage(self, event=member, embed=embed, channel=logChannel)

            if data["checknew"] is True:
                maxpoints = data["points"]
                points = 0
                member_days = (datetime.utcnow() - member.created_at).days
                if member_days <= 5:
                    points += 30
                elif member_days <= 15:
                    points += 20
                elif member_days <= 30:
                    points += 10
                elif member_days <= 80:
                    points += 5
                url = member.avatar_url
                if "/embed/" in str(url).lower():
                    points += 15
                if "gg/" in member.name:
                    points += 30
                if points >= int(maxpoints):
                    if punishment == 'kick':
                        punishment = 'kicked'
                        await member.kick(reason="Server Security Join-Filter | This user has reached the minimum number of points and was kicked from the server.")

                        time = datetime.utcnow()
                        now = round(time.timestamp())
                        embed = discord.Embed(title=f"{member} has been {punishment}", color=discord.Colour.blue())
                        embed.add_field(name="Reason", value=f"Server Security Join-Filter | This user has reached the minimum number of points and was kicked from the server.",
                                        inline=False)
                        embed.add_field(name="Maximal Points", value=f"{maxpoints}", inline=False)
                        embed.add_field(name="Points", value=f"{points}", inline=False)
                        embed.add_field(name="Date", value=f"<t:{now}:F>\n", inline=False)
                        embed.set_thumbnail(url=member.avatar_url)
                        await sendLogMessage(self, event=member, embed=embed, channel=logChannel)

                    if punishment == 'ban':
                        punishment = 'banned'
                        await member.ban(reason="Server Security Join-Filter | This user has reached the minimum number of points and was banned from the server.")

                        time = datetime.utcnow()
                        now = round(time.timestamp())
                        embed = discord.Embed(title=f"{member} has been {punishment}", color=discord.Colour.blue())
                        embed.add_field(name="Reason",
                                        value=f"Server Security Join-Filter | This user has reached the minimum number of points and was banned from the server.",
                                        inline=False)
                        embed.add_field(name="Maximal Points", value=f"{maxpoints}", inline=False)
                        embed.add_field(name="Points", value=f"{points}", inline=False)
                        embed.add_field(name="Date", value=f"<t:{now}:F>\n", inline=False)
                        embed.set_thumbnail(url=member.avatar_url)
                        await sendLogMessage(self, event=member, embed=embed, channel=logChannel)

                    if punishment == 'none':
                        punishment = 'kicked'
                        await member.kick(reason="Server Security Join-Filter | This user has reached the minimum number of points and was kicked from the server.")

                        time = datetime.datetime.now()
                        now = round(time.timestamp())
                        embed = discord.Embed(title=f"{member} has been {punishment}", color=discord.Colour.blue())
                        embed.add_field(name="Reason",
                                        value=f"Server Security Join-Filter | This user has reached the minimum number of points and was kicked from the server.",
                                        inline=False)
                        embed.add_field(name="Maximal Points", value=f"{maxpoints}", inline=False)
                        embed.add_field(name="Points", value=f"{points}", inline=False)
                        embed.add_field(name="Date", value=f"<t:{now}:F>\n", inline=False)
                        embed.set_thumbnail(url=member.avatar_url)
                        await sendLogMessage(self, event=member, embed=embed, channel=logChannel)










def setup(client):
    client.add_cog(AntiRaid(client))