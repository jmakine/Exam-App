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

def check_answer(users_answer, correct_answer):
    # Ignore case, remove any leading and trailing whitespace and replace . by ,
    users_answer=users_answer.lower().strip().replace('.', ',')
    correct_answer=correct_answer.lower().strip().replace('.', ',')
    if(users_answer == correct_answer):
        return True
    else:
        return False

# returns correct answer and points
def get_answer_and_points(question_id):
    sql = "SELECT answer, points from questions WHERE id=:question_id"
    result = db.session.execute(text(sql), {"question_id":question_id}).fetchone() # ).fetchone()  #, 
    return result

# question_id, exam_id, answer
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