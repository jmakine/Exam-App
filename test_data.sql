INSERT INTO subjects (id, name) VALUES ('1', 'Matematiikka');
INSERT INTO subjects (id, name) VALUES ('2', 'Maantieto');

INSERT INTO questions (id, subject_id, question, answer, points) 
VALUES (
    '1',
    '1',
    'Juna ajaa nopeudella 100 km/h. Matkaa on jäljellä 50 km. Kuinka kauan kestää, että juna on saapunut määränpäähän? Syötä vastaus minuutteina, pelkkä numero.',
    '30',
    '1'
);
INSERT INTO questions (id, subject_id, question, answer, points) 
VALUES (
    '2',
    '1',
    'Matkaa on jäljellä 150 km. Millä nopeudella matkaa on taitettava, jotta määränpäähän saavutaan tasan puolessa tunnissa? Syötä vastaus nopeutena km/h, pelkkä numero.',
    '300',
    '2'
);
INSERT INTO questions (id, subject_id, question, answer, points) 
VALUES (
    '3',
    '1',
    'Auto ajaa nopeudella 80 km/h. Kuinka pitkän matkan auto etenee kahdessa ja puolessa tunnissa? Syötä vastaus kilometreinä, pelkkä numero.',
    '200',
    '1'
);

INSERT INTO questions (id, subject_id, question, answer, points) 
VALUES (
    '4',
    '2',
    'Mikä on Suomen pääkaupunki?',
    'Helsinki',
    '1'
);

INSERT INTO questions (id, subject_id, question, answer, points) 
VALUES (
    '5',
    '2',
    'Mikä on Viron pääkaupunki?',
    'Tallinna',
    '1'
);

INSERT INTO questions (id, subject_id, question, answer, points) 
VALUES (
    '6',
    '2',
    'Mikä on Etelä-Korean pääkaupunki?',
    'Soul',
    '2'
);

INSERT INTO questions (id, subject_id, question, answer, points) 
VALUES (
    '7',
    '2',
    'Mikä on Etelä-Afrikan pääkaupunki?',
    'Kapkaupunki',
    '2'
);

INSERT INTO questions (id, subject_id, question, answer, points) 
VALUES (
    '8',
    '2',
    'Mikä on Etiopian pääkaupunki?',
    'Addis Abeba',
    '3'
);

INSERT INTO exams (id, name, time_limit_minutes, subject_id) 
VALUES (
    '2',
    'Km/h laskut - 10/2023',
    10,
    '1'
);

INSERT INTO exams (id, name, time_limit_minutes, subject_id) 
VALUES (
    '1',
    'Pääkaupungit - 10/2023',
    6,
    '2'
);

INSERT INTO exams_questions (id, question_id, exam_id) 
VALUES (
    '1',
    '1',
    '1'
);

INSERT INTO exams_questions (id, question_id, exam_id) 
VALUES (
    '2',
    '2',
    '1'
);

INSERT INTO exams_questions (id, question_id, exam_id) 
VALUES (
    '3',
    '3',
    '1'
);

INSERT INTO exams_questions (id, question_id, exam_id) 
VALUES (
    '4',
    '4',
    '2'
);

INSERT INTO exams_questions (id, question_id, exam_id) 
VALUES (
    '5',
    '5',
    '2'
);

INSERT INTO exams_questions (id, question_id, exam_id) 
VALUES (
    '6',
    '6',
    '2'
);

INSERT INTO exams_questions (id, question_id, exam_id) 
VALUES (
    '7',
    '7',
    '2'
);

INSERT INTO exams_questions (id, question_id, exam_id) 
VALUES (
    '8',
    '8',
    '2'
);