from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from app.models import ToDo, User, Grade
from app.forms import ToDoForm

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
        subject = request.form.get('subject')
        points = int(request.form.get('points'))
        new_grade = Grade(subject=subject, points=points, user_id=current_user.id)
        db.session.add(new_grade)
        db.session.commit()
        flash('Grade added successfully!', 'success')

    # Calculate total points for each subject for the current user
    grades = Grade.query.filter_by(user_id=current_user.id).all()
    total_points = {}
    for grade in grades:
        if grade.subject not in total_points:
            total_points[grade.subject] = 0
        total_points[grade.subject] += grade.points

    return render_template('grades.html', total_points=total_points, grades=grades)

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

