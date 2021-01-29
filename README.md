## Workout Recommender

A workout video recommender web application.

Authors: Amanda Shu, Peter Peng, Najeem Kanishka

### Data
The data is scraped from https://www.fitnessblender.com/. We are using the data for academic purposes only.

### Code Organization

- `run.py`: Run to get data and model results.
- `app.py`: Runs flask web application.
- `workout_db.sql`: Contains sql statements for creation of tables in database.

**Source**
- The `src/data` folder contains `scrape.py`, the web-scraping script that writes three data files into `data/raw` folder. `fbpreprocessing.py` takes these raw data files and outputs cleaned/transformed data files into `data/preprocessed` folder. `model_preprocessing` reads in preprocessed data and transforms the data into what is needed for model inputs.
- `src/models` contains `run_models.py` which trains and evaluates the models. Models are implemented in `lightm_fm.py` and `top_popular.py`
- The `src/utils` folder has `clean.py` which implements the standard target `clean`.
- The `src/app` folder holds files for the web application. `forms.py` ontains wtforms classes for registration/login pages.

**Config**: `data-params.json` has file paths outputs for data collection/preprocessing. To webscrape, this folder should also include `chromedriver.json`. To run the app, this folder should also include `db_config.json` which contains database configurations.

**Notebook**: Contains `eda.ipynb`, a notebook with exploratory data analysis on scraped data.

**Static**: Several css and javascript files for styling/theming of website.

**Templates**: Holds html files for the various endpoints.


### Run the Project Stages
- To get the data, run `python run.py data`. This scrapes the data and cleans the data and saves these files into `/data/raw` and `data/preprocessed` respectively.
  - Note: this assumes that there is a file `config/chromedriver.json` that specifies where the path to the downloaded chromedriver.exe file for your Chrome version lies. It looks like this:
  ```console
  {
    "chromedriver_path" : <filepath to chromedriver.exe>
  }
  ```
- To run model results, run `python run.py model`. This takes in the preprocessed data, trains the models, and prints out the NDCG scores for each model.
- Standard target `clean` is also implemented, and it will delete the `data` folder.
- Use `python app.py` to run the app locally.
  - Note: this assumes that there is a file `config/db_config.json`, which has database host, user, password, and name information.
