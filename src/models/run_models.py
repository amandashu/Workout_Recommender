import pandas as pd
from top_popular import top_popular

def run_models(user_item_interactions_path):
    # TODO: train/test split

    print("Running Top Popular...")
    user_item_interactions = pd.read_csv(user_item_interactions_path)
    predictions = top_popular(user_item_interactions, 30)
    print(predictions)
    # TODO: evaluate predictions
