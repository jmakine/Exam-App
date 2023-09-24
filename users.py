from db import db
from sqlalchemy.sql import text
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def get_users():
    sql = "SELECT * FROM users;"
    if user_role() == "teacher":
        return db.session.execute(text(sql)).fetchall()
    else:
        return False
    
def teacher_count():
    sql = "SELECT * FROM users WHERE role='teacher';"
    return len(db.session.execute(text(sql)).fetchall())

def user_count():
    sql = "SELECT count(id) FROM users GROUP BY id;"
    return len(db.session.execute(text(sql)).fetchall())

def get_user(id):
    sql = "SELECT * FROM users WHERE id=:id;"
    if user_role() == "teacher" or user_id() == id:
        return db.session.execute(text(sql), {"id":id}).fetchone()
    else:
        return False

def add_user(username, password, role):
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password, role) VALUES (:username, :password, :role)"

    if user_role() == "teacher":
        try:
            db.session.execute(text(sql), {"username":username, "password":hash_value, "role":role})
            db.session.commit()
        except:
            return False
    else: return False

def delete_user(id):
    sql = "DELETE FROM users WHERE id=:id"
    if user_role() == "teacher":
        try:
            db.session.execute(text(sql), {"id":id})
            db.session.commit()
        except:
            return False
    else:
        return False
    
def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        if user_count() == 0:
            sql = "INSERT INTO users (username, password, role) VALUES (:username, :password, 'teacher')"
            db.session.execute(text(sql), {"username":username, "password":hash_value})
            db.session.commit()
        else:
            sql = "INSERT INTO users (username, password, role) VALUES (:username, :password, 'student')"
            db.session.execute(text(sql), {"username":username, "password":hash_value})
            db.session.commit()
    except:
        return False
    return login(username, password)

def username_exists(username):
    sql = "SELECT COUNT(username) FROM users WHERE username=:username GROUP by username"
    username_exists = db.session.execute(text(sql), {"username":username}).fetchall()
    return username_exists != []

def login(username, password):
    sql = "SELECT id, password, role, username FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["role"] = user.role
            session["username"] = user.username
            return True
        else:
            return False
        
def logout():
    del session["user_id"]
    del session["role"]
    del session["username"]

def user_id():
    return session.get("user_id",0)

def user_role():
    return session.get("role",0)