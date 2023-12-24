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
#by b1tz0 und FontomO4ka
# Special thanks to Dzinski!
queues = {} # {server_id: [(vid_file, info), ...]}ч

queue  = [] # [(vid_file, info), ...]

connection = None

currently_playing = None
currently_active_message = None

config = {
    'token': 'MTEyNjk4NDAzNzI5NTIxNDYzMg.Gpszs1.kqN_MbNWnof5L1m-qTWYYmi0-HLXJEqxR43fEw',
    'prefix': '.',
}

loopedCurr = False
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


# @bot.command(help = "Показывает пинг бота")
# async def hello(ctx):
#     await ctx.send("Hello")

@bot.command(name="queue", help = "Показывает пинг бота")
async def queue_command(ctx, *args):
    global queue
    global currently_playing
    if len(args) != 1:
        await ctx.send("Invalid arguments")
        return
    if args[0] == "clear":
        queue.clear()
        await ctx.message.add_reaction("\u2705")
        for f in os.listdir(f'./dl/{ctx.guild.id}'):
            if(f'./dl/{ctx.guild.id}/{f}' != currently_playing[0]):
                os.remove(f'./dl/{ctx.guild.id}/{f}')
        return
    
@bot.command(help = "Показывает пинг бота")
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


async def is_link(str):
    return re.match(r'^https?:\/\/(www\.)?youtube\.com\/watch\?v=[\w-]+$', str) is not None

@bot.command(name = 'skip')
async def skip(ctx: commands.Context):
    global currently_active_message
    if ctx.voice_client is None:
        await ctx.send('Not connected')
        return
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
    # if currently_active_message is not None:
    #     currently_active_message.delete()

async def run_queue(ctx: commands.Context):
    global connection
    global loopedCurr
    global queue
    global currently_playing
    global currently_active_message
    while 1:
        if len(queue) > 0 or loopedCurr:
            if connection is None or not connection.is_playing():
                print('playing queue')
                if loopedCurr: 
                    path , info = currently_playing
                else:
                    path, info = queue.pop(0)
                    currently_playing = (path, info)
                if currently_active_message is not None:
                    await currently_active_message.delete()
                print(f'playing {info["title"]}')
                connection.play(discord.FFmpegOpusAudio(path))
                embed = f.createEmbed(info)
                currently_active_message = await ctx.send(embed=embed)
        await asyncio.sleep(1)

@bot.command(name='play', aliases=['p'])
async def play(ctx: commands.Context, *args):
    global connection
    global queue
    # check if no arguments
    if len(args) == 0:
        await ctx.send('No arguments')
        return
    
    # check if in voice channel
    if ctx.author.voice is None:
        await ctx.send('You are not in a voice channel')
        return

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
       
        info['requester'] = ctx.author

        path = f'./dl/{server_id}/{info["id"]}.{info["ext"]}'
       
        await ctx.send(f'Enqueued `{info["title"]}` in position `{len(queue)+1}`.')
        message = await ctx.send('downloading ' + (f'https://youtu.be/{info["id"]}' if will_need_search else f'`{info["title"]}`'))
         
        ydl.download([query])
        print(f'finished downloading {info["title"]}')
        await message.delete()

        queue.append((path, info))
        
        try: queues[server_id].append((path, info))
        except KeyError: 
            queues[server_id] = [(path, info)]
            try: 
                connection = await voice_state.channel.connect()
                await run_queue(ctx)
            except discord.ClientException: 
                connection = get_voice_client_from_channel_id(voice_state.channel.id)
          
            # await message.delete()
            
            
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

@bot.command(name='loop', aliases=['repeat,rep,lp,rp'])
async def loop(ctx: commands.Context, *args):
    global loopedCurr
    if len(args) != 1:
        await ctx.send('Invalid arguments')
        return
    arg = args[0]
    loop_words = ['on', 'true', '1', 'one', 'all']
    unloop_words = ['off', 'false', '0', 'zero', 'none']
    if arg in loop_words:
        loopedCurr = True
    elif arg in unloop_words:
        loopedCurr = False
    await ctx.message.add_reaction("\u2705")
    await ctx.send(f"Looping is {'enabled' if loopedCurr else 'disabled'}")
    
bot.load_extension("ccommands")
bot.run(config['token'])
# talibans mom
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

