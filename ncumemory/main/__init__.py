from flask import Blueprint

user_bp = Blueprint("user_bp",__name__)
event_bp = Blueprint("event_bp",__name__)
error_bp = Blueprint("error_bp",__name__)
history_bp = Blueprint("history_bp",__name__)
comment_bp = Blueprint("comment_bp",__name__)

from ncumemory.main import errors,user_blueprint,\
    event_blueprint,comment_blueprint,history_blueprint,tools
