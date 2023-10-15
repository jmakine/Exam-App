from app import app
from flask import render_template, request, redirect, flash, get_flashed_messages
from datetime import datetime
import users
import subjects
import questions
import exams
import answers

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
            flash('Kirjautuminen onnistui!', 'success')
            return redirect("/")
        else:
            flash('Väärä käyttäjätunnus tai salasana!', 'danger')
            return redirect(request.url)

@app.route("/logout")
def logout():
    users.logout()
    flash('Olet kirjautunut ulos.', 'primary')    
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
            flash('Käyttäjänimi varattu.', 'danger')
            return redirect(request.url)
        if len(username) < 4:
            flash('Käyttäjätunnuksen on oltava vähintään 4 merkkiä pitkä.', 'danger')
            return redirect(request.url)
        if len(username) > 20:
            flash('Käyttäjätunnus ei saa olla yli 20 merkkiä pitkä.', 'danger')
            return redirect(request.url)
        if len(password1) < 8:
            flash('Salasanan on oltava vähintään 8 merkkiä pitkä.', 'danger')
            return redirect(request.url)
        if len(password1) > 20:
            flash('Salasana ei saa olla yli 20 merkkiä pitkä.', 'danger')
            return redirect(request.url)
        if password1 != password2:
            flash('Syötä sama salasana molempiin kenttiin.', 'danger')
            return redirect(request.url)
        users.register(username, password1)
        flash('Rekisteröinti onnistui! Tervetuloa!', 'success')
        return redirect("/")

@app.route("/users")
def get_users():
    if users.user_id() and users.user_role() == 'teacher':
        result = users.get_users()
        return render_template("users.html", users=result)
    else: 
        return redirect("/")
    
@app.route("/users_table")
def get_exam_stats():
    if users.user_id() and users.user_role() == 'teacher':
        stats_by_user = exams.get_exam_stats()
        return render_template("users_table.html", stats=stats_by_user)
    else: 
        return redirect("/")

@app.route("/users/add", methods=["POST"])
def add_user():
    users.check_csrf()
    if users.user_id() and users.user_role() == 'teacher':
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        if users.username_exists(username) == True:
            flash('Käyttäjänimi varattu.', 'danger')
            return redirect("/users")
        if len(username) < 4:
            flash('Käyttäjätunnuksen on oltava vähintään 4 merkkiä pitkä.', 'danger')
            return redirect("/users")
        if len(username) > 20:
            flash('Käyttäjätunnus ei saa olla yli 20 merkkiä pitkä.', 'danger')
            return redirect("/users")
        if len(password) < 8:
            flash('Salasanan on oltava vähintään 8 merkkiä pitkä.', 'danger')
            return redirect("/users")
        if len(password) > 20:
            flash('Salasana ei saa olla yli 20 merkkiä pitkä.', 'danger')
            return redirect("/users")
        else:
            users.add_user(username, password, role)
            flash('Käyttäjä lisätty.', 'success')
            return redirect("/users")
    else:
        return redirect("/")

@app.route("/users/delete", methods=["POST"])
def delete_user():
    users.check_csrf()
    id_to_delete = request.form["id_to_delete"]
    role_to_delete = users.get_user(id_to_delete)[2]

    if users.user_role() == 'teacher':        
        if users.teacher_count() > 1 and users.user_id() == int(id_to_delete):
            users.delete_user(id_to_delete)
            flash('Käyttäjätilisi on poistettu.', 'primary')
            users.logout()
            return redirect("/")
        elif users.teacher_count() > 1 or (users.teacher_count() == 1 and role_to_delete == 'student'):
            users.delete_user(id_to_delete)
            flash('Käyttäjätili poistettu.', 'success')
            return redirect("/users")
        else:
            flash('Et voi poistaa ainutta opettajaa!', 'danger')
            return redirect("/users")

    elif users.user_role() == 'student':
        if users.user_id() == int(id_to_delete):
            users.delete_user(id_to_delete)
            flash('Käyttäjätilisi on poistettu.', 'primary')
            users.logout()
            return redirect("/")

    else:
        return redirect("/")

