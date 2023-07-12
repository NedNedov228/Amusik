

import functions as f

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


config = {
    'token': 'MTEyNjk4NDAzNzI5NTIxNDYzMg.GcFqYs.xt0HgoEw07-gSROK7tvoUokpCpMqAaCB-c_4oo',
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
    channel = ctx.author.voice.channel
    await channel.connect()



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

                now playing


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
@bot.command(name='disconnect', aliases=['dc'])
async def leave(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    await ctx.message.add_reaction("\u2705")



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

