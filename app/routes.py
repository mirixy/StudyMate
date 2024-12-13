from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from app.models import ToDo, User, Grade
from app.forms import ToDoForm
from flask_wtf.csrf import generate_csrf

main = Blueprint("main", __name__)

import random

from datetime import datetime, timedelta

@main.route("/")
@login_required
def home():
    quotes = [
        "Life is like riding a bicycle. To keep your balance, you must keep moving.",
        "Imagination is more important than knowledge.",
        "A person who never made a mistake never tried anything new.",
        "The important thing is not to stop questioning. Curiosity has its own reason for existence.",
        "Strive not to be a success, but rather to be of value."
    ]
    current_date = datetime.now().strftime("%B %d, %Y")
    quote = random.choice(quotes)

    # Get today's date
    today = datetime.now().date()
    tomorror = today + timedelta(days=1)
    # Get the date for one week from today
    next_week = tomorror + timedelta(days=7)

    # Fetch tasks for today
    today_tasks = ToDo.query.filter(
        ToDo.user_id == current_user.id,
        ToDo.deadline >= today,  # Check if the deadline is today or later
        ToDo.deadline < today + timedelta(days=1)  # Ensure it's only today's tasks
    ).all()

    # Fetch upcoming tasks
    upcoming_tasks = ToDo.query.filter(
        ToDo.user_id == current_user.id,
        ToDo.deadline > tomorror,
        ToDo.deadline <= next_week
    ).order_by(ToDo.deadline).all()

    return render_template("index.html", current_date=current_date, quote=quote, today_tasks=today_tasks, upcoming_tasks=upcoming_tasks)

@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if User.query.filter_by(username=username).first():
            flash("Benutzername existiert bereits.")
            return redirect(url_for("main.register"))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registrierung erfolgreich. Bitte loggen Sie sich ein.")
        return redirect(url_for("main.login"))

    return render_template("register.html")

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("main.home"))
        else:
            flash("Ungültiger Benutzername oder Passwort.")
    return render_template("login.html")

@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Erfolgreich ausgeloggt.")
    return redirect(url_for("main.login"))

@main.route("/protected")
@login_required
def protected():
    return render_template("protected.html", username=current_user.username)

@main.route('/todos')
@login_required
def todos():
    tasks = ToDo.query.filter_by(user_id=current_user.id).order_by(ToDo.created_at.desc()).all()
    return render_template('todos.html', tasks=tasks)

@main.route('/todos/add', methods=['GET', 'POST'])
@login_required
def add_todo():
    form = ToDoForm()
    if form.validate_on_submit():
        new_task = ToDo(
            title=form.title.data,
            description=form.description.data,
            user_id=current_user.id,
            deadline=form.deadline.data  # Include the deadline
        )
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('main.todos'))
    return render_template('add_todo.html', form=form)

@main.route('/grades', methods=['GET', 'POST'])
@login_required
def grades():
    if request.method == 'POST':
        if 'subject' in request.form and 'q1' in request.form:
            subject = request.form.get('subject')
            q1 = int(request.form.get('q1'))
            q2 = int(request.form.get('q2'))
            q3 = int(request.form.get('q3'))
            q4 = int(request.form.get('q4'))
            is_lk = 'is_lk' in request.form  # Check if the checkbox was selected

            new_grade = Grade(subject=subject, q1=q1, q2=q2, q3=q3, q4=q4, is_lk=is_lk, user_id=current_user.id)
            db.session.add(new_grade)
            db.session.commit()
            flash('Grades added successfully!', 'success')

    grades = Grade.query.filter_by(user_id=current_user.id).all()

    # Per-subject points
    subject_points = {}
    total_points = 0

    for grade in grades:
        subject_total = grade.calculate_total_points()
        total_points += subject_total

        if grade.subject not in subject_points:
            subject_points[grade.subject] = 0
        subject_points[grade.subject] += subject_total

    csrf_token = generate_csrf()
    return render_template('grades.html', grades=grades, total_points=total_points, subject_points=subject_points, csrf_token=csrf_token)

@main.route('/todos/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_todo(task_id):
    task = ToDo.query.get_or_404(task_id)
    form = ToDoForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.deadline = form.deadline.data  # Update the deadline
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('main.todos'))
    return render_template('edit_todo.html', form=form)

@main.route('/todos/delete/<int:task_id>', methods=['POST'])
def delete_todo(task_id):
    task = ToDo.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('main.todos'))

@main.route('/grades/add_subject', methods=['POST'])
@login_required
def add_subject():
    subject = request.form.get('subject')
    if subject:
        # Check if the subject already exists
        if not Grade.query.filter_by(subject=subject, user_id=current_user.id).first():
            new_subject = Grade(subject=subject, user_id=current_user.id)
            db.session.add(new_subject)
            db.session.commit()
            flash('Subject added successfully!', 'success')
        else:
            flash('Subject already exists!', 'warning')
    return redirect(url_for('main.grades'))

@main.route('/grades/add', methods=['POST'])
@login_required
def add_grade():
    subject = request.form.get('subject')
    q1 = int(request.form.get('q1'))
    q2 = int(request.form.get('q2'))
    q3 = int(request.form.get('q3'))
    q4 = int(request.form.get('q4'))
    
    # Check if the checkbox was selected
    is_lk = 'is_lk' in request.form  # This will be True if checked, False otherwise

    # Check if the subject already exists
    existing_grade = Grade.query.filter_by(subject=subject, user_id=current_user.id).first()
    
    if existing_grade:
        # Update existing grades
        existing_grade.q1 = q1
        existing_grade.q2 = q2
        existing_grade.q3 = q3
        existing_grade.q4 = q4
        existing_grade.is_lk = is_lk  # Update the is_lk status
        flash('Grades updated successfully!', 'success')
    else:
        # Create a new grade entry
        new_grade = Grade(subject=subject, q1=q1, q2=q2, q3=q3, q4=q4, is_lk=is_lk, user_id=current_user.id)
        db.session.add(new_grade)
        flash('Grades added successfully!', 'success')

    db.session.commit()
    return redirect(url_for('main.grades'))

@main.route('/grades/delete/<int:subject_id>', methods=['POST'])
@login_required
def delete_subject(subject_id):
    subject = Grade.query.get_or_404(subject_id)
    db.session.delete(subject)
    db.session.commit()
    flash('Subject deleted successfully!', 'success')
    return '', 204  # No content response