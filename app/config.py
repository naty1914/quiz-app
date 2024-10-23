class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test1_secret_key'