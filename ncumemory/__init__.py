from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ncumemory.config import configs

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(configs[config_name])
    db.init_app(app)
    from ncumemory.main import comment_bp,user_bp,error_bp,history_bp,event_bp
    app.register_blueprint(comment_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(error_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(event_bp)
    return app

app = create_app("default")
db.create_all("__all__",app)
if __name__ == "__main__":
    app.run(port=8000)

