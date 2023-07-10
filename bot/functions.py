from pytube import YouTube

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