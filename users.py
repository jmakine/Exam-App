from db import db
import secrets
from sqlalchemy.sql import text
from flask import session, request, abort
from werkzeug.security import check_password_hash, generate_password_hash

def get_users():
    sql = "SELECT id, username, role FROM users;"
    if user_role() == "teacher":
        return db.session.execute(text(sql)).fetchall()
    else:
        return False
    
def teacher_count():
    sql = "SELECT id FROM users WHERE role='teacher';"
    return len(db.session.execute(text(sql)).fetchall())

def user_count():
    sql = "SELECT id FROM users;"
    return len(db.session.execute(text(sql)).fetchall())

def get_user(id):
    sql = "SELECT id, username, role FROM users WHERE id=:id;"
    if user_role() == "teacher" or user_id() == id:
        return db.session.execute(text(sql), {"id":id}).fetchone()
    else:
        return False

def add_user(username, password, role):
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password, role) \
        VALUES (:username, :password, :role);"

    if user_role() == "teacher":
        try:
            db.session.execute(text(sql), {"username":username, "password":hash_value, "role":role})
            db.session.commit()
        except:
            return False
    else: return False

def delete_user(id):
    sql = "DELETE FROM users WHERE id=:id;"
    try:
        db.session.execute(text(sql), {"id":id})
        db.session.commit()
    except:
        return False
    
def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        if user_count() == 0:
            sql = "INSERT INTO users (username, password, role) \
                VALUES (:username, :password, 'teacher');"
            db.session.execute(text(sql), {"username":username, "password":hash_value})
            db.session.commit()
        else:
            sql = "INSERT INTO users (username, password, role) \
                VALUES (:username, :password, 'student');"
            db.session.execute(text(sql), {"username":username, "password":hash_value})
            db.session.commit()
    except:
        return False
    return login(username, password)

def username_exists(username):
    sql = "SELECT id FROM users WHERE username=:username;"
    username_exists = db.session.execute(text(sql), {"username":username}).fetchall()
    return username_exists != []

def login(username, password):
    sql = "SELECT id, password, role, username FROM users WHERE username=:username;"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user.password, password):
        return False
    else: 
        session["user_id"] = user.id
        session["role"] = user.role
        session["username"] = user.username
        session["csrf_token"] = secrets.token_hex(16)
        return True            
        
def logout():
    del session["user_id"]
    del session["role"]
    del session["username"]
    del session["csrf_token"]

def user_id():
    return session.get("user_id",0)

def user_role():
    return session.get("role",0)

def check_csrf():
    if session.get("csrf_token",0) != request.form["csrf_token"]:
        abort(403)