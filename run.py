import sys
import json

sys.path.insert(0, 'src/data')
sys.path.insert(0, 'src/utils')

from clean import remove_data
from scrape import scrape_data
from fbpreprocessing import fb_preprocessing

def main(targets):
    if 'clean' in targets:
        remove_data()
        print("Data cleaned.")

    if 'data' in targets:
        with open('config/chromedriver.json') as fh:
            chromedriver_path = json.load(fh)['chromedriver_path']

        with open('config/data-params.json') as fh:
            data_params = json.load(fh)

        print("Scraping data...")
        scrape_data(chromedriver_path, data_params['all_links_pickle_path'],
                    data_params['fbworkouts_path'], data_params['comments_path'])

        print("Preprocessing...")
        fb_preprocessing(data_params['fbworkouts_path'],
                         data_params['comments_path'], data_params['fbcommenters'])

    return


if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
