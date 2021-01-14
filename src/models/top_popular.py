import pandas as pd
import numpy as np
from evaluation import get_target_scores
from sklearn.metrics import ndcg_score

def top_popular(df, k=None):
    """
    Takes in user_item_interactions data frame, and output the k most commented
    on workouts and their respective scores (# of comments)
    """
    workout_counts = df.groupby('workout_id').size().sort_values(ascending=False)
    preds = np.array(workout_counts.index)
    scores = np.array(workout_counts.values)

    # write predictions/scores to pickle file?

    if k is None:
        return preds, scores
    else:
        return preds[:k], scores[:k]

def evaluate_top_popular(train_df, test_ui_matrix, item_map, k=None):
    """
    Takes in training/testing data and returns average NDCG
    for top popular reccomender
    """
    y_true = test_ui_matrix.toarray()
    external_indices, scores = top_popular(train_df)
    y_score = get_target_scores(external_indices, scores, item_map)
    #print(ndcg_score([y_true[0]],[y_score])) #0.22977373086316666
    y_scores = [list(y_score)]*(y_true.shape[0])
    return ndcg_score(y_true, y_scores, k)