@app.route("/subjects")
def get_subjects():
    if users.user_id() and users.user_role() == 'teacher':
        result = subjects.get_subjects()
        return render_template("subjects.html", subjects=result)
    else:
        return redirect("/")

@app.route("/subjects/add", methods=["POST"])
def add_subject():
    users.check_csrf()
    if users.user_id() and users.user_role() == 'teacher':
        name = request.form["name"]
        if subjects.subjectname_exists(name) == True:
            flash('Tämän niminen aihealue on jo olemassa.', 'danger')
            return redirect("/subjects")
        if len(name) < 5:
            flash('Aihealueen on oltava vähintään 5 merkkiä pitkä.', 'danger')
            return redirect("/subjects")
        if len(name) > 30:
            flash('Aihealue ei saa olla yli 30 merkkiä pitkä.', 'danger')
            return redirect("/subjects")
        else:
            subjects.add_subject(name)
            flash('Aihealue lisätty.', 'success')
            return redirect("/subjects")
    else:
        return redirect("/")

@app.route("/subjects/delete", methods=["POST"])
def delete_subject():
    users.check_csrf()
    if users.user_id() and users.user_role() == 'teacher':
        id = request.form["id"]
        subjects.delete_subject(id)
        flash('Aihealue poistettu.', 'primary')
        return redirect("/subjects")
    else:
        return redirect("/")
            
@app.route("/subjects/<int:subject_id>/questions")
def get_questions(subject_id):
    if users.user_id() and users.user_role() == 'teacher':
        subject = subjects.get_subject(subject_id)
        subject_questions = questions.get_questions(subject_id)
        return render_template("questions.html", questions=subject_questions, subject=subject)
    else:
        return redirect("/")

@app.route("/questions/add", methods=["POST"])
def add_question():
    users.check_csrf()
    if users.user_id() and users.user_role() == 'teacher':
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
    users.check_csrf()
    if users.user_id() and users.user_role() == 'teacher':
        path=request.form["path"]
        question_id=request.form["question_id"]
        questions.delete_question(question_id)
        return redirect(path)
    else:
        redirect("/")

@app.route("/subjects/<int:subject_id>/exams")
def get_exams(subject_id):
    if users.user_id() and users.user_role() == 'teacher':
        subject = subjects.get_subject(subject_id)
        subject_exams = exams.get_exams(subject_id)
        return render_template("exams.html", exams=subject_exams, subject=subject)
    else:
        redirect("/")

@app.route("/exams")
def get_all_exams():
    if users.user_id():
        exams_stats = answers.get_exams_stats()
        user_id = users.user_id()
        users_exams = answers.get_exams_and_points(user_id)

        users_exam_time_spent = []
        for exam in users_exams:
            users_exam_time_spent.append(exams.get_time_spent(exam.exam_id, user_id))

        started_exam_ids = []
        for exam in users_exams:
            if exam.exam_finished == None and exam.exam_started != None :
                started_exam_ids.append(exam.exam_id)
        
        submitted_exam_ids = []
        for exam in users_exams:
            if exam.exam_finished != None:
                submitted_exam_ids.append(exam.exam_id)
        
        return render_template("exams_table.html", 
                            exams_stats=exams_stats, 
                            users_exams=users_exams, 
                            submitted_exam_ids=submitted_exam_ids,
                            started_exam_ids=started_exam_ids,
                            users_exam_time_spent=users_exam_time_spent)
    else:
        redirect("/")

@app.route("/exams/add", methods=["POST"])
def add_exam():
    users.check_csrf()
    if users.user_id() and users.user_role() == 'teacher':
        path=request.form["path"]
        subject_id=request.form["subject_id"]
        name=request.form["name"]
        timelimit=request.form["timelimit"]
        if exams.examname_exists(name) == True:
            return render_template("error.html", message="Tämän niminen koe on jo olemassa")
        else:
            exams.add_exam(subject_id, name, timelimit)  
            return redirect(path)
    else:
        redirect("/")

