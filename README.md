A python project made for automating the creation and uploading of r/AskReddit Youtube videos.

Uses the Reddit API for querying top posts, and uses the power of Selenium to automate screenshotting posts and comments.

This project also uses Selenium to automate Youtube Video uploading.

Because I wanted to have custom descriptions with hashtags, I used LangGraph to create a two team agent - one agent for creating the videos and one for uploading the videos to youtube. This uploading agent is able to generate its own description and hashtags.

For creating the videos, I used MoviePy.

To run this code, navigate to AgentTeam and run the video_maker_team_assembly.py file.