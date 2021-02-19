import datetime, time
import os

from PIL import Image
import numpy as np
from selenium import webdriver

interval = 30
# im_frame = Image.open(f'screenshot_nospot.png')
screenshot = None
driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get("https://www.snowbird.com/parking/#parking_reservation")
time.sleep(15)
n = 0
while True:
    try:
        print(datetime.datetime.now())


        elem1 = driver.find_element_by_xpath('//iframe')
        driver.switch_to.frame(elem1)
        driver.implicitly_wait(10)
        elem2 = driver.find_element_by_xpath('//div[2]/div/table/tbody/tr[3]/td[5]/div')
        elem2.screenshot(f'screenshot_{n}.png')
        im_frame = Image.open(f'screenshot_{n}.png')
        current_screenshot = np.array(im_frame)

        if screenshot is None:
            screenshot = current_screenshot.copy()
        else:
            img_diff = np.sum(screenshot.flatten() - current_screenshot.flatten()) / np.sum(current_screenshot.flatten())
            if img_diff > 0.05:
                os.system('say "Find new spot!"')
                elem2.screenshot('new_spot.png')
            else:
                os.remove(f'screenshot_{n-1}.png')
        driver.refresh()
        n += 1
    except Exception as e:
        print(e)
        os.system('say "something is wrong"')

    time.sleep(interval)