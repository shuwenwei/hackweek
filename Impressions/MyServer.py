from flask import Flask,request,json
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature,SignatureExpired
import datetime
from flask_cors import CORS
from werkzeug.security import check_password_hash,generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:s1h2u3j4@localhost/test3?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = b"1ri1#0f11afejop"
db = SQLAlchemy(app)
CORS(app)


class Comment(db.Model):
    __tablename__ = "comments"
    comment_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    comment_content = db.Column(db.Text(1000),nullable=False)
    comment_author = db.Column(db.String(16),db.ForeignKey("users.username"))
    event_id = db.Column(db.Integer,db.ForeignKey("events.id"))
    event = db.relationship("Event",backref=db.backref("event_comments"))
    author = db.relationship("User",backref=db.backref("author_comments"))

    def get_dict(self):
        return {
            "comment_content":self.comment_content,
            "comment_author":self.comment_author,
            "title_of_event":Event.query.filter_by(id=self.event_id).first().title
        }


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
    title = db.Column(db.String(50),nullable=False)
    is_private = db.Column(db.Boolean,nullable=False)
    place_number = db.Column(db.Integer,nullable=False)
    is_story = db.Column(db.Integer,nullable=False)

    def __init__(self,author,content,post_date,event_date,is_private,place_number,is_story,title):
        self.author = author
        self.content = content
        self.post_date = post_date
        self.event_date = event_date
        self.is_private = is_private
        self.place_number = place_number
        self.is_story = is_story
        self.title = title

    def get_dict(self):
        return {
            "author":self.author,
            "content":self.content,
            "event_date":self.event_date,
            "post_date":self.post_date,
            "is_private":self.is_private,
            "place_number":self.place_number,
            "is_story":self.is_story,
            "title":self.title,
            "event_id":self.id
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


def add_comment(eid,content,author):
    comment = Comment(event_id=eid,comment_author=author,comment_content=content)
    comment.author_username = author
    db.session.add(comment)
    db.session.commit()


def add_event(author,content,event_date,is_private,place_number,is_story,title):
    event = Event(author,content,datetime.datetime.now(),event_date,is_private,place_number,is_story,title)
    db.session.add(event)
    db.session.commit()


@app.route('/auth/user/comments',methods=["GET"])
def get_user_comments():
    if "username" in request.args:
        username = request.args.get("username")
        user = get_user_by_username(username)
        return json.jsonify({
            "message":"获取成功",
            "status":1,
            "comments":[comment.get_dict() for comment in user.author_comments]
        })
    else:
        return json.jsonify({
            "message":"获取失败",
            "status":0,
        })


@app.route('/api/username',methods=["GET"])
def check_username():
    if "username" in request.args:
        username = request.args.get("username")
        if len(username) == 0:
            return json.jsonify({
                "message":"用户名不能为空",
                "status":0
            })
        elif get_user_by_username(username):
            return json.jsonify({
                "message":"用户名已存在",
                "status":0
            })
        else:
            return json.jsonify({
                "message":"用户名可用",
                "status":1
            })
    return json.jsonify({
        "message":"请输入用户名",
        "status":0
    })


@app.route('/auth/event/comments',methods=["GET"])
def get_event_comments():
    event_id = request.args.get("eid")
    event_id = int(event_id)
    event = Event.query.filter_by(id=event_id).first()
    if event:
        return json.dumps({
            "comments":[comment.get_dict() for comment in event.event_comments],
            "message":"获取成功",
            "status":1
        })
    else:
        return json.dumps({
            "message":"获取失败",
            "status":0
        })


@app.route('/auth/event/comment',methods=["POST"])
def post_comment():
    token = request.headers["Authorization"][9:]
    user = check_token(token)
    if user:
        comment_author = user.username
        event_id = request.json["eid"]
        comment_content = request.json["commentContent"]
        try:
            add_comment(event_id,comment_content,comment_author)
        except:
            return json.jsonify({
                "message":"请求数据错误",
                "status":0
            })
        return json.jsonify({
            "message":"发送成功",
            "status":1
        })
    else:
        return json.jsonify({
            "message":"发送失败",
            "status":0
        })


@app.route('/auth/token',methods=["POST"])
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


@app.route('/auth/register',methods=["POST"])
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


@app.route('/auth/password',methods=["POST"])
def modify_password():
    username = request.json["username"]
    password = request.json["password"]
    new_password = request.json["newPassword"]
    if check_password_hash(get_password(username), password):
        user = get_user_by_username(username)
        user.password = generate_password_hash(new_password)
        db.session.add(user)
        db.session.commit()
        return json.jsonify({
            "message":"修改成功",
            "status":1
        })
    else:
        return json.jsonify({
            "message":"修改失败",
            "status":0
        })


@app.route('/auth/event',methods=["POST"])
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
        title = request.json["title"]
        place_number = request.json["placeNumber"]
        add_event(author,content,event_date,is_private,int(place_number),is_story,title)
        return json.dumps({
            "message":"发送成功",
            "status":1
        })
    else:
        return json.dumps({
            "message":"发送失败",
            "status":0
        })


@app.route('/auth/ground/events',methods=["GET"])
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


@app.route('/auth/user/history',methods=["GET"])
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
    app.run(port=8000,host="0.0.0.0")
