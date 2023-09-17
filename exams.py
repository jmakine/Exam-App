from db import db
from sqlalchemy.sql import text

def get_exams(subject_id):
    sql = "SELECT subject_exams.subject_id, subject_exams.subject_name, subject_exams.exam_id, subject_exams.exam_name, subject_exams.time_limit_minutes, exam_summary.total_questions, exam_summary.max_points \
            FROM (SELECT s.id as subject_id, s.name as subject_name, e.id as exam_id, e.name as exam_name, e.time_limit_minutes \
                FROM exams e, subjects s WHERE e.subject_id=:subject_id AND s.id=:subject_id) as subject_exams \
            INNER JOIN (SELECT e.id as exam_id, COUNT(eq.question_id) as total_questions, SUM(q.points) as max_points FROM exams e \
                LEFT JOIN exams_questions eq ON e.id=eq.exam_id \
                    LEFT JOIN questions q ON q.id=eq.question_id GROUP BY e.id) as exam_summary \
            ON subject_exams.exam_id=exam_summary.exam_id"
    return db.session.execute(text(sql), {"subject_id":subject_id}).fetchall()

# SELECT first_set.subject_id, first_set.subject_name, first_set.exam_id, first_set.exam_name, first_set.time_limit_minutes, second_set.total_questions, second_set.max_points FROM (SELECT s.id as subject_id, s.name as subject_name, e.id as exam_id, e.name as exam_name, e.time_limit_minutes FROM exams e, subjects s WHERE e.subject_id=1 AND s.id=1) as first_set INNER JOIN (SELECT e.id as exam_id, COUNT(eq.question_id) as total_questions, SUM(q.points) as max_points FROM exams e LEFT JOIN exams_questions eq ON e.id=eq.exam_id LEFT JOIN questions q ON q.id=eq.question_id GROUP BY e.id) as second_set ON first_set.exam_id=second_set.exam_id;

def get_exam(exam_id):
    sql = "SELECT e.subject_id, e.id as exam_id, e.name, e.time_limit_minutes \
        FROM exams e WHERE e.id=:exam_id"
    return db.session.execute(text(sql), {"exam_id":exam_id}).fetchone()

def count_exams(subject_id):
    return len(get_exams(subject_id))

def add_exam(subject_id, name, timelimit):
    try:
        sql = "INSERT INTO exams (subject_id, name, time_limit_minutes) \
            VALUES (:subject_id, :name, :timelimit)"
        db.session.execute(text(sql), {"subject_id":subject_id, "name":name, "timelimit":timelimit})
        db.session.commit()
    except:
        return False

def examname_exists(name):
    sql = "SELECT COUNT(name) FROM exams WHERE name=:name GROUP by name"
    examname_exists = db.session.execute(text(sql), {"name":name}).fetchall()
    return examname_exists != []

def delete_exam(id):
    try:
        sql = "DELETE FROM exams WHERE id=:id"
        db.session.execute(text(sql), {"id":id})
        db.session.commit()
    except:
        return False

def get_exam_questions_and_answers(exam_id):
    sql = "SELECT e.subject_id, e.id as exam_id, e.name as exam_name, e.time_limit_minutes, eq.question_id, q.question, q.answer, q.points \
        FROM exams e LEFT JOIN exams_questions eq ON e.id=eq.exam_id \
        LEFT JOIN questions q ON q.id=eq.question_id \
        WHERE e.id=:exam_id"
    return db.session.execute(text(sql), {"exam_id":exam_id}).fetchall()

def exams_total_points(exam_id):
    sql = "SELECT e.id as exam_id, SUM(q.points) as total_points \
        FROM exams e LEFT JOIN exams_questions eq ON e.id=eq.exam_id \
        LEFT JOIN questions q ON q.id=eq.question_id \
        WHERE e.id=:exam_id \
        GROUP BY e.id"
    return db.session.execute(text(sql), {"exam_id":exam_id}).fetchone()

def get_available_questions(exam_id):
    exam = get_exam(exam_id)
    exam_subject = exam.subject_id
    sql = "SELECT * FROM \
        (SELECT q.id as question_id, q.subject_id, q.question, q.answer, q.points FROM questions q \
            LEFT JOIN exams_questions eq ON q.id=eq.question_id \
                WHERE q.subject_id=:subject_id AND (eq.exam_id<>:exam_id OR eq.exam_id IS NULL)) as possible_questions \
        WHERE NOT EXISTS \
            (SELECT q.id as question_id FROM questions q \
                LEFT JOIN exams_questions eq ON q.id=eq.question_id \
                    WHERE q.subject_id=:subject_id AND (eq.exam_id=:exam_id) AND q.id=possible_questions.question_id)"
    return db.session.execute(text(sql), {"exam_id":exam_id, "subject_id":exam_subject}).fetchall()

def add_question(question_id, exam_id):
    try:
        sql = "INSERT INTO exams_questions (exam_id, question_id) \
            VALUES (:exam_id, :question_id)"
        db.session.execute(text(sql), {"exam_id":exam_id, "question_id":question_id})
        db.session.commit()
    except:
        return False

def remove_question(exam_id, question_id):
    try:
        sql = "DELETE FROM exams_questions eq\
            WHERE eq.exam_id=:exam_id AND eq.question_id=:question_id"
        db.session.execute(text(sql), {"exam_id":exam_id, "question_id":question_id})
        db.session.commit()
    except:
        return False