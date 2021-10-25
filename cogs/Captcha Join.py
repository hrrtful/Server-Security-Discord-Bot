import discord
import numpy as np
import random
import string
import Augmentor
import os
import shutil
from shutil import rmtree
import asyncio
import time
import pytz
from discord.ext import commands
from discord.utils import get
from PIL import ImageFont, ImageDraw, Image
from Tools.utils import getConfig, getGuildPrefix, updateConfig
from datetime import datetime
from datetime import date
import json
import datetime
import discapty
import kwargs


class Join(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        data = getConfig(member.guild.id)
        getrole = get(member.guild.roles, id=data["temporaryRole"])
        if data["captcha"] is True:
            await member.add_roles(getrole)

    @commands.command()
    async def verify(self, ctx):
        data = getConfig(ctx.guild.id)
        checkrole = get(ctx.guild.roles, id=data["temporaryRole"])
        if checkrole not in ctx.author.roles:
            return await ctx.send("You are already verified!")
        else:
            member = ctx.author
            data = getConfig(member.guild.id)
            captchaChannel = self.client.get_channel(data["captchaChannel"])
            captchaLog = self.client.get_channel(data["captchaLog"])
            await ctx.message.delete()


            # Create captcha
            image = np.zeros(shape=(100, 350, 3), dtype=np.uint8)

            # Create image
            image = Image.fromarray(image + 255)  # +255 : black to white

            # Add text
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype(font="Tools/arial.ttf", size=60)

            text = ' '.join(
                random.choice(string.ascii_uppercase) for _ in range(6))  # + string.ascii_lowercase + string.digits

            # Center the text
            W, H = (350, 100)
            w, h = draw.textsize(text, font=font)
            draw.text(((W - w) / 2, (H - h) / 2), text, font=font, fill=(90, 90, 90))

            # Save
            ID = member.id
            folderPath = f"captchaFolder/{member.guild.id}/captcha_{ID}"
            try:
                os.mkdir(folderPath)
            except:
                if os.path.isdir(f"captchaFolder/{member.guild.id}") is False:
                    os.mkdir(f"captchaFolder/{member.guild.id}")
                if os.path.isdir(folderPath) is True:
                    shutil.rmtree(folderPath)
                os.mkdir(folderPath)
            image.save(f"{folderPath}/captcha{ID}.png")

            # Deform
            p = Augmentor.Pipeline(folderPath)
            p.random_distortion(probability=1, grid_width=4, grid_height=4, magnitude=14)
            p.process()

            # Search file in folder
            path = f"{folderPath}/output"
            files = os.listdir(path)
            captchaName = [i for i in files if i.endswith('.png')]
            captchaName = captchaName[0]

            image = Image.open(f"{folderPath}/output/{captchaName}")

            # Add line
            width = random.randrange(6, 8)
            co1 = random.randrange(0, 75)
            co3 = random.randrange(275, 350)
            co2 = random.randrange(40, 65)
            co4 = random.randrange(40, 65)
            draw = ImageDraw.Draw(image)
            draw.line([(co1, co2), (co3, co4)], width=width, fill=(90, 90, 90))

            # Add noise
            noisePercentage = 0.25  # 25%

            pixels = image.load()  # create the pixel map
            for i in range(image.size[0]):  # for every pixel:
                for j in range(image.size[1]):
                    rdn = random.random()  # Give a random %
                    if rdn < noisePercentage:
                        pixels[i, j] = (90, 90, 90)

            # Save
            image.save(f"{folderPath}/output/{captchaName}_2.png")
            data = getConfig(member.guild.id)
            captchaChannel = self.client.get_channel(data["captchaChannel"])
            captchaLog = self.client.get_channel(data["captchaLog"])
            gettemprole = get(member.guild.roles, id=data["temporaryRole"])
            channel = await member.guild.create_text_channel('captcha-verify-here')
            perms = channel.overwrites_for(gettemprole)
            perms.read_messages = True
            perms.send_messages = True
            await channel.set_permissions(gettemprole, overwrite=perms)

            perms = channel.overwrites_for(member.guild.default_role)
            perms.read_messages = False
            await channel.set_permissions(member.guild.default_role, overwrite=perms)
            try:
                captchaFile = discord.File(f"{folderPath}/output/{captchaName}_2.png", filename="captcha.png")
                captcha_embed = discord.Embed(title=f"{member.guild.name} Captcha Verification",
                                              description=f"{member.mention} Please return me the code written on the Captcha.",
                                              colour=discord.Colour.blue())
                captcha_embed.set_image(url="attachment://captcha.png")
                captcha_embed.set_footer(text=f"Want this bot in your server? → s!invite")
                captchaEmbed = await channel.send(file=captchaFile, embed=captcha_embed)
            except:
                pass

                # Remove captcha folder
            try:
                shutil.rmtree(folderPath)
            except Exception as error:
                print(f"Delete captcha file failed {error}")

                # Check if it is the right user

            def check(message):
                if message.author == member and message.content != "":
                    return message.content

            try:
                msg = await self.client.wait_for('message', timeout=120.0, check=check)
                # Check the captcha
                password = text.split(" ")
                password = "".join(password)
                if msg.content == password:
                    prefix = await getGuildPrefix(self.client, member)
                    try:
                        embed = discord.Embed(
                            title="Thank you!",
                            description="You have been verified in guild **{0}**".format(
                                member.guild),
                            color=discord.Colour.blue())
                        embed.set_footer(
                            text="Want this bot in your server? → {0}invite".format(prefix))
                        await channel.send(embed=embed)
                    except:
                        pass

                    try:
                        getrole = get(member.guild.roles, id=data["roleGivenAfterCaptcha"])
                        if getrole is not False:
                            await member.add_roles(getrole)
                    except Exception as error:
                        print(f"Give and remove roles failed : {error}")
                    try:
                        temp = get(member.guild.roles, id=data["temporaryRole"])
                        await member.remove_roles(temp)
                    except Exception as error:
                        print(f"No temp role found (onJoin) : {error}")
                    time.sleep(3)
                    try:
                        await captchaEmbed.delete()
                    except discord.errors.NotFound:
                        pass

                    try:
                        await channel.delete()
                    except UnboundLocalError:
                        pass

                    # Logs
                    timenow = datetime.datetime.now()
                    now = round(timenow.timestamp())
                    embed = discord.Embed(
                        title="Captcha Logging - Passed",
                        description="User {0} has successfully passed the captcha.".format(member.mention), color=discord.Colour.blue())
                    embed.add_field(
                        name="User ID",
                        value=f'{member.id}', inline=False)
                    embed.add_field(name="Date", value=f"<t:{now}:F>\n", inline=False)
                    embed.set_thumbnail(url=member.avatar_url)
                    await captchaLog.send(embed=embed)

                else:
                    try:
                        data = getConfig(ctx.guild.id)
                        punishment = data["punishment"]
                        await channel.send("You have failed the captcha please use the verify command again!")
                    except discord.errors.Forbidden:
                        # can't send dm to user
                        await channel.send("You have failed the captcha please use the verify command again!")

                    data = getConfig(ctx.guild.id)
                    captchapunishment = data["captchapunishment"]

                    if captchapunishment == "kick":
                        try:
                            await member.kick(reason="Server Security Captcha Protection | User failed the captcha")
                        except:
                            pass

                    if captchapunishment == "ban":
                        try:
                            await member.ban(reason="Server Security Captcha Protection | User failed the captcha")
                        except:
                            pass

                    if captchapunishment == "none":
                        pass

                    time.sleep(3)
                    try:
                        await captchaEmbed.delete()
                    except discord.errors.NotFound:
                        pass
                    try:
                        await msg.delete()
                    except discord.errors.Forbidden:
                        pass
                    try:
                        await channel.delete()
                    except UnboundLocalError:
                        pass

                    timenow = datetime.datetime.now()
                    now = round(timenow.timestamp())
                    embed = discord.Embed(
                        title="Captcha Logging - Failed",
                        description="User {0} has failed the captcha.".format(member.mention),
                        color=discord.Colour.blue())
                    embed.add_field(
                        name="User ID",
                        value=f'{member.id}')
                    embed.add_field(name="Date", value=f"<t:{now}:F>\n", inline=False)
                    embed.set_thumbnail(url=member.avatar_url)
                    await captchaLog.send(embed=embed)

            except(asyncio.TimeoutError):
                try:
                    try:
                        await member.send("You have exceeded the response time (120s), please use the verify command again!")
                    except discord.errors.Forbidden:
                        await channel.send("You have exceeded the response time (120s), please use the verify command again!")
                except Exception as error:
                    print(f"Log failed (onJoin) : {error}")
                time.sleep(3)
                try:
                    await captchaEmbed.delete()
                except discord.errors.Forbidden:
                    pass
                try:
                    await channel.delete()
                except UnboundLocalError:
                    pass

                timenow = datetime.datetime.now()
                now = round(timenow.timestamp())
                embed = discord.Embed(
                    title="Captcha Logging - Exceeded",
                    description="User {0} has exceeded the captcha response time (120s)".format(member.mention),
                    timestamp=datetime.now().astimezone(tz=de), color=discord.Colour.blue())
                embed.add_field(
                    name="User ID",
                    value=f'{member.id}', inline=False)
                embed.add_field(name="Date", value=f"<t:{now}:F>\n", inline=False)
                embed.set_thumbnail(url=member.avatar_url)
                await captchaLog.send(embed=embed)


def setup(client):
    client.add_cog(Join(client))