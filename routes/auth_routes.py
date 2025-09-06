from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db, bcrypt
from models import Admin, Branch

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        
        if user_type == 'admin':
            user = Admin.query.filter_by(username=username).first()
            if user and bcrypt.check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['user_type'] = 'admin'
                session['username'] = user.username
                flash('Login successful!', 'success')
                return redirect(url_for('admin.dashboard'))
            else:
                flash('Invalid admin credentials!', 'error')
        
        elif user_type == 'branch':
            user = Branch.query.filter_by(email=username, is_active=True).first()
            if user and bcrypt.check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['user_type'] = 'branch'
                session['username'] = user.branch_name
                flash('Login successful!', 'success')
                return redirect(url_for('branch.dashboard'))
            else:
                flash('Invalid branch credentials or account not active!', 'error')
    
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out!', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        from models import BranchRegistration
        
        branch_name = request.form['branch_name']
        branch_code = request.form['branch_code']
        email = request.form['email']
        password = request.form['password']
        location = request.form['location']
        phone = request.form.get('phone', '')
        
        # Check if branch code or email already exists
        existing_branch = Branch.query.filter(
            (Branch.branch_code == branch_code) | (Branch.email == email)
        ).first()
        
        existing_registration = BranchRegistration.query.filter(
            (BranchRegistration.branch_code == branch_code) | (BranchRegistration.email == email)
        ).first()
        
        if existing_branch or existing_registration:
            flash('Branch code or email already exists!', 'error')
            return render_template('register.html')
        
        # Create registration request
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        registration = BranchRegistration(
            branch_name=branch_name,
            branch_code=branch_code,
            email=email,
            password=hashed_password,
            location=location,
            phone=phone
        )
        
        db.session.add(registration)
        db.session.commit()
        
        flash('Registration request submitted! Please wait for admin approval.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')
