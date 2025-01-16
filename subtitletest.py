import subprocess
import assemblyai as aai
import moviepy
import ffmpeg
aai.settings.api_key = "2895823538bb48229386bb84312dc133"

transcriber = aai.Transcriber()
import pysubs2
transcript = transcriber.transcribe("outputvid/output1.mp4")
srt = transcript.export_subtitles_srt()
def adjust_subtitle_timing(input_srt, output_srt, offset_ms):
    subs = pysubs2.load(input_srt, encoding="utf-8")
    for line in subs:
        line.start += offset_ms
        line.end += offset_ms
    subs.save(output_srt)

with open("subtitles.srt", "w") as f:
    f.write(srt)
#adjust_subtitle_timing("subtitles.srt", "adjusted_subtitles.srt", -50)


def group_words_in_srt(input_srt, output_ass):
    subs = pysubs2.load(input_srt, encoding="utf-8")
    new_events = []

    for line in subs:
        words = line.text.split()
        grouped_lines = [" ".join(words[i:i+4]) for i in range(0, len(words), 4)]
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
#group_words_in_srt("adjusted_subtitles.srt", "custom_subtitles.ass")

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
    return f"subtitles added and saved to {output_file}"
video_path = "outputvid/output1.mp4"
srt_path = "subtitles.srt"
output_path = "output/output_with_subtitles.mp4"

add_subtitles(video_path, srt_path, output_path)