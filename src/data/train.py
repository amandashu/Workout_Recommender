import os
import csv
import time
import pickle
import json
import pandas as pd
from lightfm.data import Dataset


def build_interactions(user_item_matrix_path, fbworkouts_clean_path):
    """
    Builds the user-item interaction matrix
    #TODO: Find a location for this, not sure to put in data or train
    """
    user_item_interactions = pd.read_csv(user_item_matrix_path)
    fbworkouts_features = pd.read_csv(fbworkouts_clean_path)

    dataset = Dataset()
    dataset.fit((x for x in user_item_interactions['user_id']),
        (x for x in user_item_interactions['workout_id']))

    num_users, num_items = dataset.interactions_shape()
    print('Num users: {}, num_items {}.'.format(num_users, num_items))

    (interactions, weights) = dataset.build_interactions(
        (row['user_id'], row['workout_id']) for _ , row in user_item_interactions.iterrows()
        )

    # TODO: Build item features
    print(repr(interactions))