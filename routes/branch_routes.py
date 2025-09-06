from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db
from models import Branch

bp = Blueprint('branch', __name__)

def branch_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_type' not in session or session['user_type'] != 'branch':
            flash('Branch access required!', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@branch_required
def dashboard():
    branch = Branch.query.get(session['user_id'])
    return render_template('branch/dashboard.html', branch=branch)

@bp.route('/profile')
@branch_required
def profile():
    branch = Branch.query.get(session['user_id'])
    return render_template('branch/profile.html', branch=branch)

@bp.route('/update_profile', methods=['POST'])
@branch_required
def update_profile():
    branch = Branch.query.get(session['user_id'])
    
    branch.phone = request.form.get('phone', branch.phone)
    branch.location = request.form.get('location', branch.location)
    
    db.session.commit()
    
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('branch.profile'))
