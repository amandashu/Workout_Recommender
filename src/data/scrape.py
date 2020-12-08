import os
import csv
import time
import pickle
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# set all_links.pickle path
all_links_pickle_path = 'data/all_links.pickle'
fbworkout_headers = ['duration', 'calorie_burn', 'difficulty', 'equipment', 'training_type', 'body_focus', 'youtube_link']
comment_headers = ['username','comment_time']

# driver variable
with open('config/chromedriver.json') as fh:
    chromedriver_path = json.load(fh)['chromedriver_path']
driver = webdriver.Chrome(chromedriver_path)

def get_workout_links(chromedriver_path):
    """
    Goes through all free workouts and writes list of workout links to pickle file
    """
    fb_link = "https://www.fitnessblender.com/videos?exclusive%5B%5D=0"
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


def get_fbdata(workout_link):
    """
    Scrapes a workout link and returns dictionary of data, where the keys are column names and values are data values
    """
    # load the page
    driver.get(workout_link)
    time.sleep(5)

    # scroll down to load comments
    comments = driver.find_element_by_id("comments")
    driver.execute_script("arguments[0].scrollIntoView();", comments)

    # keep pressing load more button and scrolling down until button doesn't exist
    while True:
        try:
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(), 'Load More Comments')]")
                    )).click()
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        except Exception as e:
            break

    # get html
    html = driver.page_source
    soup = BeautifulSoup(html, "html5lib")

    # get workout details
    span_details = []
    for span in soup.find_all("span",{"class":"detail-value demi"}):
        if span.find('a'):
            span_details.append(span.find('a').get('href'))
        elif span.find_previous('span').text == 'Difficulty:':
            span_details.append(span.text[0])
        else:
            span_details.append(span.text)

    details_dct = dict(zip([x for x in fbworkout_headers if x!= 'body_focus'], span_details))
    details_dct['body_focus'] = soup.find("span",{"class":"focus demi"}).text

    #TODO implement comment scraping
    comments_df = pd.DataFrame({'username':['a','b'],
                                'comment_time': ['3 weeks','4 weeks']})
    return details_dct, comments_df


def scrape_data():
    """
    Writes data to csv
    """
    # out csv paths
    fbworkouts_out_path = 'data/fbworkouts.csv'
    comments_out_path = 'data/comments.csv'

    # headers
    fbheaders = ['workout_id'] + fbworkout_headers
    cheaders = ['workout_id'] + comment_headers

    # write headers if fbworkouts.csv doesn't yet exist
    if not os.path.isfile(fbworkouts_out_path):
        with open(fbworkouts_out_path, 'a', newline='') as f:
            fbwriter = csv.DictWriter(f, fbheaders)
            fbwriter.writerow({x:x for x in fbheaders})

    # write headers if comments.csv doesn't yet exist
    if not os.path.isfile(comments_out_path):
        with open(comments_out_path, 'a', newline='') as g:
            cwriter = csv.DictWriter(g, cheaders)
            cwriter.writerow({x:x for x in cheaders})

    # scrape all workout links to all_links.pickle if all_links.pickle doesn't yet exist
    if not os.path.isfile(all_links_pickle_path):
        get_workout_links(chromedriver_path)

    # get workout links
    with open(all_links_pickle_path, 'rb') as file:
        links = pickle.load(file)

    links = links[:5]

    #write data
    with open(fbworkouts_out_path, 'a', newline='') as f, open(comments_out_path, 'a', newline='') as g:
        fbwriter = csv.DictWriter(f, fbheaders)
        cwriter = csv.DictWriter(g, cheaders)

        #go through each link and write data to both csvs
        for i in range(len(links)):
            l = links[i]

            dct, df  = get_fbdata(l)

            # write details
            dct['workout_id'] = i+1
            fbwriter.writerow(dct)

            # write comments
            df.insert(0, 'movie id', i+1)
            df.to_csv(g, header=False, index=False)
    driver.close()
    return
