import asyncio
import discord
import json
import aiohttp
from discord.ext import commands
from datetime import datetime
from io import BytesIO
from Tools.utils import getConfig
import pytz


class onMessage(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            try:
                data = getConfig(message.guild.id)
                if data["automoderation"] is True:
                    if message.content == "" and len(message.attachments) == 0:
                        return
                    try:
                        data = getConfig(message.guild.id)
                        antiSpam = data["antiSpam"]
                        antiLink = data["antiLink"]
                        antiWord = data["antiWord"]
                        punishment = data["punishment"]

                    except AttributeError:
                        pass
                    try:
                        if antiSpam is True:
                            def check(message):
                                return(message.author == message.author and (datetime.utcnow() - message.created_at).seconds < 15)

                            if message.author.guild_permissions.administrator:
                                return

                            if len(list(filter(lambda m: check(m), self.client.cached_messages))) >= 4 and len(list(filter(lambda m: check(m), self.client.cached_messages))) < 8:
                                pass
                            elif len(list(filter(lambda m: check(m), self.client.cached_messages))) >= 8:
                                if data["punishment"] == "kick":
                                    await message.author.ban(reason=f"Server Security Auto-Moderation | Spamming", delete_message_days=7)
                                    await message.author.unban()

                                if data["punishment"] == "ban":
                                    await message.author.ban(reason=f"Server Security Auto-Moderation | Spamming", delete_message_days=7)

                                if data["punishment"] == "none":
                                    return

                        if antiLink is True:
                            if message.author.guild_permissions.administrator:
                                return
                            if "https://" in message.content:
                                await message.delete()

                                if data["punishment"] == "kick":
                                    reason = "Send a link"
                                    await message.author.kick(reason=f"Server Security Auto-Moderation | {reason}")

                                if data["punishment"] == "ban":
                                    await message.author.ban(reason=f"Server Security Auto-Moderation | {reason}", delete_message_days=0)

                                else:
                                    await message.author.kick(reason=f"Server Security Auto-Moderation | {reason}")

                        if antiWord is True:
                            if message.author.guild_permissions.administrator:
                                return

                            msg = message.content
                            with open('badwords.txt') as BadWords:
                                if msg in BadWords.read():
                                    await message.delete()
                                    await message.channel.send("Don´t use this word here!")

                        if message.mention_everyone:
                            await ctx.send("You can't mention everyone")

                    except UnboundLocalError:
                        pass
            except AttributeError:
                pass

            try:
                data = getConfig(message.guild.id)
                captchaChannel = data["captchaChannel"]
                if message.channel.id == captchaChannel:
                    await message.delete()
            except AttributeError:
                pass

        except discord.errors.NotFound:
            pass


def setup(client):
    client.add_cog(onMessage(client))