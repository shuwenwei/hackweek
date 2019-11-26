import datetime
from ncumemory.models import User,Event,Comment,db
from itsdangerous import BadSignature,SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


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


def get_public_events(page,place):
    if not place:
        place = ""
    if not place.isdigit():
        public_events = Event.query.filter_by(is_private=False).order_by(Event.id.desc())\
            .limit(5).offset((page-1)*5).all()
        return public_events
    else:
        place = int(place)
        public_events = Event.query.filter_by(is_private=False,place_number=place).\
            order_by(Event.id.desc()).limit(5).offset((page-1)*5).all()
        return public_events


def get_user_all_events(page,username):
    user_events = Event.query.filter_by(author=username).order_by(Event.id.desc()).limit(5).offset((page-1)*5).all()
    return user_events


def generate_token(user):
    from ..config import Config
    serializer = Serializer(Config.SECRET_KEY,expires_in=60*60*24*7)
    token = serializer.dumps({"username":user.username,"password":user.password})
    return token.decode("ascii")


def check_token(token):
    from ..config import Config
    serializer = Serializer(Config.SECRET_KEY)
    try:
        s = serializer.loads(token)
    except BadSignature:
        return None
    except SignatureExpired:
        return None
    user = get_user_by_username(s["username"])
    return user


def get_user_public_events(page,username):
    user_public_events = Event.query.\
        filter_by(author=username,is_private=False).order_by(Event.id.desc()).limit(5).offset((page-1)*5).all()
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
    date = datetime.datetime.strptime(s,"%Y-%m-%d %H:%M")
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
