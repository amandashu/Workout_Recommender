import pandas as pd
import numpy as np
import os

def clean_fbworkouts(fbworkouts_path):
    """
    Takes in fbworkouts.csv and outputs fbworkouts_clean.csv
    """
    return

def create_fbcommenters(comments_path):
    """
    Takes in comments.csv and outputs fbcommenters.csv, which assigns id to each
    username-profile combination
    """
    comments_df = pd.read_csv(comments_path, usecols=['username','profile'])
    comments_df = comments_df.drop_duplicates()
    comments_df['user_id'] = np.arange(1, comments_df.shape[0] + 1)

    dirname = os.path.dirname(comments_path)
    comments_df.to_csv(dirname+ '/fbcommenters.csv', index=False)

def fb_preprocessing(fbworkouts_path, comments_path):
    clean_fbworkouts(fbworkouts_path)
    create_fbcommenters(comments_path)
