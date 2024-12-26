import time, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service


options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--no-sandbox")
options.add_argument("--log-level=3")
options.add_argument("user-data-dir=C:\\Users\\kaide\\AppData\\Local\\Google\\Chrome for Testing\\User Data")
options.binary_location = "C:/Users/kaide/OneDrive/Desktop/chrome-win64/chrome.exe"

chromedriver_path = "C:\\Users\\kaide\\OneDrive\\Desktop\\chromedriver-win64\\chromedriver.exe"

print(
    "\033[1;31;40m IMPORTANT: Put one or more videos in the *videos* folder in the bot directory. Please make sure to name the video files like this --> Ex: vid1.mp4 vid2.mp4 vid3.mp4 etc..")
time.sleep(6)

howmany = 1

def upload_video(video_title, video_description, video_path):


    service = Service(executable_path=chromedriver_path)

    bot = webdriver.Chrome(options=options, service=service)

    bot.get("https://studio.youtube.com")
    time.sleep(3)


    upload_button = bot.find_element(By.XPATH, '//*[@id="upload-icon"]')
    upload_button.click()
    time.sleep(1)

    file_input = bot.find_element(By.XPATH, '//*[@id="content"]/input')
    simp_path = video_path
    abs_path = os.path.abspath(simp_path)
    file_input.send_keys(abs_path)

    time.sleep(7)

    title_input = bot.find_element(By.XPATH,
                                   '//*[@id="textbox"]')  # Adjust the XPath based on the page structure
    title_input.clear()
    title_input.send_keys(video_title)
    time.sleep(3)

    # Set the description
    description_input = bot.find_element(By.XPATH,
                                         '//*[@id="description-textarea"]')  # Adjust XPath as needed
    description_input.send_keys(video_description)



    next_button = bot.find_element(By.XPATH, '//*[@id="next-button"]')
    for i in range(3):
        next_button.click()
        time.sleep(1)

    done_button = bot.find_element(By.XPATH, '//*[@id="done-button"]')
    done_button.click()
    time.sleep(5)
    bot.quit()

if __name__ == "__main__":
    upload_video(video_path="C:\\AutoYT\\AutoYT\\RedditVideoGenerator\\OutputVideos\\2024-12-25-1hlstdp.mp4", video_description="fjf", video_title="lololol")