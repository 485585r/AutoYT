from moviepy import VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip
from . import reddit, screenshot
import time
import subprocess
import random
import configparser
import sys
import math
from os import listdir
from os.path import isfile, join

outputDir = "C:\AutoYT\AutoYT\RedditVideoGenerator\OutputVideos"

postOptionCount = 3

def createVideo():
    config = configparser.ConfigParser()
    config.read('config.ini')

    startTime = time.time()

    # Get script from reddit
    # If a post id is listed, use that. Otherwise query top posts
    if (len(sys.argv) == 2):
       script = reddit.getContentFromId(outputDir, sys.argv[1])
    else:
        script, title = reddit.getContent(outputDir, postOptionCount)
    fileName = script.getFileName()


    print(f"title is {title}")
    # Create screenshots
    screenshot.getPostScreenshots(fileName, script)

    # Setup background clip
    bgDir = "C:\AutoYT\AutoYT\RedditVideoGenerator\BackgroundVideos"
    bgPrefix = "BG_"
    bgFiles = [f for f in listdir(bgDir) if isfile(join(bgDir, f))]
    bgCount = len(bgFiles)
    bgIndex = random.randint(0, bgCount-1)
    backgroundVideo = VideoFileClip(
        filename=f"{bgDir}/{bgPrefix}{bgIndex}.mp4", 
        audio=False).subclipped(0, script.getDuration())
    w, h = backgroundVideo.size

    def __createClip(screenShotFile, audioClip, marginSize):
        imageClip = ImageClip(
            screenShotFile,
            duration=audioClip.duration
            ).with_position(("center", "center"))
        imageClip = imageClip.resized(width=(w-marginSize))
        videoClip = imageClip.with_audio(audioClip)
        videoClip.fps = 1
        return videoClip

    # Create video clips
    print("Editing clips together...")
    clips = []
    marginSize = 64
    clips.append(__createClip(script.titleSCFile, script.titleAudioClip, marginSize))
    for comment in script.frames:
        clips.append(__createClip(comment.screenShotFile, comment.audioClip, marginSize))

    # Merge clips into single track
    contentOverlay = concatenate_videoclips(clips).with_position(("center", "center"))

    # Compose background/foreground
    final = CompositeVideoClip(
        clips=[backgroundVideo, contentOverlay], 
        size=backgroundVideo.size).with_audio(contentOverlay.audio)
    final.duration = script.getDuration()
    final.with_fps(backgroundVideo.fps)

    # Write output to file
    print("Rendering final video...")
    bitrate = "8000k"
    threads =12
    outputFile = f"{outputDir}/{fileName}.mp4"
    final.write_videofile(
        outputFile, 
        codec = 'mpeg4',
        threads = threads, 
        bitrate = bitrate
    )
    print(f"Video completed in {time.time() - startTime}")


    print("Video is ready to upload!")
    print(f"Title: {script.title}  File: {outputFile}")
    endTime = time.time()
    print(f"Total time: {endTime - startTime}")

    return outputFile, title
if __name__ == "__main__":
    createVideo()