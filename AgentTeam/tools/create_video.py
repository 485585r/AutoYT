from langchain.tools import tool
import sys
import os

# Add RedditVideoGenerator directory to sys.path
sys.path.append(os.path.abspath("C:/AutoYT/RedditVideoGenerator"))

from RedditVideoGenerator.main import createVideo

#Video Creation tool
@tool
def make_video():
    """make video"""
    path, title = createVideo()

    return f"THE PATH TO USE IS {path}, and the TITLE OF THE VIDEO IS {title}"
