from moviepy.editor import VideoFileClip
from io import BytesIO
from django.core.files.base import ContentFile



def generate_preview(video_instance):
    try:
        # Open the uploaded video file
        video_path = video_instance.video.path
        clip = VideoFileClip(video_path)

        # Trim the video to the first 5 seconds
        preview_clip = clip.subclip(0, 5)

        # Save the preview to a BytesIO object
        preview_io = BytesIO()
        preview_clip.write_videofile(preview_io, codec="libx264", audio_codec="aac", fps=24)

        # Save the preview to the VidStream model
        video_instance.preview.save('preview.mp4', ContentFile(preview_io.getvalue()), save=True)
    except Exception as e:
        print(f"Preview generation failed: {e}")