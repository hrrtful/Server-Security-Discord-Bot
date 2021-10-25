import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions, CommandNotFound, BotMissingPermissions, MissingRequiredArgument
from Tools.utils import getGuildPrefix


class Errors(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        prefix = await getGuildPrefix(self.client, ctx)
        if isinstance(error, commands.CommandOnCooldown):
            minute = round(error.retry_after)
            if minute > 0:
                await ctx.send("Command Cooldown: {0} second(s)!".format(minute))

        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Wrong Usage",
                                  description=f"`{prefix}{ctx.command.name} {ctx.command.usage}`", colour=discord.Colour.blue())
            await ctx.send(embed=embed)

        if isinstance(error, commands.MissingPermissions):
            emote = ("<a:checkno:895020333986353172>")
            await ctx.send(f"You must have a higher role to use this command {emote}")

        if isinstance(error, commands.MemberNotFound):
            emote = ("<a:checkno:895020333986353172>")
            await ctx.send(f"Member not found {emote}")

        if isinstance(error, commands.RoleNotFound):
            emote = ("<a:checkno:895020333986353172>")
            await ctx.send(f"Role not found {emote}")

        if isinstance(error, commands.BotMissingPermissions):
            emote = ("<a:checkno:895020333986353172>")
            await ctx.send(f"Missing some important permissions, check if Server Security has the administrator permission {emote}")






def setup(client):
    client.add_cog(Errors(client))