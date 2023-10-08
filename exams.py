from db import db
from sqlalchemy.sql import text
import users

def get_exams(subject_id):
    sql = "SELECT subject_exams.subject_id, subject_exams.subject_name, subject_exams.exam_id, subject_exams.exam_name, subject_exams.time_limit_minutes, exam_summary.total_questions, exam_summary.max_points \
            FROM (SELECT s.id as subject_id, s.name as subject_name, e.id as exam_id, e.name as exam_name, e.time_limit_minutes \
                FROM exams e, subjects s WHERE e.subject_id=:subject_id AND s.id=:subject_id) as subject_exams \
            INNER JOIN (SELECT e.id as exam_id, COUNT(eq.question_id) as total_questions, SUM(q.points) as max_points FROM exams e \
                LEFT JOIN exams_questions eq ON e.id=eq.exam_id \
                    LEFT JOIN questions q ON q.id=eq.question_id GROUP BY e.id) as exam_summary \
            ON subject_exams.exam_id=exam_summary.exam_id;"
    return db.session.execute(text(sql), {"subject_id":subject_id}).fetchall()

def get_exam(exam_id):
    sql = "SELECT e.subject_id, e.id as exam_id, e.name, e.time_limit_minutes \
        FROM exams e WHERE e.id=:exam_id;"
    return db.session.execute(text(sql), {"exam_id":exam_id}).fetchone()

def count_exams(subject_id):
    return len(get_exams(subject_id))

def add_exam(subject_id, name, timelimit):
    try:
        sql = "INSERT INTO exams (subject_id, name, time_limit_minutes) \
            VALUES (:subject_id, :name, :timelimit);"
        db.session.execute(text(sql), {"subject_id":subject_id, "name":name, "timelimit":timelimit})
        db.session.commit()
    except:
        return False

def examname_exists(name):
    sql = "SELECT id FROM exams WHERE name=:name;"
    examname_exists = db.session.execute(text(sql), {"name":name}).fetchall()
    return examname_exists != []

def delete_exam(id):
    try:
        sql = "DELETE FROM exams WHERE id=:id;"
        db.session.execute(text(sql), {"id":id})
        db.session.commit()
    except:
        return False

def get_exam_questions_and_answers(exam_id):
    sql = "SELECT e.subject_id, e.id as exam_id, e.name as exam_name, e.time_limit_minutes, eq.question_id, q.question, q.answer, q.points \
        FROM exams e LEFT JOIN exams_questions eq ON e.id=eq.exam_id \
        LEFT JOIN questions q ON q.id=eq.question_id \
        WHERE e.id=:exam_id;"
    return db.session.execute(text(sql), {"exam_id":exam_id}).fetchall()

def exams_total_points(exam_id):
    sql = "SELECT e.id as exam_id, SUM(q.points) as total_points \
        FROM exams e LEFT JOIN exams_questions eq ON e.id=eq.exam_id \
        LEFT JOIN questions q ON q.id=eq.question_id \
        WHERE e.id=:exam_id \
        GROUP BY e.id;"
    return db.session.execute(text(sql), {"exam_id":exam_id}).fetchone()

def get_available_questions(exam_id):
    exam = get_exam(exam_id)
    exam_subject = exam.subject_id
    sql = "SELECT DISTINCT(question_id), subject_id, question, answer, points FROM \
        (SELECT q.id as question_id, q.subject_id, q.question, q.answer, q.points FROM questions q \
            LEFT JOIN exams_questions eq ON q.id=eq.question_id \
                WHERE q.subject_id=:subject_id AND (eq.exam_id<>:exam_id OR eq.exam_id IS NULL)) as possible_questions \
        WHERE NOT EXISTS \
            (SELECT q.id as question_id FROM questions q \
                LEFT JOIN exams_questions eq ON q.id=eq.question_id \
                    WHERE q.subject_id=:subject_id AND (eq.exam_id=:exam_id) AND q.id=possible_questions.question_id);"
    return db.session.execute(text(sql), {"exam_id":exam_id, "subject_id":exam_subject}).fetchall()

def add_question(question_id, exam_id):
    try:
        sql = "INSERT INTO exams_questions (exam_id, question_id) \
            VALUES (:exam_id, :question_id);"
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

