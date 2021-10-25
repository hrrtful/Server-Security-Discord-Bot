import json
from discord.ext import commands
import time
import asyncio


def getConfig(guildID):
    with open("config.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "owner": " ",
            "administrator": False,
            "prefix": "s!",
            "antinuke": False,
            "punishment": "kick",
            "whitelist": [],
            "captcha": False,
            "captchaChannel": False,
            "captchaLog": False,
            "temporaryRole": False,
            "roleGivenAfterCaptcha": False,
            "automoderation": False,
            "antiWord": False,
            "antiSpam": False,
            "antiLink": False,
            "antighost": False,
            "joinfilter": False,
            "botfilter": False,
            "avatarfilter": False,
            "captchapunishment": False,
            "logChannel": False,
            "panicmode": False,
            "panicpunishment": False,
            "autoban": False,
            "checknew": False,
            "points": 25
        }
        updateConfig(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]


def updateConfig(guildID, data):
    with open("config.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("config.json", "w") as config:
        config.write(newdata)


async def getGuildPrefix(client, message):
    if not message.guild:
        return "s!"
    else:
        config = getConfig(message.guild.id)
        return config["prefix"]


def guild_owner_only():
    async def predicate(ctx):
        return ctx.author == ctx.guild.owner
    return commands.check(predicate)


async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['warns'] = 0