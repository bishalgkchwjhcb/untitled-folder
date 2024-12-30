from flask import Blueprint, render_template, send_file, redirect, url_for
from flask_login import login_required, current_user
from models import db, User, Attendance
import qrcode
import os
from datetime import datetime

bp = Blueprint('student', __name__)

@bp.route('/student/dashboard')
@login_required
def dashboard():
    if current_user.user_type != 'student':
        return redirect(url_for('admin.dashboard'))
    return render_template('student/dashboard.html')

@bp.route('/student/qr-code')
@login_required
def view_qr():
    if not current_user.qr_code:
        # Generate QR code if not exists
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(str(current_user.id))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR code
        filename = f'qr_{current_user.id}.png'
        filepath = os.path.join('static', 'qrcodes', filename)
        img.save(filepath)
        
        current_user.qr_code = filename
        db.session.commit()
    
    return render_template('student/qr_code.html')

@bp.route('/student/download-qr')
@login_required
def download_qr():
    if current_user.qr_code:
        return send_file(
            os.path.join('static', 'qrcodes', current_user.qr_code),
            as_attachment=True,
            download_name=f'qr_code_{current_user.username}.png'
        )
    return "QR Code not generated", 404

@bp.route('/student/attendance-history')
@login_required
def attendance_history():
    attendance = Attendance.query.filter_by(student_id=current_user.id).order_by(Attendance.date.desc()).all()
    return render_template('student/attendance_history.html', attendance=attendance)

@bp.route('/student/attendance-percentage')
@login_required
def attendance_percentage():
    total = Attendance.query.filter_by(student_id=current_user.id).count()
    present = Attendance.query.filter_by(student_id=current_user.id, status='present').count()
    percentage = (present / total * 100) if total > 0 else 0
    return render_template('student/attendance_percentage.html', percentage=percentage)
