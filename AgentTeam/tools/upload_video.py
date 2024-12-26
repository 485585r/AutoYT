from pydantic import BaseModel, Field
from langchain.tools import tool
from RedditVideoGenerator.youtube import upload_video

#Detailed descriptions of the inputs required for the upload tool
class UploadInput(BaseModel):
    video_title: str = Field(description="The title that you get from the video maker agent")
    video_description: str = Field(description="Must be a description with a lot of keywords and tags associated with what the reddit post is about. Be sure to include #reddit #askreddit #shorts")
    video_path: str = Field(description="The video path you get from the video maker agent")

#Upload tool
@tool("upload", args_schema=UploadInput)
def upload(video_title, video_description, video_path):
    """this is the tool you use for uploading the video to youtube. requires the video title, description, and path."""
    upload_video(video_title=video_title, video_description=video_description, video_path=video_path)

