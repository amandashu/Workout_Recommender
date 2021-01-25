import pandas as pd
import numpy as np
from sklearn.metrics import ndcg_score
from sklearn.preprocessing import normalize, MinMaxScaler

from surprise import KNNBasic, SVD
from surprise import Dataset
from surprise import Reader
from surprise.model_selection import cross_validate, KFold
from surprise import accuracy


def knn(df):
    """
    Takes in user_item_interactions data frame, and output the k most commented
    on workouts and their respective scores (# of comments)
    :param df: data dict
    """
    train_df = df['train_df']
    train_df['rating'] = 1
    testset = df['test_df']
    testset['test_df'] = 1

    # A reader is still needed but only the rating_scale param is requiered.
    reader = Reader(rating_scale=(0, 1))

    # The columns must correspond to user id, item id and ratings (in that order).
    train_df = Dataset.load_from_df(train_df, reader)
    testset = Dataset.load_from_df(testset, reader)

    mms = MinMaxScaler()

    algo = KNNBasic()

    # train and test algorithm.
    algo.fit(train_df)
    predictions = algo.test(testset)

    # Compute and print Root Mean Squared Error
    accuracy.rmse(predictions, verbose=True)

def evaluate(df, pred, k=None):
    """
    Takes in data dictionary and returns average NDCG for LightFM
    :param df: data_dict
    :param pred: prediction from the function above
    :param k: any k value
    """
    return ndcg_score(df['test_ui_matrix'].toarray(), pred, k)
