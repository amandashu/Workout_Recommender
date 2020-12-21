import sys
import json

sys.path.insert(0, 'src/data')
sys.path.insert(0, 'src/utils')

from scrape import scrape_data
from clean import remove_data

def main(targets):
    if 'clean' in targets:
        remove_data()

    if 'data' in targets:
        with open('config/chromedriver.json') as fh:
            chromedriver_path = json.load(fh)['chromedriver_path']

        with open('config/data-params.json') as fh:
            data_params = json.load(fh)
            
        scrape_data(chromedriver_path, **data_params)

    return

if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