@app.route("/exams/delete", methods=["POST"])
def delete_exam():
    users.check_csrf()
    if users.user_id() and users.user_role() == 'teacher':
        path=request.form["path"]
        exam_id=request.form["exam_id"]
        exams.delete_exam(exam_id)
        return redirect(path)
    else:
        redirect("/")

@app.route("/exams/<int:exam_id>")
def get_exam(exam_id):
    if users.user_id():
        exam=exams.get_exam(exam_id)
        max_points = exams.exams_total_points(exam_id)
        exams_questions=exams.get_exam_questions_and_answers(exam_id)

        if users.user_role() == 'teacher':
            available_questions=exams.get_available_questions(exam_id)        
            return render_template("modify_exam.html", 
                                exam=exam, 
                                exams_questions=exams_questions, 
                                available_questions=available_questions, 
                                available_questions_count=len(available_questions), 
                                questions_count=len(exams_questions), 
                                max_points=max_points.total_points)
        
        elif users.user_role() == 'student':
            user_id = users.user_id()
            exam_started = exams.start_exam(exam_id)
            exam_finished = exams.get_timestamp_finished(exam_id, user_id)
            time_spent = exams.get_time_spent(exam_id, user_id)
            
            answered_questions = answers.submitted_answers(exam_id, user_id)
            answered_question_ids = []
            for item in answered_questions:
                answered_question_ids.append(item.question_id)
            answered_question_points_received = []
            for item in answered_questions:
                answered_question_points_received.append(item.points_received)

            return render_template("perform_exam.html",
                                exam=exam, 
                                exam_finished=exam_finished,
                                exams_questions=exams_questions, 
                                questions_count=len(exams_questions), 
                                max_points=max_points.total_points,
                                exam_started=exam_started,
                                answers=answered_questions,
                                answered_question_ids=answered_question_ids,
                                answered_questions_count=len(answered_questions),
                                total_points_received=sum(answered_question_points_received),
                                user_id=user_id,
                                time_spent=time_spent)

        else:
            redirect("/")
    else:
        redirect("/")

@app.route("/exam/add_question", methods=["POST"])
def add_exam_question():
    users.check_csrf()
    if users.user_id() and users.user_role() == 'teacher':
        path=request.form["path"]
        exam_id=request.form["exam_id"]
        question=request.form["question"]
        question_id=questions.get_question_id(question)
        exams.add_question(question_id, exam_id)
        return redirect(path)
    else:
        redirect("/")

@app.route("/exam/remove_question", methods=["POST"])
def remove_exam_question():
    users.check_csrf()
    if users.user_id() and users.user_role() == 'teacher':
        path=request.form["path"]
        exam_id=request.form["exam_id"]
        question_id=request.form["question_id"]
        exams.remove_question(exam_id, question_id)
        return redirect(path)
    else:
        redirect("/")

@app.route("/exam/answer_question", methods=["POST"])
def submit_answer():
    users.check_csrf()
    if users.user_id() and users.user_role() == 'student':
        path=request.form["path"]
        exam_id=request.form["exam_id"]
        question_id=request.form["question_id"]
        answer=request.form["answer"]
        answers.answer_question(question_id, exam_id, answer)
        return redirect(path)
    else:
        redirect("/")

@app.route("/exam/submit", methods=["POST"])
def submit_exam():
    users.check_csrf()
    if users.user_id() and users.user_role() == 'student':
        user_id = users.user_id()
        path=request.form["path"]
        exam_id=request.form["exam_id"]
        total_score=request.form["total_score"]
        exam_finished = datetime.now()
        exams.end_exam(user_id, exam_id, total_score, exam_finished)
        return redirect(path)
    else:
        redirect("/")