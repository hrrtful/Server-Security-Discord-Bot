import discord
import json
from Tools.utils import getConfig
from discord.ext import commands
from discord.utils import get


class OnChannelCreate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        data = getConfig(channel.guild.id)
        temporaryRole = get(channel.guild.roles, id=data["temporaryRole"])

        if temporaryRole is not None:

            if channel.name == "captcha-verify-here":
                return

            if isinstance(channel, discord.TextChannel):

                perms = channel.overwrites_for(temporaryRole)
                perms.read_messages = False
                await channel.set_permissions(temporaryRole, overwrite=perms)

            elif isinstance(channel, discord.VoiceChannel):

                perms = channel.overwrites_for(temporaryRole)
                perms.read_messages = False
                perms.connect = False
                await channel.set_permissions(temporaryRole, overwrite=perms)



def setup(client):
    client.add_cog(OnChannelCreate(client))