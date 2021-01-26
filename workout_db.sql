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
    max_calories INT
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
--      core INT,
--      lowerbody INT,
--      totalbody INT,
--      upperbody INT,
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


