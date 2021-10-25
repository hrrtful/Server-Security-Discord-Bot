import discord
from discord.ext import commands
from Tools.utils import getConfig, getGuildPrefix, updateConfig


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        prefix = await getGuildPrefix(self.client, ctx)
        help = discord.Embed(title="Overview", description="Server Security is an anti nuke bot with some other cool features.", colour=discord.Colour.blue())
        help.add_field(name="General Commands:", value="`about`, `invite`, `serverinfo`, `userinfo`, `prefix`, `inviteinfo`, `commands`, `bug`, `fetchuser`, `snipe`", inline=False)
        help.add_field(name="Moderation Commands:", value=f"`lock`, `unlock`, `kick`, `ban`, `unban`, `clear`, `mute`, `unmute`, `nuke`, `role`")
        help.add_field(name="Server Security", value=f"`features`, `settings`, `permissions`\n\nDo you want to setup Server Security? use `{prefix}setup`", inline=False)
        await ctx.send(embed=help)

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.mentions[0] == self.client.user:
                prefix = await getGuildPrefix(self.client, message)
                help = discord.Embed(title="Overview", description="Server Security is an anti nuke bot with some moderation features.", colour=discord.Colour.blue())
                help.add_field(name="General Commands:", value="`about`, `invite`, `serverinfo`, `userinfo`, `prefix`, `inviteinfo`, `commands`, `bug`, `fetchuser`, `snipe`", inline=False)
                help.add_field(name="Moderation Commands:", value=f"`lock`, `unlock`, `kick`, `ban`, `unban`, `clear`, `mute`, `unmute`, `nuke`, `role`")
                help.add_field(name="Server Security", value=f"`features`, `settings`, `permissions`\n\nDo you want to setup Server Security? use `{prefix}setup`", inline=False)
                await message.channel.send(embed=help)
                await self.client.process_commands(message)
        except IndexError:
            pass


def setup(client):
    client.add_cog(Help(client))