#from moviepy.editor import *
from langchain_core.tools import tool
from moviepy import *
from moviepy.audio.AudioClip import CompositeAudioClip
import assemblyai as aai
import ffmpeg
import subprocess
aai.settings.api_key = "2895823538bb48229386bb84312dc133"

transcriber = aai.Transcriber()

import reddit, screenshot, time, subprocess, random, configparser, sys, math, youtube
from os import listdir

from os.path import isfile, join
from youtube import upload_video
from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip



audio = AudioFileClip("backgroundvid/summer-memories-270159.mp3")
my_clip = VideoFileClip("outputvid/2024-12-27-1hni0fa.mp4")

adjusted_audio = audio.volumex(0.2)
if adjusted_audio.duration > my_clip.duration:
    adjusted_audio = adjusted_audio.subclip(0, my_clip.duration)
#video1 = VideoFileClip("outputvid/2024-12-27-1hni0fa.mp4")
#final = video1.set_audio(adjusted_audio)

#final.write_videofile("outputvid/output.mp4")
audio_background = adjusted_audio
final_audio = CompositeAudioClip([my_clip.audio, audio_background])
final_clip = my_clip.set_audio(final_audio)
final_clip.write_videofile("outputvid/output1.mp4")
transcript = transcriber.transcribe("outputvid/output1.mp4")
srt = transcript.export_subtitles_srt()

with open("subtitles.srt", "w") as f:
    f.write(srt)
def add_subtitles(video_file, srt_file, output_file):
    # Command to burn subtitles into the video
    command = [
        "ffmpeg",
        "-i", video_file,
        "-vf", f"subtitles={srt_file}",
        output_file
    ]
    subprocess.run(command, check=True)
    print(f"Subtitles added and saved to {output_file}")
video_path = "outputvid/output1.mp4"
srt_path = "subtitles.srt"
output_path = "output/output_with_subtitles.mp4"

add_subtitles(video_path, srt_path, output_path)