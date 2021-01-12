import sys
import json

sys.path.insert(0, 'src/data')
sys.path.insert(0, 'src/utils')

from clean import remove_data
from scrape import scrape_data
from fbpreprocessing import fb_preprocessing
from train import build_interactions

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
        scrape_data(chromedriver_path,
                    data_params['all_links_pickle_path'],
                    data_params['fbworkouts_path'],
                    data_params['comments_path'])

        print("Preprocessing...")
        fb_preprocessing(
            fbworkouts_path = data_params['fbworkouts_path'],
            fbworkouts_clean_path = data_params['fbworkouts_clean_path'],
            comments_path = data_params['comments_path'],
            fbcommenters_path = data_params['fbcommenters'],
            user_item_matrix_path = data_params['user_item_matrix_path']
            )

    if 'train' in targets:
        with open('config/data-params.json') as fh:
            data_params = json.load(fh)

        build_interactions(data_params['user_item_matrix_path'], data_params['fbworkouts_clean_path'])

    return


if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
