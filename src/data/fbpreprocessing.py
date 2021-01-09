import pandas as pd
import numpy as np
import os

def clean_fbworkouts(fbworkouts_path):
    """
    Takes in fbworkouts.csv and outputs fbworkouts_clean.csv
    """
    return

def create_fbcommenters(comments_path, fbcommenters_path):
    """
    Takes in comments.csv and outputs fbcommenters.csv, which assigns id to each
    hash_id-profile combination
    """
    comments_df = pd.read_csv(comments_path, usecols=['hash_id','profile'])
    comments_df = comments_df.drop_duplicates()
    comments_df['user_id'] = np.arange(1, comments_df.shape[0] + 1)

    dirname = os.path.dirname(comments_path)
    comments_df.to_csv(fbcommenters_path, index=False)

def fb_preprocessing(fbworkouts_path, comments_path, fbcommenters_path):
    clean_fbworkouts(fbworkouts_path)
    create_fbcommenters(comments_path, fbcommenters_path)
