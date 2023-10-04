from db import db
from sqlalchemy.sql import text
import users

def get_user_exam_id(user_id, exam_id):
    sql = "SELECT id as user_exam_id from users_exams ue \
        WHERE ue.exam_id=:exam_id AND ue.user_id=:user_id"
    user_exam_id = db.session.execute(text(sql), {"exam_id":exam_id, "user_id":user_id}).fetchone()
    return user_exam_id.user_exam_id

def get_exam_question_id(question_id, exam_id):
    sql = "SELECT id as exam_question_id from exams_questions eq \
        WHERE eq.exam_id=:exam_id AND eq.question_id=:question_id"
    exam_question_id = db.session.execute(text(sql), {"exam_id":exam_id, "question_id":question_id}).fetchone()
    return exam_question_id.exam_question_id

# Ignore case, remove any leading and trailing whitespace and replace . by ,
def check_answer(users_answer, correct_answer):
    users_answer=users_answer.lower().strip().replace('.', ',')
    correct_answer=correct_answer.lower().strip().replace('.', ',')
    if(users_answer == correct_answer):
        return True
    else:
        return False

def get_answer_and_points(question_id):
    sql = "SELECT answer, points from questions WHERE id=:question_id"
    result = db.session.execute(text(sql), {"question_id":question_id}).fetchone() 
    return result

def answer_question(question_id, exam_id, answer):
    user_id = users.user_id()
    user_exam_id = get_user_exam_id(user_id, exam_id)
    exam_question_id = get_exam_question_id(question_id, exam_id)
    correct_answer = get_answer_and_points(question_id).answer
    points = 0
    if(check_answer(answer, correct_answer)):
        points = get_answer_and_points(question_id).points

    try:
        sql = "INSERT INTO users_answers (exams_question_id, user_exam_id, points_received, answer) \
            SELECT :exams_question_id, :user_exam_id, :points_received, :answer \
            WHERE NOT EXISTS ( \
                SELECT 1 FROM users_answers WHERE (exams_question_id, user_exam_id) = (:exams_question_id, :user_exam_id) \
            )"
        db.session.execute(text(sql), 
                           {"exams_question_id":exam_question_id, 
                            "user_exam_id":user_exam_id, 
                            "answer":answer, 
                            "points_received":points})
        db.session.commit()
        return correct_answer, points, answer
    except:
        return False

def submitted_answers(exam_id, user_id):
    sql = "SELECT q.points, q.answer as correct_answer, eq.question_id, ua.points_received, ua.answer as users_answer, q.question FROM users_answers ua \
        LEFT JOIN exams_questions eq on eq.id=ua.exams_question_id \
        LEFT JOIN questions q on q.id=eq.question_id \
        LEFT JOIN users_exams ue on ua.user_exam_id=ue.id \
        WHERE eq.exam_id=:exam_id AND ue.user_id=:user_id"
    return db.session.execute(text(sql), {"exam_id":exam_id, "user_id":user_id}).fetchall()

def get_exams_and_points(user_id):
    sql = "SELECT exam_id, user_id, TO_CHAR(exam_finished, 'YYYY/MM/DD HH24:MM:SS') as exam_finished, TO_CHAR(exam_started, 'YYYY/MM/DD HH24:MM:SS') as exam_started, total_score as points_received \
        FROM users_exams WHERE user_id=:user_id;"
    return db.session.execute(text(sql), {"user_id":user_id}).fetchall()

def get_all_exams_and_points():
    sql = "SELECT users_summary.users_count, users_summary.total_score, users_summary.average_score, subject_exams.subject_id, subject_exams.subject_name, subject_exams.exam_id, subject_exams.exam_name, subject_exams.time_limit_minutes, exam_summary.total_questions, exam_summary.max_points \
        FROM (SELECT s.id as subject_id, s.name as subject_name, e.id as exam_id, e.name as exam_name, e.time_limit_minutes \
            FROM exams e, subjects s \
            WHERE e.subject_id=s.id) as subject_exams \
                INNER JOIN (SELECT e.id as exam_id, COUNT(eq.question_id) as total_questions, SUM(q.points) as max_points \
                    FROM exams e \
                        LEFT JOIN exams_questions eq ON e.id=eq.exam_id LEFT JOIN questions q ON q.id=eq.question_id GROUP BY e.id) as exam_summary ON subject_exams.exam_id=exam_summary.exam_id \
        LEFT JOIN ( \
            SELECT exam_id, COUNT(user_id) as users_count, SUM(total_score) as total_score, round((SUM(total_score)*1.0/COUNT(user_id)*1.0),1) as average_score \
            FROM users_exams GROUP BY exam_id HAVING SUM(total_score) IS NOT NULL) as users_summary \
        ON users_summary.exam_id=subject_exams.exam_id"
    result = db.session.execute(text(sql)).fetchall()
    return result