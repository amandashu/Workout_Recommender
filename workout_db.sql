CREATE DATABASE IF NOT EXISTS workout;


DROP TABLE IF EXISTS users;

-- create users table
CREATE TABLE IF NOT EXISTS users
(
    user_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(100),
    equipment VARCHAR(300),
    training_type VARCHAR(300),
    min_duration INT,
    max_duration INT,
    min_calories INT,
    max_calories INT,
    min_difficulty INT,
    max_difficulty INT,
    -- binary variables for training type
    balance_agility INT,
     barre INT,
     cardiovascular INT,
     hiit INT,
     low_impact INT,
     pilates INT,
     plyometric INT,
     strength_training INT,
     stretching_flexibility INT,
     toning INT,
     warm_up_cool_down INT,
     aerobics_step INT,
     -- binary variables for equipment
     barbell INT,
     bench INT,
     dumbbell INT,
     exercise_band INT,
     jump_rope INT,
     kettlebell INT,
     mat INT,
     medicine_ball INT,
     physioball INT,
     sandbag INT,
     stationary_bike INT
);


-- manually upload fb_workouts.csv into table fbworkouts_meta with the following datatypes
--      workout_id INT PRIMARY KEY,
--      workout_title TEXT,
--      fb_link TEXT,
--      youtube_link TEXT,
--      equipment VARCHAR(100),
--      training_type VARCHAR(100),
--      body_focus VARCHAR(100)

-- manually upload fb_workouts.csv into table fbworkouts with the following datatypes
--      workout_id INT FOREIGN KEY REFERENCES fbworkouts_meta(workout_id),
--      duration INT,
--      min_calorie_burn INT,
--      max_calorie_burn INT,
--      difficulty INT,
--      equipment VARCHAR(300),
--      training_type VARCHAR(300),
--      body_focus VARCHAR(300),
--      core INT,
--      lower_body INT,
--      total_body INT,
--      upper_body INT,
--      balance_agility INT,
--      barre INT,
--      cardiovascular INT,
--      hiit INT,
--      low_impact INT,
--      pilates INT,
--      plyometric TINT,
--      strength_training INT,
--      stretching_flexibility INT,
--      toning INT,
--      warm_up_cool_down INT,
--      aerobics_step INT,
--      barbell INT,
--      bench INT,
--      dumbbell INT,
--      exercise_band INT,
--      jump_rope INT,
--      kettlebell TINT,
--      mat INT,
--      medicine_ball INT,
--      no_equipment INT,
--      physioball INT,
--      sandbag INT,
--      stationary_bike INT

-- manually upload user_items_interactions.csv (users with less than 5 interactions dropped)
--      user_id INT
--      workout_id INT,
