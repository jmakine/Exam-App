DROP TABLE IF EXISTS users_answers;
DROP TABLE IF EXISTS users_exams;
DROP TABLE IF EXISTS exams_questions;
DROP TABLE IF EXISTS exams;
DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS users;
DROP TYPE IF EXISTS role_type;

CREATE TYPE role_type AS ENUM ('student', 'teacher');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(20) UNIQUE NOT NULL CHECK(LENGTH(username) >= 4),
    password TEXT NOT NULL,
    role role_type NOT NULL
);

CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL CHECK(LENGTH(name) >= 5)
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    subject_id INTEGER REFERENCES subjects ON DELETE CASCADE,
    question VARCHAR(300) UNIQUE NOT NULL,
    answer VARCHAR(20) NOT NULL,
    points INTEGER NOT NULL CHECK(points > -1 AND points < 11)
);

CREATE TABLE exams ( 
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) UNIQUE NOT NULL CHECK(LENGTH(name) > 4),
    time_limit_minutes INTEGER NOT NULL CHECK(time_limit_minutes > 0 AND time_limit_minutes < 481),
    subject_id INTEGER REFERENCES subjects ON DELETE CASCADE
);

CREATE TABLE exams_questions (
    id SERIAL PRIMARY KEY,
    question_id INTEGER REFERENCES questions ON DELETE CASCADE,
    exam_id INTEGER REFERENCES exams ON DELETE CASCADE
);

CREATE TABLE users_exams (
    id SERIAL PRIMARY KEY,
    exam_id INTEGER REFERENCES exams ON DELETE CASCADE,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    exam_started TIMESTAMP,
    exam_finished TIMESTAMP,
    time_spent INTEGER[],
    total_score INTEGER
);

CREATE TABLE users_answers (
    id SERIAL PRIMARY KEY,
    exams_question_id INTEGER REFERENCES exams_questions ON DELETE CASCADE,
    user_exam_id INTEGER REFERENCES users_exams ON DELETE CASCADE,
    points_received INTEGER,
    answer VARCHAR(20)
);