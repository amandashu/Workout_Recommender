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


def pred_i(df, user_id):
    """
    Takes in data dictionary and external user id, and output lightfm's predictions for this user
    """
    model = LightFM(loss='warp')

    model.fit(df['train_ui_matrix'])
    workout_id = np.asarray(
        [i for i in range(df['user_item_interactions']['workout_id'].nunique())])
    scores = model.predict(get_internal_user_id(
        df['user_map'], user_id), workout_id)

    # format output in accordance to external index (our workout ID)
    external_indices = [get_external_workout_id(
        df['item_map'], i)-1 for i in workout_id]
    scores_by_internal = np.zeros(len(workout_id))
    scores_by_internal.put(external_indices, scores)
    return np.argsort(scores_by_internal)


def get_internal_workout_id(mapping, workout_id):
    return mapping[workout_id]


def get_internal_user_id(mapping, user_id):
    return mapping[user_id]


def get_external_workout_id(mapping, internal_workout_id):
    return {v: k for k, v in mapping.items()}[internal_workout_id]


def get_external_user_id(mapping, internal_user_id):
    return {v: k for k, v in mapping.items()}[internal_user_id]


def evaluate(df, pred, k=None):
    """
    Takes in data dictionary and returns average NDCG for LightFM
    :param df: data_dict
    :param pred: prediction from the function above
    :param k: any k value
    """
    return ndcg_score(df['test_ui_matrix'].toarray(), pred, k)
