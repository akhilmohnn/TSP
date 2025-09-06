# Database Configuration
import os

def get_database_uri():
    """Get the database URI based on DATABASE_TYPE"""
    database_type = os.environ.get('DATABASE_TYPE', 'sqlite')
    
    if database_type == 'mysql':
        mysql_user = 'root'
        mysql_password = ''  # Empty password for XAMPP/WAMP default
        mysql_host = 'localhost'
        mysql_port = '3306'
        mysql_database = 'branch_management_db'
        return f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}'
    else:
        return 'sqlite:///login_system.db'

class Config:
    SECRET_KEY = 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # MySQL Database Configuration - Update these with your MySQL details
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''  # Empty password for XAMPP/WAMP default
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = '3306'
    MYSQL_DATABASE = 'branch_management_db'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
