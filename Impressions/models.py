from werkzeug.security import generate_password_hash
from MyServer import db


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
