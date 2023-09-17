from app import app
from flask import render_template, request, redirect
import users
import subjects
import questions
import exams

@app.route("/")
def index():
    user_id = users.user_id()
    loggeduser = users.get_user(int(user_id))
    return render_template("index.html", user=loggeduser)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if users.username_exists(username) == True:
            return render_template("error.html", message="Käyttäjänimi varattu")
        if password1 != password2:
            return render_template("error.html", message="Syötä sama salasana molempiin kenttiin")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti epäonnistui")

@app.route("/users", methods=["GET"])
def get_users():
    if users.user_role() == 'teacher':
        result = users.get_users()
        return render_template("users.html", users=result)
    else: 
        return redirect("/")

@app.route("/users/add", methods=["POST"])
def add_user():
    if users.user_role() == 'teacher':
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        if users.username_exists(username) == True:
            return render_template("error.html", message="Käyttäjänimi varattu")
        else:
            users.add_user(username, password, role)    
            return redirect("/users")
    else:
        return redirect("/")

@app.route("/users/delete", methods=["POST"])
def delete_user():
    if users.user_role() == 'teacher':
        id = request.form["id"]
        if users.teacher_count() > 1:
            users.delete_user(int(id))
            return redirect("/users")
        else:
            return render_template("error.html", message="Et voi poistaa ainutta opettajaa")
    else:
        return redirect("/")

@app.route("/subjects", methods=["GET"])
def get_subjects():
    result = subjects.get_subjects()
    return render_template("subjects.html", subjects=result)

@app.route("/subjects/add", methods=["POST"])
def add_subject():
    if users.user_role() == 'teacher':
        name = request.form["name"]
        if subjects.subjectname_exists(name) == True:
            return render_template("error.html", message="Aihealue luotu jo")
        else:
            subjects.add_subject(name)    
            return redirect("/subjects")
    else:
        return redirect("/subjects")

@app.route("/subjects/delete", methods=["POST"])
def delete_subject():
    if users.user_role() == 'teacher':
        id = request.form["id"]
        subjects.delete_subject(int(id))
    return redirect("/subjects")
            
@app.route("/subjects/<int:subject_id>/questions")
def get_questions(subject_id):
    if users.user_role() == 'teacher':
        subject = subjects.get_subject(subject_id)
        subject_questions = questions.get_questions(subject_id)
        return render_template("questions.html", questions=subject_questions, subject=subject)
    else:
        return redirect("/subjects/<int:subject_id>")

@app.route("/questions/add", methods=["POST"])
def add_question():
    if users.user_role() == 'teacher':
        path=request.form["path"]
        subject_id=request.form["subject_id"]
        question=request.form["question"]
        answer=request.form["answer"],
        points=request.form["points"]
        questions.add_question(subject_id, question, answer, points)
        return redirect(path)
    else:
        redirect("/")

@app.route("/questions/delete", methods=["POST"])
def delete_question():
    if users.user_role() == 'teacher':
        path=request.form["path"]
        question_id=request.form["question_id"]
        questions.delete_question(question_id)
        return redirect(path)
    else:
        redirect("/")

@app.route("/subjects/<int:subject_id>/exams")
def get_exams(subject_id):
    subject = subjects.get_subject(subject_id)
    subject_exams = exams.get_exams(subject_id)
    return render_template("exams.html", subject=subject, exams=subject_exams)

@app.route("/exams/add", methods=["POST"])
def add_exam():
    if users.user_role() == 'teacher':
        path=request.form["path"]
        subject_id=request.form["subject_id"]
        name=request.form["name"]
        timelimit=request.form["timelimit"]
        if exams.examname_exists(name) == True:
            return render_template("error.html", message="Tämän niminen koe luotu jo, syötä uniikki nimi")
        else:
            exams.add_exam(subject_id, name, timelimit)  
            return redirect(path)
    else:
        redirect("/")

@app.route("/exams/delete", methods=["POST"])
def delete_exam():
    if users.user_role() == 'teacher':
        path=request.form["path"]
        exam_id=request.form["exam_id"]
        exams.delete_exam(exam_id)
        return redirect(path)
    else:
        redirect("/")

@app.route("/exams/<int:exam_id>")
def get_exam(exam_id):
    exam=exams.get_exam(exam_id)
    total_points = exams.exams_total_points(exam_id)
    exams_questions=exams.get_exam_questions_and_answers(exam_id)

    if users.user_role() == 'teacher':
        available_questions=exams.get_available_questions(exam_id)        
        return render_template("modify_exam.html", 
                            exam=exam, 
                            exams_questions=exams_questions, 
                            available_questions=available_questions, 
                            questions_count=len(exams_questions), 
                            total_points=total_points)
    else:
        return render_template("perform_exam.html",
                            exam=exam, 
                            exams_questions=exams_questions, 
                            questions_count=len(exams_questions), 
                            total_points=total_points)

@app.route("/exam/add_question", methods=["POST"])
def add_exam_question():
    if users.user_role() == 'teacher':
        path=request.form["path"]
        exam_id=request.form["exam_id"]
        question_id=request.form["question_id"]
        exams.add_question(question_id, exam_id)
        return redirect(path)
    else:
        redirect("/")

@app.route("/exam/remove_question", methods=["POST"])
def remove_exam_question():
    if users.user_role() == 'teacher':
        path=request.form["path"]
        exam_id=request.form["exam_id"]
        question_id=request.form["question_id"]
        exams.remove_question(exam_id, question_id)
        return redirect(path)
    else:
        redirect("/")

@app.route("/exam/answer_question", methods=["POST"])
def add_users_answer():
    return ''

@app.route("/exam/submit", methods=["POST"])
def submit_users_exam():
    return ''