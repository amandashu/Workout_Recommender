import os
import csv

def get_workout_links():
    """
    Goes through all (free?) workouts and returns lists of individual workout links
    """
    return ['https://www.fitnessblender.com/videos/daniel-s-upper-body-strength-workout-for-people-who-get-bored-easily']


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
