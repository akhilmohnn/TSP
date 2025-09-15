from flask import Blueprint,render_template,request,redirect,url_for,flash,session
from extensions import db
from models import Auditor,Branch

bp=Blueprint('auditor',__name__)

def auditor_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_type' not in session or session['user_type'] != 'auditor':
            flash('Auditor access required!', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@auditor_required
def dashboard():
    auditor = Auditor.query.get(session['user_id'])
    branches = Branch.query.all()  
    return render_template('auditor/dashboard.html', auditor=auditor, branches=branches)
