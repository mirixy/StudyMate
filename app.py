from flask import Flask, render_template, redirect, url_for, request, flash, jsonify,  session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models.db import db, bcrypt, login_manager, User, ToDo

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



if __name__ == "__main__":
    app.run(debug=True)