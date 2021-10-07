class Config():
    SECRET_KEY = 'ASDGHJKLDFGHJK'
    SQLALCHEMY_DATABASE_URI = 'mariadb+mariadbconnector://root:''@127.0.0.1:3306/CarrosDB'
    SQLALCHEMY_TRACK_MODIFICATIONS = False