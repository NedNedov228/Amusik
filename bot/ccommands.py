from discord.ext import commands



@commands.command()
async def hello(ctx):
    await ctx.send("Hello!")


def setup(bot):
    bot.add_command(hello)