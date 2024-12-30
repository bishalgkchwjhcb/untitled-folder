from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(20), nullable=False)  # 'student' or 'admin'
    department = db.Column(db.String(50))
    qr_code = db.Column(db.String(200))  # Path to QR code image

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'present' or 'absent'
    marked_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    student = db.relationship('User', foreign_keys=[student_id])
    admin = db.relationship('User', foreign_keys=[marked_by])

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
