class Config:
    #General Flask Config
    FLASK_ENV = "development"
    FLASK_APP = 'endpoint.py'
    FLASK_DEBUG = True

    #Database config
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:''@localhost/callejero_ine'
    SECRET_KEY = 'cosa'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False