**Overview**
----------------

A python project made for automating the creation and uploading of r/AskReddit Youtube videos.

Uses the Reddit API for querying top posts, and uses the power of Selenium to automate screenshotting posts and comments.

This project also uses Selenium to automate Youtube Video uploading.

Because we wanted to have custom descriptions with hashtags, we used LangGraph to create a two team agent - one agent for creating the videos and one for uploading the videos to youtube. This uploading agent is able to generate its own description and hashtags.

For creating the videos, we used MoviePy.

To run this code, navigate to AgentTeam and run the video_maker_team_assembly.py file.

**How to run**
-----------------

1. pip install requirements.txt
2. Set up API keys in define_vars and config.ini.
3. Create folders in your main directory named output, outputvid, Voiceovers, and Screenshots
4. Download a chromedriver and chromium that matches each others version [here](https://googlechromelabs.github.io/chrome-for-testing/), while adding the paths in youtube.py (make sure they are also in your system path)
5. Then put the paths in the code as shown below: ![image](https://github.com/user-attachments/assets/88b37c90-5e2f-4095-b273-4cf5d1a40279)
6. Run historian.py — This is the LangChain agent that connects everything together.
7. You will then be prompted to choose a reddit topic (It will display top 10, but you can set it to more than 10 in *config.ini*: NumberOfPostsToSelectFrom, this constantly updates)
8. Pick a number according to the choice:

![image](https://github.com/user-attachments/assets/e478252d-7da5-413b-81ed-433d8ce55fb4)

9. Wait until it uploads automatically, chrome browser will be uploaded twice when taking screenshots and uploading videos

_Finalized product can be seen here:_ [Example Youtube Video](https://youtube.com/shorts/ukS6cI8FPhg)


