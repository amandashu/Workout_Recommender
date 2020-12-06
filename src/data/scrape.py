import os
import csv
import time
import pickle
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


all_links_pickle_path = 'data/all_links.pickle'

def get_workout_links(chromedriver_path):
    """
    Goes through all free workouts and writes list of workout links to pickle file
    """
    fb_link = "https://www.fitnessblender.com/videos?exclusive%5B%5D=0"
    driver = webdriver.Chrome(chromedriver_path)
    driver.get(fb_link)

    all_links = []
    for page in range(29):
        #print(page)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "contents"))
        )

        time.sleep(2)
        links = [content.get_attribute('href') for content in driver.find_elements_by_class_name('contents') if content.get_attribute('href') != None]
        all_links.append(links)

        next_btn = driver.find_element_by_class_name('iconfont-arrow-forward')
        next_btn.click()
    driver.close()

    # create data folder if it doesn't yet exist
    dirname = os.path.dirname(all_links_pickle_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(all_links_pickle_path, 'wb') as f:
        pickle.dump([i for j in all_links for i in j if i is not None], f)


def get_data(workout_link):
    """
    Scrapes a workout link and returns dictionary of data, where the keys are column names and values are data values
    """

    return {'test1':'a','test2':'b'}


def scrape_data():
    """
    Writes data to csv
    """
    fbworkouts_out_path = 'data/fbworkouts.csv'
    headers = ['test1','test2']

    # scrape all workout links to all_links.pickle if all_links.pickle doesn't yet exist
    if not os.path.isfile(all_links_pickle_path):
        with open('config/chromedriver.json') as fh:
            chromedriver_path = json.load(fh)['chromedriver_path']

        get_workout_links(chromedriver_path)


    # with open(out_path, 'a', newline='') as f:
    #     writer = csv.DictWriter(f, headers)
    #
    #     # write headers if fbworkouts.csv doesn't yet exist
    #     if not os.path.isfile(fbworkouts_out_path):
    #         writer.writerow({x:x for x in headers})
    #
    #     # go through each link and write data to csv
    #     for l in links:
    #         dct = get_data(l)
    #         writer.writerow(dct)

    return
