from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    deadline = db.Column(db.DateTime, nullable=True)

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    q1 = db.Column(db.Integer, default=0)
    q2 = db.Column(db.Integer, default=0)
    q3 = db.Column(db.Integer, default=0)
    q4 = db.Column(db.Integer, default=0)
    is_lk = db.Column(db.Boolean, default=False)  # New field for LK status
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def calculate_total_points(self):
        total = self.q1 + self.q2 + self.q3 + self.q4
        return total * 2 if self.is_lk else total  # Weight by 2 if LK