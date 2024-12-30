from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from models import db, User, Attendance
from datetime import datetime

bp = Blueprint('admin', __name__)

@bp.route('/admin/dashboard')
@login_required
def dashboard():
    if current_user.user_type != 'admin':
        return redirect(url_for('student.dashboard'))
    return render_template('admin/dashboard.html')

@bp.route('/admin/scan-qr', methods=['GET', 'POST'])
@login_required
def scan_qr():
    if request.method == 'POST':
        student_id = request.form.get('qr_data')
        student = User.query.get(student_id)
        
        if not student or student.user_type != 'student':
            return jsonify({'error': 'Invalid QR Code'}), 400
            
        # Mark attendance
        attendance = Attendance(
            student_id=student.id,
            date=datetime.now().date(),
            time=datetime.now().time(),
            status='present',
            marked_by=current_user.id
        )
        db.session.add(attendance)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'student': {
                'name': student.username,
                'department': student.department
            }
        })
    
    return render_template('admin/scan_qr.html')

@bp.route('/admin/analytics')
@login_required
def analytics():
    department = request.args.get('department')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Attendance.query
    
    if department:
        query = query.join(User).filter(User.department == department)
    if start_date:
        query = query.filter(Attendance.date >= start_date)
    if end_date:
        query = query.filter(Attendance.date <= end_date)
        
    attendance_data = query.all()
    
    # Calculate statistics
    total_students = User.query.filter_by(user_type='student').count()
    present_count = len([a for a in attendance_data if a.status == 'present'])
    absent_count = total_students - present_count
    
    return render_template('admin/analytics.html',
                         present_count=present_count,
                         absent_count=absent_count,
                         total_students=total_students)

@bp.route('/admin/search-students')
@login_required
def search_students():
    query = request.args.get('query', '')
    students = User.query.filter(
        User.user_type == 'student',
        User.username.ilike(f'%{query}%')
    ).all()
    return render_template('admin/search_students.html', students=students)

@bp.route('/admin/student/<int:student_id>')
@login_required
def student_details(student_id):
    student = User.query.get_or_404(student_id)
    attendance = Attendance.query.filter_by(student_id=student_id).order_by(Attendance.date.desc()).all()
    return render_template('admin/student_details.html', student=student, attendance=attendance)
