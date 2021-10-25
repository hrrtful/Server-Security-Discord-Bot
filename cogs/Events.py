import discord
from discord.ext import commands
from Tools.utils import getConfig, getGuildPrefix, guild_owner_only, updateConfig
import datetime


class Event(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        data = getConfig(message.guild.id)
        ghostping = data["antighost"]
        if data["automoderation"] is True:
            if ghostping is True:
                if len(message.mentions) == 0:
                    return
                else:
                    ghostping = discord.Embed(title=f'Ghost Pinged!', color=discord.Colour.blue())
                    ghostping.add_field(name='Name', value=f"{message.author.mention}")
                    ghostping.add_field(name='Message', value=f'{message.content}', inline=False)
                    try:
                        await message.channel.send(embed=ghostping)
                    except:
                        pass


def setup(client):
    client.add_cog(Event(client))