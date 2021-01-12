import pandas as pd
import numpy as np
import os

def clean_fbworkouts(fbworkouts_path, fbworkouts_clean_path):
    """
    Takes in fbworkouts.csv and outputs fbworkouts_clean.csv
    """
    # reads workouts_df
    workouts_df = pd.read_csv(fbworkouts_path)

    # extracts the minutes from the column
    duration = workouts_df.duration.str.split().apply(lambda x: x[0] if x[1] == 'Minutes' else x)
    workouts_df.duration = duration.astype(int)

    def strip_special_chars_and_split(df, col):
        """
        This will clean up a given column in a dataframe inplace, and will remove
        any character that is not alphanumerical, a comma, or a slash
        """
        stripped_column = df[col].str.replace('[^a-zA-Z0-9/, ]', '', regex=True)
        df[col] = stripped_column.str.split(', ')
        return df

    # strip special characters from body_focus and convert to list with {'UpperBody', 'TotalBody', 'LowerBody', 'Core'}
    strip_special_chars_and_split(workouts_df, 'body_focus')
    strip_special_chars_and_split(workouts_df, 'training_type')
    strip_special_chars_and_split(workouts_df, 'equipment')


    # converts the calories burned from a range to a numerical mean
    duration = workouts_df.calorie_burn.str.split('-')
    duration = duration.apply(lambda x: (float(x[0]) + float(x[1])) / 2)
    workouts_df.calorie_burn = duration
    workouts_df = workouts_df.rename(columns={"calorie_burn": "mean_calorie_burn"})

    ## asserts that the categories are regular and contains no errors or miscategorizations
    #flatten = lambda t: [item for sublist in t for item in sublist]
    #assert set(flatten(workouts_df.body_focus.tolist())) == {'UpperBody', 'TotalBody', 'LowerBody', 'Core'}
    #assert set(flatten(workouts_df.training_type.tolist())) == {'Pilates', 'Plyometric',
    #    'Toning', 'Kettlebell', 'Barre', 'Low Impact', 'Strength Training', 'Cardiovascular',
    #    'Warm UpCool Down', 'StretchingFlexibility', 'BalanceAgility', 'HIIT'}
    #assert set(flatten(workouts_df.equipment.tolist())) == {'Bench', 'PhysioBall', 'Kettlebell', 'Mat',
    #    'Aerobics Step', 'No Equipment', 'Exercise Band', 'Sandbag',
    #    'Barbell', 'Dumbbell', 'Stationary Bike', 'Jump Rope', 'Medicine Ball'}

    # OHE Encoder Function
    def OHEListEncoder(df, col, drop=True):
        """
        Given a dataframe and a column, return a OHE encoding of the column
        df: pandas dataframe
        col: str, name of the column to encode
        drop: Boolean, drops column from dataframe (default = True)
        """
        expanded_col = df[col].explode()
        if drop: df = df.drop([col], axis=1)
        return df.join(pd.crosstab(expanded_col.index, expanded_col))


    workouts_df = OHEListEncoder(workouts_df, 'body_focus')
    workouts_df = OHEListEncoder(workouts_df, 'training_type')
    # there is both a workout type and equipment named kettlebell, meaning that there will be overlap
    # therefore, we dropped the kettlebell from the "training_type", since you won't be doing
    # kettlebell exercises without the kettlebell; kettlebell will be encoded in the equipment section
    workouts_df = workouts_df.drop(['Kettlebell'], axis=1)
    workouts_df = OHEListEncoder(workouts_df, 'equipment')

    workouts_df.to_csv(fbworkouts_clean_path, index=False)


def create_fbcommenters(comments_path, fbcommenters_path):
    """
    Takes in comments.csv and outputs fbcommenters.csv, which assigns id to each
    hash_id-profile combination.

    Note: only fbcommenters who commented at least 5 times are kept
    """
    comments_df = pd.read_csv(comments_path, usecols=['hash_id'])
    counts= comments_df.groupby('hash_id').size()
    more_than_five = counts[counts>=5].index

    dct = {
        'hash_id': more_than_five,
        'user_id': np.arange(1, len(more_than_five) + 1)
    }

    out = pd.DataFrame(dct)
    out.to_csv(fbcommenters_path, index=False)

def create_UI_interactions(comments_path, fbcommenters_path, user_item_matrix_path):
    """
    Outputs user_item_interactinos.csv, containing columns user_id and workout_id
    """
    comments_df = pd.read_csv(comments_path, usecols=['hash_id', 'workout_id']).drop_duplicates() # some users might comment twice on the same video
    fbcommenters_df = pd.read_csv(fbcommenters_path)
    merged_df = pd.merge(comments_df, fbcommenters_df, on="hash_id", how='inner')
    interactions_df = merged_df[['user_id','workout_id']]
    interactions_df.to_csv(user_item_matrix_path, index=False)

def fb_preprocessing(fbworkouts_path, fbworkouts_clean_path, comments_path, fbcommenters_path, user_item_matrix_path):
    clean_fbworkouts(fbworkouts_path, fbworkouts_clean_path)
    create_fbcommenters(comments_path, fbcommenters_path)
    create_UI_interactions(comments_path, fbcommenters_path, user_item_matrix_path)
