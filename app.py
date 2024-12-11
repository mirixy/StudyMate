from flask import Flask, render_template, redirect, url_for, request, flash, jsonify,  session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models.db import db, bcrypt, login_manager, User, ToDo, Subject, Grade

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo_app.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwörter stimmen nicht überein.', 'error')
            return redirect(url_for('register'))
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Diese E-Mail-Adresse ist bereits registriert.', 'error')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registrierung erfolgreich! Bitte loggen Sie sich ein.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Validate user
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Ungültige E-Mail oder Passwort.', 'error')
            return redirect(url_for('login'))

        # Log in the user using Flask-Login
        login_user(user)
        flash('Erfolgreich eingeloggt!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Erfolgreich ausgeloggt.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not current_user.is_authenticated:
        flash('Bitte loggen Sie sich ein, um auf das Dashboard zuzugreifen.', 'error')
        return redirect(url_for('login'))
    
    todos = ToDo.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', todos=todos)

@app.route('/add', methods=['POST'])
@login_required
def add_todo():
    title = request.form.get('title')
    description = request.form.get('description')
    if title:  # Überschrift ist erforderlich
        new_todo = ToDo(title=title, description=description, user_id=current_user.id)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def edit_todo(todo_id):
    todo = ToDo.query.filter_by(id=todo_id, user_id=current_user.id).first()
    if not todo:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        todo.title = request.form.get('title')
        todo.description = request.form.get('description')
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('edit_todo.html', todo=todo)

@app.route('/api/todos/<int:todo_id>', methods=['GET'])
@login_required
def get_todo(todo_id):
    todo = ToDo.query.filter_by(id=todo_id, user_id=current_user.id).first()
    if not todo:
        return jsonify({'error': 'ToDo nicht gefunden'}), 404
    return jsonify({
        'id': todo.id,
        'title': todo.title,
        'description': todo.description
    })

@app.route('/delete/<int:todo_id>')
@login_required
def delete_todo(todo_id):
    todo = ToDo.query.filter_by(id=todo_id, user_id=current_user.id).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/grades', methods=['GET'])
@login_required
def get_grades():
    subjects = Subject.query.filter_by(user_id=current_user.id).all()
    grades_data = []
    
    for subject in subjects:
        grades = Grade.query.filter_by(subject_id=subject.id).all()
        subject_data = {
            'id': subject.id,
            'name': subject.name,
            'grades': [{
                'id': grade.id,
                'final_grade': grade.final_grade,
                'semester': grade.semester,
                'created_at': grade.created_at.strftime('%d.%m.%Y')
            } for grade in grades]
        }
        grades_data.append(subject_data)
    
    return jsonify(grades_data)

@app.route('/grades/add', methods=['POST'])
@login_required
def add_grade():
    try:
        data = request.json
        
        # Validate input data
        required_fields = ['subject', 'semester', 'final_grade', 'is_abitur']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if not (1.0 <= float(data['final_grade']) <= 6.0):
            return jsonify({'error': 'Grade must be between 1.0 and 6.0'}), 400

        if not (1 <= int(data['semester']) <= 4):
            return jsonify({'error': 'Semester must be between 1 and 4'}), 400

        # Get or create subject
        subject = Subject.query.filter_by(
            name=data['subject'],
            user_id=current_user.id
        ).first()
        
        if not subject:
            subject = Subject(
                name=data['subject'],
                user_id=current_user.id,
                is_abitur_subject=data['is_abitur']
            )
            db.session.add(subject)
        else:
            # Update the Abitur status if necessary
            subject.is_abitur_subject = data['is_abitur']
        
        # Check if grade for this semester already exists
        existing_grade = Grade.query.filter_by(
            subject_id=subject.id,
            semester=data['semester']
        ).first()

        if existing_grade:
            existing_grade.final_grade = data['final_grade']
        else:
            # Create new grade
            grade = Grade(
                final_grade=data['final_grade'],
                semester=data['semester'],
                subject_id=subject.id,
                user_id=current_user.id
            )
            db.session.add(grade)
        
        # Handle the Abitur grade
        if subject.is_abitur_subject and data['semester'] == 5:
            abitur_grade = Grade.query.filter_by(
                subject_id=subject.id,
                semester=5
            ).first()
            if abitur_grade:
                abitur_grade.final_grade = data['final_grade']
            else:
                abitur_grade = Grade(
                    final_grade=data['final_grade'],
                    semester=5,
                    subject_id=subject.id,
                    user_id=current_user.id
                )
                db.session.add(abitur_grade)

        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Note erfolgreich hinzugefügt'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Fehler beim Hinzufügen der Note',
            'details': str(e)
        }), 500

@app.route('/grades/delete/<int:grade_id>', methods=['DELETE'])
@login_required
def delete_grade(grade_id):
    try:
        grade = Grade.query.get_or_404(grade_id)
        
        # Check if the grade belongs to the current user
        if grade.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        db.session.delete(grade)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Note erfolgreich gelöscht'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Fehler beim Löschen der Note',
            'details': str(e)
        }), 500

@app.route('/grades/subject/<int:subject_id>', methods=['DELETE'])
@login_required
def delete_subject(subject_id):
    try:
        subject = Subject.query.get_or_404(subject_id)
        
        # Check if the subject belongs to the current user
        if subject.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Delete all grades associated with the subject
        Grade.query.filter_by(subject_id=subject_id).delete()
        
        # Delete the subject
        db.session.delete(subject)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Fach und zugehörige Noten erfolgreich gelöscht'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Fehler beim Löschen des Fachs',
            'details': str(e)
        }), 500

@app.route('/grades/calculate', methods=['GET'])
@login_required
def calculate_average():
    try:
        subjects = Subject.query.filter_by(user_id=current_user.id).all()
        total_grades = 0
        grade_count = 0
        abitur_grades = 0
        abitur_count = 0
        
        for subject in subjects:
            grades = Grade.query.filter_by(subject_id=subject.id).all()
            for grade in grades:
                if subject.is_abitur_subject:
                    abitur_grades += grade.final_grade
                    abitur_count += 1
                else:
                    total_grades += grade.final_grade
                    grade_count += 1
        
        normal_average = total_grades / grade_count if grade_count > 0 else 0
        abitur_average = abitur_grades / abitur_count if abitur_count > 0 else 0
            
        return jsonify({
            'success': True,
            'normal_average': round(normal_average, 2),
            'abitur_average': round(abitur_average, 2)
        })

    except Exception as e:
        return jsonify({
            'error': 'Fehler bei der Durchschnittsberechnung',
            'details': str(e)
        }), 500

@app.route('/subjects/add', methods=['GET', 'POST'])
@login_required
def add_subject():
    if request.method == 'POST':
        name = request.form.get('name')
        is_abitur = request.form.get('is_abitur') == 'on'  # Checkbox returns 'on' if checked

        # Check if the subject already exists
        existing_subject = Subject.query.filter_by(name=name, user_id=current_user.id).first()
        if existing_subject:
            flash('Dieses Fach existiert bereits.', 'error')
            return redirect(url_for('add_subject'))

        # Add new subject
        new_subject = Subject(name=name, user_id=current_user.id, is_abitur_subject=is_abitur)
        db.session.add(new_subject)
        db.session.commit()

        flash('Fach erfolgreich hinzugefügt.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('subject_form.html')

if __name__ == "__main__":
    app.run(debug=True)