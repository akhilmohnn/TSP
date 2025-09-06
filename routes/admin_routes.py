from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db, bcrypt
from models import Admin, Branch, BranchRegistration
from datetime import datetime

bp = Blueprint('admin', __name__)

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_type' not in session or session['user_type'] != 'admin':
            flash('Admin access required!', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@admin_required
def dashboard():
    total_branches = Branch.query.count()
    active_branches = Branch.query.filter_by(is_active=True).count()
    pending_registrations = BranchRegistration.query.filter_by(status='pending').count()
    recent_branches = Branch.query.order_by(Branch.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         total_branches=total_branches,
                         active_branches=active_branches,
                         pending_registrations=pending_registrations,
                         recent_branches=recent_branches)

@bp.route('/branches')
@admin_required
def branches():
    branches = Branch.query.all()
    return render_template('admin/branches.html', branches=branches)

@bp.route('/add_branch', methods=['GET', 'POST'])
@admin_required
def add_branch():
    if request.method == 'POST':
        branch_name = request.form['branch_name']
        branch_code = request.form['branch_code']
        email = request.form['email']
        password = request.form['password']
        location = request.form['location']
        phone = request.form.get('phone', '')
        
        # Check if branch code or email already exists
        existing = Branch.query.filter(
            (Branch.branch_code == branch_code) | (Branch.email == email)
        ).first()
        
        if existing:
            flash('Branch code or email already exists!', 'error')
            return render_template('admin/add_branch.html')
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        branch = Branch(
            branch_name=branch_name,
            branch_code=branch_code,
            email=email,
            password=hashed_password,
            location=location,
            phone=phone,
            created_by=session['user_id']
        )
        
        db.session.add(branch)
        db.session.commit()
        
        flash('Branch added successfully!', 'success')
        return redirect(url_for('admin.branches'))
    
    return render_template('admin/add_branch.html')

@bp.route('/registrations')
@admin_required
def registrations():
    registrations = BranchRegistration.query.order_by(BranchRegistration.submitted_at.desc()).all()
    return render_template('admin/registrations.html', registrations=registrations)

@bp.route('/approve_registration/<int:registration_id>')
@admin_required
def approve_registration(registration_id):
    registration = BranchRegistration.query.get_or_404(registration_id)
    
    if registration.status != 'pending':
        flash('Registration already processed!', 'error')
        return redirect(url_for('admin.registrations'))
    
    # Create new branch
    branch = Branch(
        branch_name=registration.branch_name,
        branch_code=registration.branch_code,
        email=registration.email,
        password=registration.password,  # Already hashed
        location=registration.location,
        phone=registration.phone,
        created_by=session['user_id']
    )
    
    # Update registration status
    registration.status = 'approved'
    registration.reviewed_at = datetime.utcnow()
    registration.reviewed_by = session['user_id']
    
    db.session.add(branch)
    db.session.commit()
    
    flash('Registration approved and branch created!', 'success')
    return redirect(url_for('admin.registrations'))

@bp.route('/reject_registration/<int:registration_id>', methods=['POST'])
@admin_required
def reject_registration(registration_id):
    registration = BranchRegistration.query.get_or_404(registration_id)
    
    if registration.status != 'pending':
        flash('Registration already processed!', 'error')
        return redirect(url_for('admin.registrations'))
    
    rejection_reason = request.form.get('rejection_reason', '')
    
    registration.status = 'rejected'
    registration.reviewed_at = datetime.utcnow()
    registration.reviewed_by = session['user_id']
    registration.rejection_reason = rejection_reason
    
    db.session.commit()
    
    flash('Registration rejected!', 'success')
    return redirect(url_for('admin.registrations'))

@bp.route('/toggle_branch/<int:branch_id>')
@admin_required
def toggle_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    branch.is_active = not branch.is_active
    db.session.commit()
    
    status = 'activated' if branch.is_active else 'deactivated'
    flash(f'Branch {status} successfully!', 'success')
    return redirect(url_for('admin.branches'))
