from flask import Flask, render_template, request, redirect, url_for, flash, session
from extensions import db, bcrypt
from config import config
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)

# Load configuration
config_name = os.environ.get('FLASK_ENV') or 'development'
app.config.from_object(config[config_name])

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)

# Import models after app initialization
from models import Admin, Branch, BranchRegistration

# Import routes
from routes import auth_routes, admin_routes, branch_routes

# Register blueprints
app.register_blueprint(auth_routes.bp)
app.register_blueprint(admin_routes.bp, url_prefix='/admin')
app.register_blueprint(branch_routes.bp, url_prefix='/branch')

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create default admin if not exists
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(
                username='admin',
                email='admin@example.com',
                password=bcrypt.generate_password_hash('admin123').decode('utf-8')
            )
            db.session.add(admin)
            db.session.commit()
    
    app.run(debug=True)
