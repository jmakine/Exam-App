from db import db
from sqlalchemy.sql import text

def get_questions(subject_id):
    sql = "SELECT s.id, s.name, q.id, q.subject_id, q.question, q.answer, q.points \
            FROM questions q, subjects s \
                WHERE q.subject_id=:id AND s.id=:id"
    return db.session.execute(text(sql), {"id":subject_id}).fetchall()

def get_question_id(question):
    sql = "SELECT id FROM questions WHERE question=:question"
    response = db.session.execute(text(sql), {"question":question}).fetchone()
    if response != None:
        return response[0]
    else:
        return None

def count_questions(subject_id):
    return len(get_questions(subject_id))

def add_question(subject_id, question, answer, points):
    try:
        sql = "INSERT INTO questions (subject_id, question, answer, points) \
            VALUES (:subject_id, :question, :answer, :points)"
        db.session.execute(text(sql), 
                           {"subject_id":subject_id, 
                            "question":question, 
                            "answer":answer, 
                            "points":points})
        db.session.commit()
    except:
        return False

def delete_question(id):
    remove_associations = "DELETE FROM exams_questions WHERE question_id=:id"
    db.session.execute(text(remove_associations), {"id":id})
    db.session.commit()

    sql = "DELETE FROM questions WHERE id=:id"
    db.session.execute(text(sql), {"id":id})
    db.session.commit()