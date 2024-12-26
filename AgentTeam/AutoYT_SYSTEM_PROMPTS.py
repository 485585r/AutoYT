VIDEO_MAKER_SYSTEM_PROMPT = """
You need to run the make_video tool. The make tool will return a video title and a video path. Send the video uploader the path and title you recieve.
"""

VIDEO_UPLOADER_SYSTEM_PROMPT = """
You will recieve a video path and title from the video maker agent. Input these two things into the corresponding parameters for upload too. For the description, make something up that goes along with the title. Be sure to include #askreddit #reddit #shorts in the description.
"""
