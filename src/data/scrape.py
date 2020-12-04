import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_workout_links():
    """
    Goes through all (free?) workouts and returns lists of individual workout links
    """
    driver = webdriver.Chrome(os.path.abspath('../chromedriver'))
    driver.get("https://www.fitnessblender.com/videos?exclusive%5B%5D=0")

    all_links = []
    for page in range(29):
        print(page)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "contents"))
        )

        time.sleep(2)
        links = [content.get_attribute('href') for content in driver.find_elements_by_class_name('contents') if content.get_attribute('href') != None]
        all_links.append(links)

        next_btn = driver.find_element_by_class_name('iconfont-arrow-forward')
        next_btn.click()
    driver.close()

    with open('all_links.pickle', 'wb') as f:
        pickle.dump([i for j in all_links for i in j if i is not None], f)

    return [i for j in all_links for i in j if i is not None]


if __name__ == "__main__":
    get_workout_links()
    

def get_data(link):
    """
    Scrapes a workout link and returns dictionary of data, where the keys are column names and values are data values
    """

    return {'test1':'a','test2':'b'}

def scrape_data():
    """
    Writes data to csv
    """
    out_path = 'data/fbworkouts.csv'
    headers = ['test1','test2']

    out_path_exists = os.path.isfile(out_path)

    # create data folder containing csv if it doesn't yet exist
    dirname = os.path.dirname(out_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    # get workout links to scrape
    links = get_workout_links()

    with open(out_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, headers)

        # write headers if file doesn't yet exist
        if not out_path_exists:
            writer.writerow({x:x for x in headers})

        # go through each link and write data to csv
        for l in links:
            dct = get_data(l)
            writer.writerow(dct)

    return
