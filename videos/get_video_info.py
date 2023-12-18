# get_video_info.py

from moviepy.editor import VideoFileClip
from io import BytesIO
import tempfile
import math

def format_duration(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes)}:{int(seconds):02d}"

def format_size(bytes_size):
    mb_size = bytes_size / (1024 ** 2)
    return f"{mb_size:.2f} MB"

def get_video_info(file_content):
    try:
        # Create a BytesIO object to read the file content
        video_file = BytesIO(file_content)

        # Save the BytesIO content to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(video_file.read())

        # Use moviepy to get video information from the temporary file
        clip = VideoFileClip(temp_file.name)
        duration = clip.duration
        size = len(file_content)

        formatted_duration = format_duration(duration)
        formatted_size = format_size(size)

        return formatted_duration, formatted_size
    except Exception as e:
        # Print or log the exception details
        print(f"Error getting video information: {e}")
        return None, None
    finally:
        # Clean up: delete the temporary file
        try:
            temp_file.close()
        except Exception:
            pass
