class Config:
    TESTING = True
    SECRET_KEY = 'so_much_testing_secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGIN_REQUIRED_DISABLED = True
    ADMIN_LOGIN_REQUIRED_DISABLED = True
