#from moviepy.editor import *
from langchain_core.tools import tool
from moviepy.editor import *
import os
import random
import configparser
import sys
import subprocess
import assemblyai as aai
import moviepy
import ffmpeg
import reddit, screenshot, youtube
import time, subprocess, random, configparser, sys, math
from os import listdir
import moviepy as mpe
from PIL import Image
from moviepy.video.fx.resize import resize
from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip
from moviepy.audio.AudioClip import CompositeAudioClip

from os.path import isfile, join
from youtube import upload_video
#@tool("createVideo")
def createVideo():
    """
    Use this tool when prompted to make a video or reddit video, if you need to choose an option for a reddit
    choose 0 or 1. Do not use more than once in a row, if already used go to upload_video tool if asked to upload the video
    """

    config = configparser.ConfigParser()

    config.read('config.ini')
    #outputDir = config["General"]["OutputDirectory"]
    outputDir = "outputvid"

    startTime = time.time()


    # Get script from reddit
    # If a post id is listed, use that. Otherwise query top posts
    if (len(sys.argv) == 2):
        script = reddit.getContentFromId(outputDir, sys.argv[1])
    else:
        postOptionCount = int(config["Reddit"]["NumberOfPostsToSelectFrom"])
        script = reddit.getContent(r"outputvid", postOptionCount)
    fileName = script.getFileName()
    title = script.title
    print(title)


    # Create screenshots
    screenshot.getPostScreenshots(fileName, script)

    # Setup background clip
    #bgDir = config["General"]["BackgroundDirectory"]
    #bgPrefix = config["General"]["BackgroundFilePrefix"]
    #bgFiles = [f for f in listdir(bgDir) if isfile(join(bgDir, f))]
    #bgCount = len(bgFiles)
    #bgIndex = random.randint(0, bgCount-1)
    #backgroundVideo = VideoFileClip(
    #    filename=f"{bgDir}/{bgPrefix}{bgIndex}.mp4",
    #    audio=False).subclip(0, script.getDuration())
    backgroundVideo = VideoFileClip("backgroundvid/SpicySauce Parkour 01.mp4")
    w, h = backgroundVideo.size


    def __createClip(screenShotFile, audioClip, marginSize):
        imageClip = ImageClip(
            screenShotFile,
            duration=audioClip.duration
            ).set_position(("center", "center"))
        imageClip = imageClip.resize(width=(w-marginSize))
        #imageClip = resize(ImageClip, w-marginSize)


        #pil_image = Image.open(screenShotFile)
       # resized_image = pil_image.resize((w, h), resample=Image.Resampling.LANCZOS)
        #imageClip = imageClip.resize(width=(w - marginSize), resample=Image.Resampling.LANCZOS)
        videoClip = imageClip.set_audio(audioClip)
        videoClip.fps = 1
        return videoClip

    # Create video clips
    print("Editing clips together...")
    clips = []
    print("a")
    marginSize = int(config["Video"]["MarginSize"])
    print(config["Video"]["MarginSize"])
    if not hasattr(script, "titleSCFile") or not hasattr(script, "titleAudioClip"):
        raise AttributeError("script object is missing required attributes: 'titleSCFile' or 'titleAudioClip'")

    print(f"ScreenShot File: {script.titleSCFile}")
    print(f"Audio Clip: {script.titleAudioClip}")
    print(f"Margin Size: {marginSize}")
    clips.append(__createClip(script.titleSCFile, script.titleAudioClip, marginSize))
    print("a")
    for comment in script.frames:
        clips.append(__createClip(comment.screenShotFile, comment.audioClip, marginSize))
    print("c")
    # Merge clips into single track
    contentOverlay = concatenate_videoclips(clips).set_position(("center", "center"))
    print("a")
    # Compose background/foreground
    final = CompositeVideoClip(
        clips=[backgroundVideo, contentOverlay], 
        size=backgroundVideo.size).set_audio(contentOverlay.audio)
    print("a")
    final.duration = script.getDuration()
    print("a")
    final.set_fps(backgroundVideo.fps)
    print("d")
    # Write output to file
    print("Rendering final video...")
    bitrate = config["Video"]["Bitrate"]
    threads = config["Video"]["Threads"]
    outputFile = f"{outputDir}/{fileName}.mp4"
    final.write_videofile(
        outputFile, 
        codec = 'mpeg4',
        threads = threads, 
        bitrate = bitrate
    )
    print(f"Video completed in {time.time() - startTime}")
    endTime = time.time()
    print(f"Total time: {endTime - startTime}")
    #upload_video("reddit video", "video description", outputFile)
    my_clip = VideoFileClip(outputFile)
    audio_background = AudioFileClip('backgroundvid/summer-memories-270159.mp3')
    adjusted_audio = audio_background.volumex(0.2)

    background_audio_adjusted = adjusted_audio.subclip(0, my_clip.duration)

    final_audio = CompositeAudioClip([my_clip.audio, background_audio_adjusted])
    final_clip = my_clip.set_audio(final_audio)
    final_clip.write_videofile(f"outputvid/{fileName}(audio).mp4")

    print(final_clip)
    aai.settings.api_key = "2895823538bb48229386bb84312dc133"

    transcriber = aai.Transcriber()
    import pysubs2
    transcript = transcriber.transcribe(f"outputvid/{fileName}(audio).mp4")
    srt = transcript.export_subtitles_srt()

    with open("subtitles.srt", "w") as f:
        f.write(srt)
    def group_words_in_srt(input_srt, output_ass):
        subs = pysubs2.load(input_srt, encoding="utf-8")
        new_events = []

        for line in subs:
            words = line.text.split()
            grouped_lines = [" ".join(words[i:i + 4]) for i in range(0, len(words), 4)]
            start = line.start
            duration = (line.end - line.start) // len(grouped_lines)

            for i, group in enumerate(grouped_lines):
                new_line = pysubs2.SSAEvent(
                    start=start + i * duration,
                    end=start + (i + 1) * duration,
                    text=group
                )
                new_events.append(new_line)

        subs.events = new_events
        subs.styles["Default"].fontname = "Arial"
        subs.styles["Default"].fontsize = 40
        subs.styles["Default"].alignment = 2  # Bottom-center
        subs.save(output_ass)

    # group_words_in_srt("adjusted_subtitles.srt", "custom_subtitles.ass")

    aai.settings.api_key = "2895823538bb48229386bb84312dc133"


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
    def sanitize_filename(filename):
        # Remove invalid characters entirely
        return ''.join(c for c in filename if c not in '<>:"/\\|?*')

    # Sanitize the title
    sanitized_title = sanitize_filename(title)

    video_path = f"outputvid/{fileName}(audio).mp4"
    srt_path = "subtitles.srt"
    output_path = f"output/{sanitized_title}.mp4"

    add_subtitles(video_path, srt_path, output_path)



    return f"video saved at {output_path} and the title of the video is {title}"
    # Preview in VLC for approval before uploading
''' if (config["General"].getboolean("PreviewBeforeUpload")):
        vlcPath = f"outputvid/{outputFile}"
        p = subprocess.Popen([vlcPath, outputFile])
        print("Waiting for video review. Type anything to continue")
        wait = input()

    print("Video is ready to upload!")
    print(f"Title: {script.title}  File: {outputFile}")
    endTime = time.time()
    print(f"Total time: {endTime - startTime}")'''

if __name__ == "__main__":
    createVideo()