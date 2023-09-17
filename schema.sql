CREATE TYPE role_type AS ENUM ('student', 'teacher');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role role_type
);

CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    subject_id INTEGER REFERENCES subjects ON DELETE CASCADE,
    question TEXT UNIQUE NOT NULL,
    answer TEXT NOT NULL,
    points INTEGER NOT NULL
); 

CREATE TABLE exams ( 
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    time_limit_minutes INTEGER NOT NULL,
    subject_id INTEGER REFERENCES subjects ON DELETE CASCADE
);

CREATE TABLE exams_questions (
    id SERIAL PRIMARY KEY,
    question_id INTEGER REFERENCES questions ON DELETE CASCADE,
    exam_id INTEGER REFERENCES exams ON DELETE CASCADE
);

CREATE TABLE users_answers (
    id SERIAL PRIMARY KEY,
    exams_question_id INTEGER REFERENCES exams_questions ON DELETE CASCADE,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    points_received INTEGER,
    answer TEXT,
    exam_finished TIMESTAMP
)