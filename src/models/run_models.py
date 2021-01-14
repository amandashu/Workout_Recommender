import pandas as pd
from top_popular import top_popular, evaluate_top_popular

def run_models(data_dct):


    print("\nRunning Top Popular...")
    predictions, _ = top_popular(data_dct['user_item_interactions'])
    print(len(predictions))

    top_pop_ndcg = evaluate_top_popular(data_dct['train_df'],
                                        data_dct['test_ui_matrix'],
                                        data_dct['item_map'])
    print('Average NDCG of Top Popular: ' + str(top_pop_ndcg))

    print("\nRunning LightFM...")
