import pandas as pd

def top_popular(df, k):
    """
    Takes in user_item_interactions data frame, and output the k most commented
    on workouts
    """
    workout_counts = df.groupby('workout_id').size().sort_values(ascending=False)
    return list(workout_counts.index)[:k]
