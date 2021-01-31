import pandas as pd
"""
TODO: this currently gets rid of the ordering of predictions -> need to change this
"""

def filter(workouts, user):
    """
    Takes in dataframe of workouts (with fbworkouts schema) and users series
    (with schema users) and returns a dictionary with body focus as keys and
    workout ids in lists, with workouts not matching users' preferences filtered
    out
    """
    def training_type_helper(str):
        """
        Takes in a workout's training types and returns True if at least
        one matches user's preferred training types else False
        """
        training_type_list = str.split(', ')
        for t in training_type_list:
            if user[t] == 1:
                return True
        return False

    def equipment_helper(str):
        """
        Takes in workout's required equipment and returns True if
        user has ALL of the required equipment else False or if workout lists
        no equipment
        """
        equipment_list = str.split(', ')
        if 'no_equipment' in equipment_list:
            return True
        for e in equipment_list:
            if e == 'no_equipment':
                pass
            elif user[e] == 0:
                return False
        return True

    def calorie_helper(series):
        """
        Takes in workout's series , and returns True if user's preferred min/max
        calorie range has some overlap with the workout's calorie range
        """
        if user['max_calories'] < series['min_calorie_burn'] or series['max_calorie_burn'] < user['min_calories']:
            return False
        return True

    def in_range_helper(x, attr):
        """
        Takes in workout's attr (difficulty or duration) and returns True if it is
        within the range of user's preferred attr range (inclusive)
        """
        if x >= user['min_' + attr] and x <= user['max_' + attr]:
            return True
        return False

    # filter
    workouts = workouts[workouts['duration'].apply(in_range_helper, args=('duration',))]
    workouts = workouts[workouts['difficulty'].apply(in_range_helper, args=('difficulty',))]
    workouts = workouts[workouts['equipment'].apply(equipment_helper)]
    workouts = workouts[workouts['training_type'].apply(training_type_helper)]
    workouts = workouts[workouts.apply(calorie_helper,axis=1)]

    dct = {
        'upper_body': list(workouts.loc[workouts['body_focus']=='upper_body','workout_id']),
        'lower_body': list(workouts.loc[workouts['body_focus']=='lower_body','workout_id']),
        'core': list(workouts.loc[workouts['body_focus']=='core','workout_id']),
        'total_body': list(workouts.loc[workouts['body_focus']=='total_body','workout_id'])
    }
    return dct
