import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'q1qwj13aw13aw'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app():
        pass


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost/test4?charset=utf8mb4"

configs = {
    "default":ProductionConfig
}