def get_exam_stats():
    try:
        sql = "SELECT u.id as user_id, u.username, s.name as subject_name, e.id as exam_id, e.name as exam_name, exams_total_points.total_points as max_points, TO_CHAR(ue.exam_finished, 'YYYY/MM/DD HH24:MM:SS') as exam_finished, ue.total_score as points_received, ue.time_spent \
            FROM users u LEFT JOIN users_exams ue ON ue.user_id=u.id \
                LEFT JOIN exams e ON e.id=ue.exam_id \
                    INNER JOIN subjects s ON s.id=e.subject_id \
                        LEFT JOIN (SELECT e.id as exam_id, SUM(q.points) as total_points \
                            FROM exams e LEFT JOIN exams_questions eq ON e.id=eq.exam_id \
                                LEFT JOIN questions q ON q.id=eq.question_id GROUP BY e.id) as exams_total_points \
                                    ON exams_total_points.exam_id=e.id;"
        return db.session.execute(text(sql)).fetchall()
    except:
        return False

def get_timestamp_started(exam_id, user_id):
    sql = "SELECT exam_started from users_exams \
        WHERE (user_id, exam_id) = (:user_id, :exam_id);"
    exam_started = db.session.execute(text(sql), {"exam_id":exam_id, "user_id":user_id}).fetchone()
    exam_started = exam_started[0].strftime("%c")
    return exam_started

def start_exam(exam_id):
    user_id = users.user_id()
    try:
        sql = "INSERT INTO users_exams (user_id, exam_id, exam_started) \
            SELECT :user_id, :exam_id, current_timestamp \
            WHERE NOT EXISTS ( \
                SELECT 1 FROM users_exams WHERE (user_id, exam_id) = (:user_id, :exam_id));"
        db.session.execute(text(sql), {"exam_id":exam_id, "user_id":user_id})
        db.session.commit()
        exam_started = get_timestamp_started(exam_id, user_id)
        return exam_started
    except:
        return False

def get_timestamp_finished(exam_id, user_id):
    sql = "SELECT exam_finished from users_exams \
        WHERE (user_id, exam_id) = (:user_id, :exam_id);"
    exam_finished = db.session.execute(text(sql), {"exam_id":exam_id, "user_id":user_id}).fetchone()
    exam_finished = exam_finished[0]
    if exam_finished != None:
        exam_finished = exam_finished.strftime("%c")
    return exam_finished

def get_time_spent(exam_id, user_id):
    sql_started = "SELECT exam_started from users_exams \
        WHERE (user_id, exam_id) = (:user_id, :exam_id);"
    exam_started = db.session.execute(text(sql_started), {"exam_id":exam_id, "user_id":user_id}).fetchone()
    exam_started = exam_started[0]

    sql_finished = "SELECT exam_finished from users_exams \
        WHERE (user_id, exam_id) = (:user_id, :exam_id);"
    exam_finished = db.session.execute(text(sql_finished), {"exam_id":exam_id, "user_id":user_id}).fetchone()
    exam_finished = exam_finished[0]
    time_spent = 0
    if exam_finished != None:
        time_spent = exam_finished - exam_started
        seconds_in_day = 24*60*60
        time_spent = divmod(time_spent.days * seconds_in_day + time_spent.seconds, 60)
    return time_spent

def end_exam(user_id, exam_id, total_score, exam_finished):
    try:
        sql_end = "UPDATE users_exams \
            SET exam_finished = (CASE WHEN b.count=0 THEN current_timestamp ELSE exam_finished END), \
                total_score = (CASE WHEN b.count=0 THEN :total_score ELSE total_score END) \
            FROM (SELECT COUNT(*) as count FROM users_exams WHERE exam_id=:exam_id AND user_id=:user_id AND exam_finished IS NOT NULL) b \
            WHERE user_id=:user_id AND exam_id=:exam_id;"
        db.session.execute(text(sql_end), {"exam_id":exam_id, "user_id":user_id, "total_score":total_score, "exam_finished":exam_finished})
        db.session.commit()
    
        try:
            time_spent = get_time_spent(exam_id, user_id)
            print('time_spent in exams.py end_exam: ', type(list(time_spent)), list(time_spent))
            time_spent = list(time_spent)
            sql_add_time_spent = "UPDATE users_exams \
                SET time_spent=:time_spent \
                WHERE user_id=:user_id AND exam_id=:exam_id;"
            db.session.execute(text(sql_add_time_spent), {"exam_id":exam_id, "user_id":user_id, "time_spent":time_spent})
            db.session.commit()
        except:
            return False
    except:
        return False
    