import numpy as np

################################
## use sklearn implementation ##
################################
def get_target_scores(external_indices, scores, dct):
    """
    Helper function to get input of sklearn ncdg:
    Given movie ids and their popularity score, as well as a dictionary mapping
    external ids to LightFM internal ids, return the list of popularity scores
    by LightFM internal id ordering
    """
    internal_indices = [dct[i] for i in external_indices]
    scores_by_internal = np.zeros(len(external_indices))
    scores_by_internal.put(internal_indices,scores)
    return scores_by_internal




#####################################
### our implementation of metrics ###
######################################

# def get_relevance_score(true_interactions, predictions):
#     """
#     Takes in a user's true interactions and predicted interactions and returns
#     binary relevance scores for predictions, where it is 1 if a user interacted with
#     the predicted workout else 0
#     """
#     pred_indices = predictions-1
#     prediction_bools = np.zeros(len(true_interactions))
#     prediction_bools[pred_indices,] = 1
#     matched = (prediction_bools==true_interactions).astype(int)
#     rel_scores = np.take(matched, pred_indices)
#     return rel_scores
#
# def cg(rel_scores, k=None):
#     """
#     Cumulative Gain: sum of relevance scores
#     """
#     if k is not None:
#         rel_scores = rel_scores[:k]
#     return sum(rel_scores)
#
# def dcg(rel_scores, k=None):
#     """
#     Discounted Cumulative Gain: sum of relevance scores, where each score is
#     scaled down by its rank in the list
#
#     See traditional formula of here:
#     DCG https://en.wikipedia.org/wiki/Discounted_cumulative_gain
#     """
#     if k is not None:
#         rel_scores = rel_scores[:k]
#
#     i_array = np.arange(1,len(rel_scores)+1)
#     dcg = sum(rel_scores/(np.log2(i_array+1)))
#     return dcg
#
# def ndcg(rel_scores, k=None):
#     """
#     Normalized Discounted Cumulative Gain: DCG/IDCG, where IDCG (Idealized
#     Discounted Cumulative Gain) is DCG of a perfectly sorted list
#     """
#     if k is not None:
#         rel_scores = rel_scores[:k]
#
#     perfect_sort = np.sort(rel_scores)[::-1]
#     idcg = dcg(perfect_sort)
#     ndcg = dcg(rel_scores)/idcg
#     if np.isnan(ndcg):
#         return 0
#     return ndcg
#
# def evaluate(true_interactions, predictions, method, k=None):
#     """
#     Evaluates metric (specified with method parameter) on a user's predictions
#     """
#     rel_scores = get_relevance_scores(true_interactions, predictions)
#     return method(rel_scores, k)
