from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import datetime

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
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    author = db.Column(db.String(16),nullable=False)
    content = db.Column(db.String(16),nullable=False)
    post_date = db.Column(db.DateTime,nullable=False)
    event_date = db.Column(db.DateTime,nullable=False)
    is_private = db.Column(db.Boolean,nullable=False)

    def __init__(self,author,content,post_date,event_date,is_private):
        self.author = author
        self.content = content
        self.post_date = post_date
        self.event_date = event_date
        self.is_private = is_private

    def get_dict(self):
        return {
            "author":self.author,
            "content":self.content,
            "event_date":self.event_date,
            "post_date":self.post_date
        }


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def get_password(username):
    user = get_user_by_username(username)
    return str(user.password)


def find_events_by_username(username):
    events = Event.query.filter_by(author=username).all()
    return events


def get_public_events(page):
    public_events = Event.query.filter_by(is_private=False).order_by(Event.id.desc()).limit(5).offset((page-1)*5).all()
    return public_events


def get_user_all_events(page,username):
    user_events = Event.query.filter_by(author=username).order_by(Event.id.desc()).limit(5).offset((page-1)*5).all()
    return user_events


def get_user_public_events(page,username):
    user_public_events = Event.query.filter_by(author=username,is_private=False).order_by(Event.id.desc()).limit(5).offset((page-1)*5).all()
    return user_public_events


def add_user(username,password):
    if not get_user_by_username(username):
        user = User(username,password)
        db.session.add(user)
        db.session.commit()
        return True
    else:
        return False


def to_datetime(s):
    date = datetime.datetime.strptime(s,"%Y/%m/%d %H:%M")
    return date


def add_event(author,content,event_date,is_private):
    event = Event(author,content,datetime.datetime.now(),event_date,is_private)
    db.session.add(event)
    db.session.commit()


@app.route('/login',methods=["GET","POST"])
def login():
#     if session["userne"]:
#         return redirect(url_for("home"))
    if request.method == "POST":
        username = request.json["username"]
        password = request.json["password"]
        if str(username).__len__() == 0:
            return "用户名为空",0
        elif password != get_password(username):
            return "用户名或密码错误",0
        else:
            session["username"] = username
            return redirect("home"),1
    else:
        return render_template("login.html")


@app.route('/register',methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.json["username"]
        password = request.json["password"]
        if add_user(username,password):
            return redirect("login")
        else:
            return "注册失败"
    else:
        return render_template("register.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route('/postEvent',methods=["POST","GET"])
def post_event():
    if session["username"]:
        if request.method == "GET":
            return render_template("editEvent.html")
        e = request.json
        author = session["username"]
        content = e["content"]
        is_private = e["isPrivate"]
        # 接收eventDate为字符串格式 %Y/%m/%d %H:%M
        event_date = to_datetime(e["eventDate"])
        add_event(author,content,event_date,is_private)
        return redirect(url_for("ground"))
    else:
        return redirect(url_for("login"))


@app.route('/ground',methods=["GET"])
def ground():
    page_number = request.args.get("pageNumber")
    if not page_number or int(page_number) < 0:
        page_number = 1
    else:
        page_number = int(page_number)
    public_events = get_public_events(page_number)
    # 待修改
    # --------------------------------------------
    current_length = len(public_events)
    next_length = len(get_public_events(page_number+1))
    if current_length == 0:
        return redirect(url_for("ground",pageNumber=1))
    if next_length == 0 and current_length == 5:
        return render_template("ground.html", public_events=public_events, length=current_length,next_length=next_length)
    return render_template("ground.html",public_events=public_events,length=current_length)
# --------------------------------------------------

@app.route('/history',methods=["GET"])
def get_content_history():
    username = request.args.get("username")
    page_number = request.args.get("pageNumber")
    if not page_number:
        page_number = 1
    else:
        page_number = int(page_number)
    if "username" in session and session["username"] == username:
        events = get_user_all_events(page_number,username)
    else:
        events = get_user_public_events(page_number,username)
    length = len(events)
    # 待修改
    if length == 0:
        return redirect(url_for("ground", pageNumber=1,username=username))
    return render_template("history.html",events=events,length=length)


@app.route('/')
def home():
    username = session.get("username")
    if username:
        user = get_user_by_username(username)
        return render_template("home.html",user=user)
    else:
        return redirect(url_for("login"))

# db.create_all()
# user1 = User("aaa","123456")
# user2 = User("bbb","12345")
# db.session.add(user1)
# db.session.add(user2)
# db.session.commit()
# event1 = Event("aaa","aejfafae",datetime.date.today(),to_datetime("2019/11/19 12:40"),False)
# event2 = Event("aaa","afafeawafawf",datetime.date.today(),to_datetime("2019/11/19 12:41"),False)
# db.session.add(event1)
# db.session.add(event2)
# db.session.commit()
if __name__ == "__main__":
    app.run(port=8000)
# add_event("bbb","9999999999999",to_datetime("2019/11/19 12:40"),False)
# add_event("bbb","44444444444",to_datetime("2019/11/19 12:40"),False)
# add_event("bbb","5555555555",to_datetime("2019/11/19 12:40"),False)
# add_event("bbb","666666666",to_datetime("2019/11/19 12:40"),False)
# add_event("bbb","7777777",to_datetime("2019/11/19 12:40"),False)
# add_event("bbb","1qaaaaaaaaaaaa",to_datetime("2019/11/19 12:59"),False)
# public_events = get_public_events(2)
# for pe in public_events:
#     pass
# print(pe.content)
