import pandas as pd
from top_popular import top_popular, evaluate_top_popular
from light_fm import light_fm, evaluate_light_fm
import warnings

warnings.filterwarnings("ignore")

def run_models(data_dct):

    # Top Pop ######################################################
    print("\nRunning Top Popular...")
    predictions, _ = top_popular(data_dct['user_item_interactions'])
    
    top_pop_ndcg = evaluate_top_popular(data_dct['train_df'],
                                        data_dct['test_ui_matrix'],
                                        data_dct['item_map'])
    print('Average NDCG of Top Popular: ' + str(top_pop_ndcg))

    # LightFM ######################################################
    print("\nRunning LightFM...")
    pred = light_fm(data_dct)

    light_fm_ndcg = evaluate_light_fm(data_dct, pred)
    print('Average NDCG of LightFM: ' + str(light_fm_ndcg))
