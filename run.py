import sys

sys.path.insert(0, 'src/data')
sys.path.insert(0, 'src/analysis')
sys.path.insert(0, 'src/utils')

from scrape import scrape_data
from clean import remove_data

def main(targets):
    ### standard targets
    if 'clean' in targets:
        remove_data()

    if 'data' in targets: # defaults to dsmlp data
        scrape_data()

    return

if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
