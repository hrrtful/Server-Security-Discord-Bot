import discord

from discord.ext import commands
from Tools.utils import getConfig, getGuildPrefix, guild_owner_only, updateConfig


class Developer(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def shutdown(self, ctx):
        if ctx.author.id == 644895688160837642:
            await ctx.send("Shuting down....")
            await self.client.logout()
        else:
            return

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def guildleave(self, ctx):
        if ctx.author.id == 644895688160837642:
            await ctx.guild.leave()
            print(f"{ctx.author.name} send a cmd in {ctx.guild.name}")
        else:
            return

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def guilds(self, ctx):
        try:
            if ctx.author.id == 644895688160837642:
                embed = discord.Embed(title="guilds:", color=discord.Colour.blue()
                                      )
                guilds = self.client.guilds
                for guild in guilds:
                    gm = guild.member_count
                    gn = guild.name
                    await ctx.send(f"{gn} | {gm}")
            else:
                return
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = guild.text_channels[0]
        joinchannel = self.client.get_channel(895186901022158868)
        invlink = await channel.create_invite(unique=True)
        await joinchannel.send(f"I have been added to: {invlink}")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        removechannel = self.client.get_channel(895186901022158868)
        await removechannel.send(f"I have been removed at {guild.name}")



def setup(client):
    client.add_cog(Developer(client))