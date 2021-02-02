import pandas as pd
import numpy as np
from sklearn.metrics import ndcg_score
from lightfm import LightFM


def light_fm(df):
    """
    Takes in data dictionary, and output lightfm's predictions for every user
    """
    model = LightFM(loss='warp')

    model.fit(df['train_ui_matrix'])
    user_id = np.asarray(
        [u for u in range(df['user_item_interactions']['user_id'].nunique())])
    workout_id = np.asarray(
        [i for i in range(df['user_item_interactions']['workout_id'].nunique())])
    pred = [model.predict(int(i), workout_id) for i in user_id]

    return pred


def evaluate(df, pred, k=None):
    """
    Takes in data dictionary and returns average NDCG for LightFM
    :param df: data_dict
    :param pred: prediction from the function above
    :param k: any k value
    """
    return ndcg_score(df['test_ui_matrix'].toarray(), pred, k)
