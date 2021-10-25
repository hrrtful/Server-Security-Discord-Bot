import discord
from discord.ext import commands
import platform
from Tools.utils import getGuildPrefix, getConfig
from dislash import InteractionClient, ActionRow, Button, ButtonStyle
from reactionmenu import ReactionMenu, Button, ButtonType
from discord import *
import datetime
from datetime import datetime
import os


class General(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.counter = 0

    @commands.command()
    async def about(self, ctx):
        dpyVersion = discord.__version__
        serverCount = len(self.client.guilds)
        about = discord.Embed(colour=discord.Colour.blue())
        about.add_field(name="Name", value=f"{self.client.user.name}")
        about.add_field(name="ID", value=f"{self.client.user.id}")
        about.add_field(name="Dpy-Version", value=f"{dpyVersion}")
        about.add_field(name="Guilds", value=f"{serverCount}")
        about.add_field(name="Ping", value=f"{round(self.client.latency * 1000)}ms")
        about.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=about)

    @commands.command()
    async def invite(self, ctx):
        invitelink = ("https://discord.com/api/oauth2/authorize?client_id=882901345466724373&permissions=8&scope=bot")
        msg = await ctx.send("Check your DMs")
        try:
            await ctx.author.send(f"`Invite Link`: {invitelink}")
        except discord.errors.Forbidden:
            await msg.edit(content="I am not allowed to send you a DM, look at my User profile there is also a invite link!")

    @commands.command()
    async def serverinfo(self, ctx):
        guild_roles = len(ctx.guild.roles)
        guild_categories = len(ctx.guild.categories)
        guild_members = len(ctx.guild.members)
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        channels = text_channels + voice_channels
        serverinfo = discord.Embed(colour=discord.Colour.blue())
        serverinfo.add_field(name="Server Name", value=f"{ctx.guild.name}")
        serverinfo.add_field(name="Server ID", value=f"{ctx.guild.id}")
        serverinfo.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
        serverinfo.add_field(name="Boosts", value=f"{ctx.guild.premium_subscription_count}")
        serverinfo.add_field(name="Channels", value=f"{channels}")
        serverinfo.add_field(name="Roles", value=f"{guild_roles}")
        serverinfo.add_field(name="Categories", value=f"{guild_categories} Categories")
        serverinfo.add_field(name="Members", value=f"{guild_members}")
        serverinfo.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=serverinfo)

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        format = "%d-%m-%Y"
        member = ctx.author if not member else member
        member_roles = len(member.roles)
        serverinfo = discord.Embed(colour=discord.Colour.blue())
        serverinfo.add_field(name="Username", value=f"{member}")
        serverinfo.add_field(name="User ID", value=f"{member.id}")
        serverinfo.add_field(name="Created At", value=f"{member.created_at.strftime(format)}")
        serverinfo.add_field(name="Joined At", value=f"{member.joined_at.strftime(format)}")
        serverinfo.add_field(name="Roles", value=f"{member_roles}")
        serverinfo.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=serverinfo)

    @commands.command(usage="<invitelink/code>")
    async def inviteinfo(self, ctx, invite):
        invite = await self.client.fetch_invite(invite)
        inviteinfo = discord.Embed(colour=discord.Colour.blue())
        inviteinfo.add_field(name="Server Name", value=f"{invite.guild.name}")
        inviteinfo.add_field(name="Server ID", value=f"{invite.guild.id}")
        inviteinfo.add_field(name="Inviter", value=f"{invite.inviter}")
        inviteinfo.add_field(name="Member", value=f"{invite.approximate_member_count}")
        inviteinfo.add_field(name="Link", value=f"{invite}")
        inviteinfo.set_thumbnail(url=invite.guild.icon_url)
        await ctx.send(embed=inviteinfo)

    @commands.command(name="commands")
    async def _commands(self, ctx):
        prefix = await getGuildPrefix(self.client, ctx)
        nextemote = "▶"
        backemote = "◀"
        menu = ReactionMenu(ctx, back_button=backemote, next_button=nextemote, config=ReactionMenu.STATIC)
        page1 = discord.Embed(title="Available commands", colour=discord.Colour.blue(),
                              description=f"`{prefix}about`\n"
                                          f"`{prefix}invite`\n"
                                          f"`{prefix}serverinfo`\n"
                                          f"`{prefix}userinfo`\n"
                                          f"`{prefix}prefix`\n"
                                          f"`{prefix}inviteinfo`\n"
                                          f"`{prefix}lockall`\n"
                                          f"`{prefix}unlockall`\n"
                                          f"`{prefix}lock`\n"
                                          f"`{prefix}unlock`")
        page2 = discord.Embed(title="Available commands", colour=discord.Colour.blue(),
                              description=f"`{prefix}kick`\n"
                                          f"`{prefix}ban`\n"
                                          f"`{prefix}unban`\n"
                                          f"`{prefix}clear`\n"
                                          f"`{prefix}mute`\n"
                                          f"`{prefix}unmute`\n"
                                          f"`{prefix}nuke`\n"
                                          f"`{prefix}whitelist`\n"
                                          f"`{prefix}unwhitelist`\n"
                                          f"`{prefix}whitelisted`\n")
        page3 = discord.Embed(title="Available commands", colour=discord.Colour.blue(),
                              description=
                                          f"`{prefix}punishment`\n"
                                          f"`{prefix}help`\n"
                                          f"`{prefix}setup`\n"
                                          f"`{prefix}commands`\n"
                                          f"`{prefix}bug`\n"
                                          f"`{prefix}verifiedrole`\n"
                                          f"`{prefix}captchapunishment`\n"
                                          f"`{prefix}panicmode`\n")
        menu.add_page(page1)
        menu.add_page(page2)
        menu.add_page(page3)
        member_details = []
        for member_embed in member_details:
            menu.add_page(member_embed)
        await menu.start()

    @commands.command(usage="<message>")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def bug(self, ctx, *, message=None):
        prefix = await getGuildPrefix(self.client, ctx)
        if message == None:
            await ctx.send(f"Please do `{prefix}bug` for this command to work!")
        else:
            await ctx.send("Thank you for reporting this bug my developer will try to fix it!")

            channel = self.client.get_channel(894943888832360539)
            embed2 = discord.Embed(title=f"Bug reported by {ctx.author}", colour=discord.Colour.blue())
            embed2.add_field(name="Server", value=f"{ctx.guild.name}")
            embed2.add_field(name="Bug", value=f"{message}")
            embed2.set_thumbnail(url=ctx.guild.icon_url)
            await channel.send(embed=embed2)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):
        data = getConfig(ctx.guild.id)
        captcha = data["captcha"]
        captchaChannel = data["captchaChannel"]
        temporaryRole = data["temporaryRole"]
        roleGivenAfterCaptcha = data["roleGivenAfterCaptcha"]
        antinuke = data["antinuke"]
        punishment = data["punishment"]
        prefix = data["prefix"]
        owner = data["owner"]
        captchaLog = data["captchaLog"]
        captchapunishment = data["captchapunishment"]
        joinfilter = data["joinfilter"]
        botfilter = data["botfilter"]
        avatarfilter = data["avatarfilter"]
        logChannel = data["logChannel"]
        automoderation = data["automoderation"]
        antiSpam = data["antiSpam"]
        antiWord = data["antiWord"]
        antiLink = data["antiLink"]
        antighost = data["antighost"]
        panicmode = data["panicmode"]
        panicpunishment = data["panicpunishment"]
        administrator = data["administrator"]
        autoban = data["autoban"]
        checknew = data["checknew"]
        points = data["points"]

        if roleGivenAfterCaptcha is not False:
            roleGivenAfterCaptcha = f"<@&{roleGivenAfterCaptcha}>"
        else:
            roleGivenAfterCaptcha = f"Not Found"
        if temporaryRole is not False:
            temporaryRole = f"<@&{temporaryRole}>"
        else:
            temporaryRole = f"Not Found"
        if captchaChannel is not False:
            captchaChannel = f"<#{captchaChannel}>"
        else:
            captchaChannel = f"Not Found"

        if captcha is True:
            captchaonoff = f"**enabled**"
        else:
            captchaonoff = f"disabled"

        if antinuke is True:
            antinuke = f"**enabled**"
        else:
            antinuke = f"disabled"
        if captchaLog is not False:
            captchaLog = f"<#{captchaLog}>"
        else:
            captchaLog = f"Not Found"
        if captchapunishment is False:
            captchapunishment = f"None"

        if joinfilter is True:
            joinfilter = f"**enabled**"
        else:
            joinfilter = f"disabled"

        if botfilter is True:
            botfilter = f"**enabled**"
        else:
            botfilter = f"disabled"

        if avatarfilter is True:
            avatarfilter = f"**enabled**"
        else:
            avatarfilter = f"disabled"

        if punishment is False:
            punishment = f"None"

        if logChannel is False:
            logChannel = f"Not Found"
        else:
            logChannel = f"<#{logChannel}>"

        if automoderation is not False:
            automoderation = f"**enabled**"
        else:
            automoderation = f"disabled"

        if antiSpam is not False:
            antiSpam = f"**enabled**"
        else:
            antiSpam = f"disabled"

        if antiLink is not False:
            antiLink = f"**enabled**"
        else:
            antiLink = f"disabled"

        if antiWord is not False:
            antiWord = f"**enabled**"
        else:
            antiWord = f"disabled"
        if antighost is not False:
            antighost = f"**enabled**"
        else:
            antighost = f"disabled"
        if panicmode is not False:
            panicmode = f"**enabled**"
        else:
            panicmode = f"disabled"

        if administrator is not False:
            administrator = f"<@{administrator}>"
        else:
            administrator = f"None"

        owner = f"<@{owner}>"

        if autoban is not False:
            autoban = f"**enabled**"
        else:
            autoban = f"disabled"

        if checknew is not False:
            checknew = f"**enabled**"
        else:
            checknew = f"disabled"

        embed = discord.Embed(title=f"Settings for {ctx.guild.name}", colour=discord.Colour.blue())
        embed.add_field(name="General Settings", value=f"Owner: {owner}\nAdministrator: {administrator}\nPrefix: {prefix}\nLog-Channel: {logChannel}", inline=False)
        embed.add_field(name="Anti-Nuke", value=f"Anti-Nuke: {antinuke}\nPunishment: {punishment}", inline=False)
        embed.add_field(name="Join-Filter", value=f"Join-Filter: {joinfilter}\nBot-Filter: {botfilter}\nAvatar-Filter: {avatarfilter}\nAuto-Ban: {autoban}\nCheck new member: {checknew}\nPoints: {points}", inline=False)
        embed.add_field(name="Captcha-Verification", value=f"Captcha-Verification: {captchaonoff}\nVerification-Channel: {captchaChannel}\nCaptcha-Log: {captchaLog}\nCaptcha-Punishment: {captchapunishment}\nUnverified-Role: {temporaryRole}\nVerified-Role: {roleGivenAfterCaptcha}", inline=False)
        embed.add_field(name="Auto-Moderation", value=f"Auto-Moderation: {automoderation}\nAnti-Spam: {antiSpam}\nAnti-Link: {antiLink}\n Anti-Word: {antiWord}\nAnti-Ghostping: {antighost}", inline=False)
        embed.add_field(name="Panic-Mode", value=f"Panic-Mode: {panicmode}\nPanic-Mode punishment: {panicpunishment}\n", inline=False)
        await ctx.send(embed=embed)



    @commands.group(invoke_without_command=True)
    async def features(self, ctx):
        prefix = await getGuildPrefix(self.client, ctx)
        features = discord.Embed(title=f"{self.client.user.name} features", colour=discord.Colour.blue(),
                                 description=f"With some powerful features, Server Security will be able to protect your server from being nuked, raiders, malicous users, spammer etc. Make sure the bot has the highest possible role on your server. Don't give it a higher role! Move the role it created higher! **Also the bot won't function without having the Administrator permission.**")
        features.add_field(name=f"Information", value=f"`{prefix}features captcha`\n"
                                                      f"`{prefix}features antinuke`\n"
                                                      f"`{prefix}features joinfilter`\n"
                                                      f"`{prefix}features automoderation`\n"
                                                      f"`{prefix}features panicmode`\n", inline=False)
        features.add_field(name="Captcha-Verification", value=f"`{prefix}setup captcha`\n"
                                                              f"`{prefix}verifiedrole <role id>`\n"
                                                              f"`{prefix}captchapunishment <kick/ban/none>`\n", inline=False)
        features.add_field(name="Anti-Nuke", value=f"`{prefix}setup antinuke`\n"
                                                   f"`{prefix}punishment <kick/ban/none>`\n"
                                                   f"`{prefix}whitelist <user>`\n"
                                                   f"`{prefix}unwhitelist <user>`\n"
                                                   f"`{prefix}whitelisted`", inline=False)
        features.add_field(name="Join-Filter", value=f"`{prefix}setup joinfilter`\n"
                                                     f"`{prefix}botfilter <on/off>`\n"
                                                     f"`{prefix}avatarfilter <on/off>`\n"
                                                     f"`{prefix}checknew <on/off>`\n"
                                                     f"`{prefix}autoban <on/off>`\n"
                                                     f"`{prefix}maxpoints <points>`\n")
        features.add_field(name="Auto-Moderation", value=f"`{prefix}setup automoderation`\n"
                                                         f"`{prefix}antispam <on/off>`\n"
                                                         f"`{prefix}antiword <on/off>`\n"
                                                         f"`{prefix}antilink <on/off>`\n"
                                                         f"`{prefix}antighost <on/off>`", inline=False)
        features.add_field(name="Panic-Mode", value=f"`{prefix}panicmode <on/off>`\n"
                                                    f"`{prefix}panicpunishment <kick/ban/mute>`")
        await ctx.send(embed=features)

    @commands.command()
    async def permissions(self, ctx):
        embed = discord.Embed(title=f"Important Permissions", description=f'1. **Administrator Permission**\n'
                                                                          f'2. **The created Role must be at the Top**\n', colour=discord.Colour.blue())
        await ctx.send(embed=embed)

    @features.command()
    async def captcha(self, ctx):
        prefix = await getGuildPrefix(self.client, ctx)
        embed = discord.Embed(title=f"Captcha-Verification", description=f"The Captcha-Verification will protect your server from malicious raids using automoated bots and malicious users/discord scammer! I will create a Verification-Channel, Captcha-Logs, Unverified-Role and a Verified-Role. You can also change the punishment!", colour=discord.Colour.blue())
        embed.add_field(name=f"Setup", value=f"`{prefix}setup captcha`", inline=False)
        embed.add_field(name="Disable", value=f"`{prefix}captcha <off>`", inline=False)
        embed.add_field(name=f"Verified Role", value=f"`{prefix}verifiedrole <role id>`", inline=False)
        embed.add_field(name=f"Punishment", value=f"`{prefix}captchapunishment <kick/ban/none>`", inline=False)
        await ctx.send(embed=embed)

    @features.command()
    async def antinuke(self, ctx):
        prefix = await getGuildPrefix(self.client, ctx)
        embed = discord.Embed(title=f"Anti-Nuke System", description=f"If the Anti-Nuke system is enabled, Server Security will constantly monitor the audit log. This means that malicous bots can no longer destroy your server! **You should whitelist some users!**", colour=discord.Colour.blue())
        embed.add_field(name="Setup", value=f"`{prefix}setup antinuke`", inline=False)
        embed.add_field(name="Disable", value=f"`{prefix}antinuke <off>`", inline=False)
        embed.add_field(name=f"Punishment", value=f"`{prefix}punishment <kick/ban/none>`", inline=False)
        embed.add_field(name=f"Whitelist", value=f"`{prefix}whitelist <user>`\n"
                                                 f"`{prefix}unwhitelist <user>`\n"
                                                 f"`{prefix}whitelisted`", inline=False)
        await ctx.send(embed=embed)

    @features.command()
    async def joinfilter(self, ctx):
        prefix = await getGuildPrefix(self.client, ctx)
        embed = discord.Embed(title=f"Join-Filter", description=f"The Join-Filter filters out bots, users who don't have a custom avatar, or it checks the users with a points system. The maximum default number of points is 25, but you can change it at any time. Tip I would be careful with the Auto-Ban module and enable it only in emergency situations!", colour=discord.Colour.blue())
        embed.add_field(name=f"Setup", value=f"`{prefix}setup joinfilter`", inline=False)
        embed.add_field(name=f"Disable", value=f"`{prefix}joinfilter <off>`", inline=False)
        embed.add_field(name="Module", value=f"`{prefix}botfilter <on/off>`\n`{prefix}avatarfilter <on/off>`\n`{prefix}autoban <on/off>`\n`{prefix}checknew <on/off>`\n`{prefix}maxpoints <points>`\n", inline=False)
        await ctx.send(embed=embed)

    @features.command()
    async def automoderation(self, ctx):
        prefix = await getGuildPrefix(self.client, ctx)
        embed = discord.Embed(title=f"Auto-Moderation", description=f"The Auto-Moderation System is enabled it will monitor every message!", colour=discord.Colour.blue())
        embed.add_field(name=f"Setup", value=f"`{prefix}setup automoderation`", inline=False)
        embed.add_field(name=f"Disable", value=f"`{prefix}automoderation <off>`", inline=False)
        embed.add_field(name="Module", value=f"`{prefix}antispam <on/off>`\n"
                                             f"`{prefix}antiword <on/off>`\n"
                                             f"`{prefix}antilink <on/off>`\n"
                                             f"`{prefix}antighost <on/off>`\n", inline=False)
        await ctx.send(embed=embed)

    @features.command()
    async def panicmode(self, ctx):
        prefix = await getGuildPrefix(self.client, ctx)
        embed = discord.Embed(title=f"Panic-Mode", description=f"If the Panic-Mode is enabled, every user who writes a message will be kicked/banned/muted", colour=discord.Colour.blue())
        embed.add_field(name=f"Enable", value=f"`{prefix}panicmode <on>`", inline=False)
        embed.add_field(name=f"Disable", value=f"`{prefix}panicmode <off>`", inline=False)
        embed.add_field(name=f"Punishment", value=f"`{prefix}panicpunishment <kick/ban/mute>`", inline=False)
        await ctx.send(embed=embed)

    @commands.command(usage="user id")
    async def fetchuser(self, ctx, user: discord.User = id):
        format = "%d-%m-%Y"
        user = await self.client.fetch_user(int(user.id))
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.add_field(name="Username", value=f"{user}")
        embed.add_field(name="User ID", value=f"{user.id}")
        embed.add_field(name="Created At", value=f"{user.created_at.strftime(format)}")
        embed.add_field(name="Bot", value=f"{('Yes' if user.bot else 'No')}")
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(General(client))