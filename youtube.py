import os
import time

from langchain_core.tools import tool
from pydantic import Field, BaseModel


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service


options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--no-sandbox")
options.add_argument("--log-level=3")
options.add_argument(r"user-data-dir=C:\Users\shija\AppData\Local\Google\Chrome for Testing\User Data")
options.binary_location = r"C:\Users\shija\Downloads\chrome-win64(1)\chrome-win64\chrome.exe"

chromedriver_path = "C:\gs3629\ChromeDriver\chromedriver-win64\chromedriver.exe"


print(
    "\033[1;31;40m IMPORTANT: Put one or more videos in the *videos* folder in the bot directory. Please make sure to name the video files like this --> Ex: vid1.mp4 vid2.mp4 vid3.mp4 etc..")
time.sleep(6)

howmany = 1
class videoParameters(BaseModel):
    title: str = Field(
        description="The appropriate title for the reddit video being generated which is returned by createvideo or the manual user reference from input (IMPORTANT, add space #Shorts after the title, for example: {TITLE} #Shorts"
    )
    description: str = Field(
        description="Description of the video being uploaded (be creative with this and use your imagination based on the title), use the title as reference which is returned from tool createvideo or the manual user reference from input, also add one word tags  to the title in the description underneath the main description with this as an example: #food #reddit #story etc. IMPORTANT always add a tag #Shorts"
    )
    video_path: str = Field(
        description="the string path of the output video file, which is returned by createvideo, or the file that is given to you manually by the user"
    )
@tool("upload_video", args_schema=videoParameters)
def upload_video(title: str, description: str, video_path: str):
    '''Use this for when you need to either upload a pre-existing video that the user gives
       reference too or in tangent with createvideo tool, for when the user tells you to create and
       upload a video use this tool to upload the video after creation.'''

    print("using upload_video")
    print("title: " + title)
    print("description: " + description)
    print("video_path: " + video_path)
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
    title_input.send_keys(title)
    time.sleep(3)

    # Set the description
    description_input = bot.find_element(By.XPATH,
                                         '//*[@id="description-textarea"]')  # Adjust XPath as needed
    description_input.send_keys(description)
    next_button = bot.find_element(By.XPATH, '//*[@id="next-button"]')
    for i in range(3):
        next_button.click()
        time.sleep(1)

    done_button = bot.find_element(By.XPATH, '//*[@id="done-button"]')
    done_button.click()
    time.sleep(40)
    input("Press Enter to close the browser...")
    bot.quit()

#if __name__ == "__main__":
#upload_video(title="testvideo1", description="test1", video_path=r"C:\Users\shija\PycharmProjects\AutoYT2\output\If somebody offered you $1,000 because you're ugly, what is the appropriate response.mp4")


'''if __name__ == "__main__":
    from selenium import webdriver

    # Initialize WebDriver
    driver = webdriver.Chrome()

    print(driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0])
    #upload_video("reddit video", "video description", "outputvid/2024-12-24-1hl30mi.mp4")'''
