from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Config
screenshotDir = "C:\AutoYT\AutoYT\RedditVideoGenerator\Screenshots"
screenWidth = 400
screenHeight = 800

def getPostScreenshots(filePrefix, script):
    print("Taking screenshots...")
    driver = __setupDriver(script.url)
    script.titleSCFile = __takeScreenshot(filePrefix, driver)
    for commentFrame, i in zip(script.frames, range(len(script.frames))):
        filePrefix = f'/comment_{i}'
        commentFrame.screenShotFile = __takeScreenshot(filePrefix, driver, f"[thingid='t1_{commentFrame.commentId}']")
    driver.quit()

def __takeScreenshot(filePrefix, driver, handle="shreddit-post.block"):
    shadow_host = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, handle))
    )

    fileName = f"{screenshotDir}/{filePrefix}-{handle}.png"


    # Take a screenshot of the shadow host element
    shadow_host.screenshot(fileName)
    print(f"Screenshot saved to {fileName}")
    return fileName




def __setupDriver(url: str):
    driver = webdriver.Chrome()

    driver.set_window_size(width=screenWidth, height=screenHeight)
    driver.get(url)

    return driver