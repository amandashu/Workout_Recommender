## Workout Recommender

This repository contains code for a workout recommender project.

Authors: Amanda Shu, Peter Peng, Najeem Kanishka

## Data
The data is scraped from https://www.fitnessblender.com/.

## Code Organization

#### Source
The `src` folder contains subfolders `data` and `utils`.

In the `src/data` folder:
- `scrape.py`: the web-scraping script that writes three data files into `data` folder. `all_links.pickle` contains the list of links to scrape, `comments.csv` contains the comments data, and `fbworkouts.csv` contains the individual workout attributes.

In the `src/utils` folder:
- `clean.py`: contains function `remove_data` that implements the standard target `clean`

## Run the Results
To web scrape the data, run this command:
```console
python run.py data
```

Note: this assumes that there is a file `config/chromedriver.json` that specifies, where the path to the downloaded chromedriver.exe file for your Chrome version lies. It might look like this:
```console
{
  "chromedriver_path" : "C:/Users/JohnDoe/Downloads/chromedriver_win32/chromedriver.exe"
}
```

Standard target `clean` is also implemented, and it will delete `data` folder.
