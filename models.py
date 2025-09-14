from extensions import db
from datetime import datetime

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Admin {self.username}>'

class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch_name = db.Column(db.String(100), unique=True, nullable=False)
    branch_code = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    
    admin = db.relationship('Admin', backref=db.backref('branches', lazy=True))
    
    def __repr__(self):
        return f'<Branch {self.branch_name}>'
    
class Auditor(db.Model):
    __tablename__ = 'auditors'   # ✅ force correct table name

    id = db.Column(db.Integer, primary_key=True)
    auditor_name = db.Column(db.String(100), nullable=False)
    emp_code = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

    def __repr__(self):
        return f'<Auditor {self.auditor_name}>'
    

class BranchRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch_name = db.Column(db.String(100), nullable=False)
    branch_code = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=True)
    rejection_reason = db.Column(db.Text, nullable=True)
    
    reviewer = db.relationship('Admin', backref=db.backref('reviewed_registrations', lazy=True))
    
    def __repr__(self):
        return f'<BranchRegistration {self.branch_name} - {self.status}>'
