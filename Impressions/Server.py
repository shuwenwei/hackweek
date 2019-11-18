from flask import Flask,render_template,request,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required,login_user
from flask_cors import CORS
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:s1h2u3j4@localhost/testdb?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = b"1ri1#0f11afejop"
db = SQLAlchemy(app)
CORS(app)

class User(db.Model):
    __tablename__ = "users"
    username = db.Column(db.String(16),nullable=False,primary_key=True)
    password = db.Column(db.String(16),nullable=False)

    def __init__(self,username,password):
        self.username = username
        self.password = password

    def get_dict(self):
        return {
            "username":self.username,
            "password":self.password
        }


class Event(db.Model):
    __tablename__ = "events"
    author = db.Column(db.String(16),nullable=False)
    content = db.Column(db.String(16),nullable=False)
    date = db.Column(db.DateTime,nullable=False)
    is_private = db.Column(db.Boolean,nullable=False)

    def __init__(self,author,content,date,is_private):
        self.author = author
        self.content = content
        self.date = date
        self.is_private = is_private

    def get_dict(self):
        return {
            "author":self.author,
            "content":self.content,
            "date":self.date
        }


def get_password(username):
    user = User.query.filter_by(username=username).first()
    return str(user.password)

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.json["username"]
        password = request.json["password"]
        if password != get_password(username):
            return "用户名或密码错误",0
        else:
            return redirect("home"),1
    else:
        return render_template("login.html")


@app.route('/register',methods=["GET","POST"])
def register():
    if request.method == "POST":
        pass
    else:

        return render_template("register.html")

@app.route('/')
def home():
    return render_template("")