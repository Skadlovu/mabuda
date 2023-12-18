from tempfile import NamedTemporaryFile
from pathlib import Path
from io import BytesIO
from PIL import Image
from moviepy.editor import VideoFileClip
from django.core.files.base import ContentFile




def thumb_generator(video_content, model):
    temp_video_file = NamedTemporaryFile(delete=False)
    temp_thumbnail_file = NamedTemporaryFile(suffix='.jpg', delete=False)

    try:
        # Write video content to the temporary file
        temp_video_file.write(video_content.read())

        # Use moviepy to extract a thumbnail
        clip = VideoFileClip(temp_video_file.name)
        thumbnail = clip.get_frame(clip.duration / 2)

        # Convert the thumbnail to an Image object using Pillow
        thumbnail_image = Image.fromarray(thumbnail)

        # Save the thumbnail to the model
        thumbnail_io = BytesIO()
        thumbnail_image.save(thumbnail_io, format='JPEG')
        thumbnail_file = ContentFile(thumbnail_io.getvalue())
        model.thumb.save('thumbnail.jpg', thumbnail_file, save=True)

    except Exception as e:
        # Handle errors
        print(f"Thumbnail generation failed: {e}")

    finally:
        # Clean up temporary files
        temp_video_file.close()
        temp_thumbnail_file.close()
        Path(temp_video_file.name).unlink()
        Path(temp_thumbnail_file.name).unlink()

        # Add debug statements

   


