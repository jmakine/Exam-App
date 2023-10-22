INSERT INTO subjects (name) VALUES ('Matematiikka');
INSERT INTO subjects (name) VALUES ('Maantieto');

INSERT INTO questions (subject_id, question, answer, points) 
VALUES (
    ( SELECT id FROM subjects WHERE name='Matematiikka' ),
    'Juna ajaa nopeudella 100 km/h. Matkaa on jäljellä 50 km. Kuinka kauan kestää, että juna on saapunut määränpäähän? Syötä vastaus minuutteina, pelkkä numero.',
    '30',
    1
);

INSERT INTO questions (subject_id, question, answer, points) 
VALUES (
    ( SELECT id FROM subjects WHERE name='Matematiikka' ),
    'Matkaa on jäljellä 150 km. Millä nopeudella matkaa on taitettava, jotta määränpäähän saavutaan tasan puolessa tunnissa? Syötä vastaus nopeutena km/h, pelkkä numero.',
    '300',
    2
);

INSERT INTO questions (subject_id, question, answer, points) 
VALUES (
    ( SELECT id FROM subjects WHERE name='Matematiikka' ),
    'Auto ajaa nopeudella 80 km/h. Kuinka pitkän matkan auto etenee kahdessa ja puolessa tunnissa? Syötä vastaus kilometreinä, pelkkä numero.',
    '200',
    1
);

INSERT INTO questions (subject_id, question, answer, points) 
VALUES (
    ( SELECT id FROM subjects WHERE name='Maantieto' ),
    'Mikä on Suomen pääkaupunki?',
    'Helsinki',
    1
);

INSERT INTO questions (subject_id, question, answer, points) 
VALUES (
    ( SELECT id FROM subjects WHERE name='Maantieto' ),
    'Mikä on Viron pääkaupunki?',
    'Tallinna',
    1
);

INSERT INTO questions (subject_id, question, answer, points) 
VALUES (
    ( SELECT id FROM subjects WHERE name='Maantieto' ),
    'Mikä on Etelä-Korean pääkaupunki?',
    'Soul',
    2
);

INSERT INTO questions (subject_id, question, answer, points) 
VALUES (
    ( SELECT id FROM subjects WHERE name='Maantieto' ),
    'Mikä on Etelä-Afrikan pääkaupunki?',
    'Kapkaupunki',
    2
);

INSERT INTO questions (subject_id, question, answer, points) 
VALUES (
    ( SELECT id FROM subjects WHERE name='Maantieto' ),
    'Mikä on Etiopian pääkaupunki?',
    'Addis Abeba',
    3
);

INSERT INTO exams (name, time_limit_minutes, subject_id) 
VALUES (
    'Km/h laskut - 10/2023',
    10,
    ( SELECT id FROM subjects WHERE name='Matematiikka' )
);

INSERT INTO exams (name, time_limit_minutes, subject_id) 
VALUES (
    'Pääkaupungit - 10/2023',
    6,
    ( SELECT id FROM subjects WHERE name='Maantieto' )
);

INSERT INTO exams_questions (question_id, exam_id) 
VALUES (
    ( SELECT id FROM questions WHERE question='Juna ajaa nopeudella 100 km/h. Matkaa on jäljellä 50 km. Kuinka kauan kestää, että juna on saapunut määränpäähän? Syötä vastaus minuutteina, pelkkä numero.' ),
    ( SELECT id FROM exams WHERE name='Km/h laskut - 10/2023')
);

INSERT INTO exams_questions (question_id, exam_id) 
VALUES (
    ( SELECT id FROM questions WHERE question='Matkaa on jäljellä 150 km. Millä nopeudella matkaa on taitettava, jotta määränpäähän saavutaan tasan puolessa tunnissa? Syötä vastaus nopeutena km/h, pelkkä numero.' ),
    ( SELECT id FROM exams WHERE name='Km/h laskut - 10/2023')
);

INSERT INTO exams_questions (question_id, exam_id) 
VALUES (
    ( SELECT id FROM questions WHERE question='Auto ajaa nopeudella 80 km/h. Kuinka pitkän matkan auto etenee kahdessa ja puolessa tunnissa? Syötä vastaus kilometreinä, pelkkä numero.' ),
    ( SELECT id FROM exams WHERE name='Km/h laskut - 10/2023')
);

INSERT INTO exams_questions (question_id, exam_id) 
VALUES (
    ( SELECT id FROM questions WHERE question='Mikä on Suomen pääkaupunki?' ),
    ( SELECT id FROM exams WHERE name='Pääkaupungit - 10/2023')
);

INSERT INTO exams_questions (question_id, exam_id) 
VALUES (
    ( SELECT id FROM questions WHERE question='Mikä on Viron pääkaupunki?' ),
    ( SELECT id FROM exams WHERE name='Pääkaupungit - 10/2023')
);

INSERT INTO exams_questions (question_id, exam_id) 
VALUES (
    ( SELECT id FROM questions WHERE question='Mikä on Etelä-Korean pääkaupunki?' ),
    ( SELECT id FROM exams WHERE name='Pääkaupungit - 10/2023')
);

INSERT INTO exams_questions (question_id, exam_id) 
VALUES (
    ( SELECT id FROM questions WHERE question='Mikä on Etelä-Afrikan pääkaupunki?' ),
    ( SELECT id FROM exams WHERE name='Pääkaupungit - 10/2023')
);

INSERT INTO exams_questions (question_id, exam_id) 
VALUES (
    ( SELECT id FROM questions WHERE question='Mikä on Etiopian pääkaupunki?' ),
    ( SELECT id FROM exams WHERE name='Pääkaupungit - 10/2023')
);
