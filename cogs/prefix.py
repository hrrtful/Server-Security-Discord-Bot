import discord
from discord.ext import commands
import json
from Tools.utils import getConfig, updateConfig, getGuildPrefix


class Prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(usage="<new prefix>")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.guild_only()
    async def prefix(self, ctx, newprefix):
        data = getConfig(ctx.guild.id)
        data["prefix"] = newprefix

        await ctx.send(f"Your server prefix has been changes, new prefix: {newprefix}")

        updateConfig(ctx.guild.id, data)
        data = getConfig(ctx.guild.id)
        if data["captcha"] is True:
            if newprefix == "s!":
                pass
            else:
                await ctx.send(f"You should disable and enable the captcha-verification, because the prefix has been changed and the embed in <#{data['captchaChannel']}> was not changed")



def setup(client):
    client.add_cog(Prefix(client))