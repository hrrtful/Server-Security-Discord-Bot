import discord

from discord.ext import commands
from discord.utils import get
from Tools.utils import getConfig, getGuildPrefix, guild_owner_only, updateConfig


class Disable(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(usage="all")
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def disable(self, ctx, all):
        data = getConfig(ctx.guild.id)
        owner = data["owner"]
        if ctx.author.id == owner:
            loading = await ctx.channel.send("Disabling... (Sometimes it can take a while until everything got delete.)")
            data = getConfig(ctx.guild.id)
            data["captcha"] = False

            noDeleted = []

            try:
                temporaryRole = get(ctx.guild.roles, id=data["temporaryRole"])
                await temporaryRole.delete()
            except:
                noDeleted.append("temporaryRole")
            try:
                captchaChannel = self.client.get_channel(data["captchaChannel"])
                await captchaChannel.delete()
            except:
                noDeleted.append("captchaChannel")
            try:
                captchaLog = self.client.get_channel(data["captchaLog"])
                await captchaLog.delete()
            except:
                noDeleted.append("captchaLog")
            try:
                roleGivenAfterCaptcha = get(ctx.guild.roles, id=data["roleGivenAfterCaptcha"])
                await roleGivenAfterCaptcha.delete()
            except:
                noDeleted.append("roleGivenAfterCaptcha")
            try:
                logChannel = self.client.get_channel(data["logChannel"])
                await logChannel.delete()
            except:
                noDeleted.append("logChannel")

            # Add modifications
            data["captchaChannel"] = False
            data["captchaLog"] = False
            data["temporaryRole"] = False
            data["roleGivenAfterCaptcha"] = False
            data["antinuke"] = False
            data["logChannel"] = False
            data["automoderation"] = False
            data["panicmode"] = False
            data["antighost"] = False
            data["antiSpam"] = False
            data["antiWord"] = False
            data["antiLink"] = False
            data["botfilter"] = False
            data["avatarfilter"] = False
            data["joinfilter"] = False
            data["panicmode"] = False
            data["autoban"] = False
            data["checknew"] = False

            # Edit configuration.json
            updateConfig(ctx.guild.id, data)

            await loading.delete()
            await ctx.send("Server Security features successfully disabled!")

            if len(noDeleted) > 0:
                await ctx.send("Error(s) detected during the deletion of the `{0}`.".format(errors))

        if ctx.author.id != owner:
            await ctx.send("Only the server owner can use this command!")



def setup(client):
    client.add_cog(Disable(client))