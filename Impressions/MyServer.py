from flask import Flask, request, json
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature,SignatureExpired
from werkzeug.security import check_password_hash,generate_password_hash

from flask_cors import CORS
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:s1h2u3j4@localhost/test1?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = b"1ri1#0f11afejop"
auth = HTTPBasicAuth
db = SQLAlchemy(app)
CORS(app)

class User(db.Model):
    __tablename__ = "users"
    username = db.Column(db.String(16),nullable=False,primary_key=True)
    password = db.Column(db.String(128),nullable=False)

    def __init__(self,username,password):
        self.username = username
        self.password = generate_password_hash(password)

    def get_dict(self):
        return {
            "username":self.username,
            "password":self.password
        }


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    author = db.Column(db.String(16),nullable=False)
    content = db.Column(db.Text(4000),nullable=False)
    post_date = db.Column(db.DateTime,nullable=False)
    event_date = db.Column(db.DateTime,nullable=False)
    is_private = db.Column(db.Boolean,nullable=False)
    place_number = db.Column(db.Integer,nullable=False)
    is_story = db.Column(db.Integer,nullable=False)

    def __init__(self,author,content,post_date,event_date,is_private,place_number,is_story):
        self.author = author
        self.content = content
        self.post_date = post_date
        self.event_date = event_date
        self.is_private = is_private
        self.place_number = place_number
        self.is_story = is_story

    def get_dict(self):
        return {
            "author":self.author,
            "content":self.content,
            "event_date":self.event_date,
            "post_date":self.post_date,
            "is_private":self.is_private,
            "place_number":self.place_number,
            "is_story":self.is_story
        }


def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user
    else:
        return None


def get_password(username):
    user = get_user_by_username(username)
    if user:
        return str(user.password)
    else:
        return ""


def find_events_by_username(username):
    events = Event.query.filter_by(author=username).all()
    return events


def events_to_dicts(events):
    dicts = []
    for event in events:
        dicts.append(event.get_dict())
    return dicts


def get_public_events(page):
    public_events = Event.query.filter_by(is_private=False).order_by(Event.id.desc()).limit(5).offset((page-1)*5).all()
    return public_events


def get_user_all_events(page,username):
    user_events = Event.query.filter_by(author=username).order_by(Event.id.desc()).limit(5).offset((page-1)*5).all()
    return user_events


def generate_token(user):
    serializer = Serializer(app.secret_key,expires_in=60*60*24*7)
    token = serializer.dumps({"username":user.username,"password":user.password})
    return token.decode("ascii")


def check_token(token):
    serializer = Serializer(app.secret_key)
    try:
        s = serializer.loads(token)
    except BadSignature:
        return None
    except SignatureExpired:
        return None
    user = get_user_by_username(s["username"])
    return user


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


def add_event(author,content,event_date,is_private,place_number,is_story):
    event = Event(author,content,datetime.datetime.now(),event_date,is_private,place_number,is_story)
    db.session.add(event)
    db.session.commit()


@app.route('/api/token',methods=["POST"])
def login():
    username = request.json["username"]
    password = request.json["password"]
    # if password == get_password(username):
    if check_password_hash(get_password(username),password):
        token = generate_token(get_user_by_username(username))
        return json.dumps({
            "token":token,
            "message":"获取成功",
            "status":1
        })
    else:
        return json.dumps({
            "message": "账户名或密码错误",
            "status": 0
        })


@app.route('/api/register',methods=["POST"])
def register():
    username = request.json["username"]
    password = request.json["password"]
    if add_user(username,password):
        return json.dumps({
            "message":"注册成功",
            "status":1
        })
    else:
        return json.dumps({
            "message":"注册失败",
            "status":0
        })


@app.route('/api/postEvent',methods=["POST"])
def post_event():
    token = request.headers["Authorization"][9:]
    print(token)
    user = check_token(token)
    if user:
        author = user.username
        content = request.json["content"]
        is_private = request.json["isPrivate"]
        # 接收eventDate为字符串格式 %Y/%m/%d %H:%M
        event_date = to_datetime(request.json["eventDate"])
        is_story = request.json["isStory"]
        place_number = request.json["placeNumber"]
        add_event(author,content,event_date,is_private,int(place_number),is_story)
        return json.dumps({
            "message":"发送成功",
            "status":1
        })
    else:
        return json.dumps({
            "message":"发送失败",
            "status":0
        })


@app.route('/api/getGroundEvents',methods=["GET"])
def ground():
    page_number = request.args.get("pageNumber")
    if not page_number or int(page_number) < 1:
        page_number = 1
    else:
        page_number = int(page_number)
    public_events = get_public_events(page_number)
    next_length = len(get_public_events(page_number + 1))
    # code:0 这一页没有活动
    # code:1 以到最后一页
    # code:2 获取成功,且不是最后一页
    if len(public_events) == 0:
        return json.dumps({
            "message":"当前页面没有内容",
            "code":0
        })
    if next_length == 0:
        return json.dumps({
            "message":"已经是最后一页",
            "code":1,
            "events":events_to_dicts(public_events)
        })
    return json.dumps({
        "message":"获取成功",
        "code":2,
        "events":events_to_dicts(public_events)
    })


@app.route('/api/getHistory',methods=["GET"])
def user_history():
    token = request.headers["Authorization"][9:]
    user = check_token(token)
    username = request.args.get("username")
    page_number = request.args.get("pageNumber")
    if not get_user_by_username(username):
        return json.dumps({
            "message":"用户名不存在",
            "code":0
        })
    if not page_number or int(page_number) < 1:
        page_number = 1
    else:
        page_number = int(page_number)
    if user and username == user.username:
        events = get_user_all_events(page_number,username)
        next_events = get_user_all_events(page_number+1,username)
    else:
        events = get_user_public_events(page_number,username)
        next_events = get_user_public_events(page_number + 1, username)
    # code:0 这一页没有活动
    # code:1 以到最后一页
    # code:2 获取成功,且不是最后一页
    if len(events) == 0:
        return json.dumps({
            "message":"该用户当前页面没有内容",
            "code":0,
        })
    if len(next_events) == 0:
        return json.dumps({
            "message":"已经是最后一页",
            "code":1,
            "events":events_to_dicts(events)
        })
    else:
        return json.dumps({
            "message":"获取成功",
            "code":2,
            "events":events_to_dicts(events)
        })

db.create_all()
if __name__ == "__main__":
    app.run(port=8000)