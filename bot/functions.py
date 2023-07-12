from pytube import YouTube
import discord

def get_video_icon(url):
    try:
        video = YouTube(url)
        return video.thumbnail_url
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def seconds_to_time(seconds):
    """Converts seconds to a string of the format HH:MM:SS."""
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = int(seconds % 60)

    return f"{hours:02}:{minutes:02}:{seconds:02}"


def createEmbed(info):
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
    embed.set_thumbnail(url= get_video_icon(f'https://youtu.be/{info["id"]}'))
    embed.add_field(name="Duration", value=seconds_to_time(info['duration']), inline=True)
    embed.add_field(name="Requested by", value=info['requester'], inline=True)
    embed.set_footer(text="© 2023 XYECoC inc.")
    
    return embed