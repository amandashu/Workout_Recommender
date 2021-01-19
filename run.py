import sys
import json

sys.path.insert(0, 'src/data')
sys.path.insert(0, 'src/utils')
sys.path.insert(0, 'src/models')

from clean import remove_data
from scrape import scrape_data
from fbpreprocessing import fb_preprocessing
# from train import build_interactions
from train import get_data
from run_models import run_models

def main(targets):
    if 'clean' in targets:
        remove_data()
        print("Data cleaned.")

    with open('config/data-params.json') as fh:
        data_params = json.load(fh)

    if 'data' in targets:
        with open('config/chromedriver.json') as fh:
            chromedriver_path = json.load(fh)['chromedriver_path']

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
            user_item_interactions_path = data_params['user_item_interactions_path']
            )

    # if 'train' in targets:
    #     build_interactions(data_params['user_item_interactions_path'], data_params['fbworkouts_clean_path'])

    if 'model' in targets:
        data = get_data(data_params['user_item_interactions_path'])
        run_models(data)

    return


if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
