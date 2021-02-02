def register_user(form, user_id, hashed_password):
    """
    Takes wtforms object, user_id, hashed_password, and returns arguments
    to execute query (query string, tuple of variables)
    """
    # dictionary with equipment_training_types as values and 0 or 1 for user's preference
    equipment_training_types = ['balance_agility', 'barre', 'cardiovascular', 'hiit',
    'low_impact', 'pilates', 'plyometric', 'strength_training', 'stretching_flexibility',
     'toning', 'warm_up_cool_down', 'aerobics_step', 'barbell', 'bench',
     'dumbbell', 'exercise_band', 'jump_rope', 'kettlebell', 'mat', 'medicine_ball',
     'physioball', 'sandbag', 'stationary_bike']
    dct = {}
    for v in equipment_training_types:
        dct[v] = 0

    # insert string of available equipment and update dct, else empty string
    if form.no_equipment.data == False:
        equipment_string = str(form.equipment.data)[
            1:-1].replace('\'', '')
        for e in form.equipment.data:
            dct[e] = 1
    else:
        equipment_string = ''

    # insert string of preferred training types, else have all types
    if form.no_training_type.data == False:
        training_type_string = str(form.training_type.data)[
            1:-1].replace('\'', '')

        for x in form.training_type.data:
            dct[x] = 1
    else:
        training_type_string = str([x[0] for x in form.training_type.choices])[
            1:-1].replace('\'', '')

        for x in form.training_type.choices:
            dct[x[0]] = 1

    # string of column names
    cols = ['user_id', 'name', 'email', 'password', 'equipment',
            'training_type', 'min_duration', 'max_duration', 'min_calories',
            'max_calories', 'min_difficulty', 'max_difficulty']
    cols += equipment_training_types
    cols_string = ', '.join(cols)

    # values string
    values = ('%s,'*len(cols))[:-1]

    # insert string
    insert  = 'INSERT INTO users(' + cols_string +') VALUES(' + values + ')'

    # tuples of values to insert
    equipment_training_types_tup = tuple([dct[v] for v in dct.keys()])

    # print(len(equipment_training_types_tup))
    tup = (user_id, form.name.data, form.email.data, hashed_password,
             equipment_string, training_type_string, form.min_duration.data,
             form.max_duration.data, form.min_calories.data,
             form.max_calories.data, form.min_difficulty.data,
              form.max_difficulty.data, *equipment_training_types_tup)
    return insert, tup
