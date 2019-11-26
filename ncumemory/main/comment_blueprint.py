from . import comment_bp
from flask import request,jsonify
from .tools import check_token, add_comment
from ..models import Event


@comment_bp.route('/api/event/comments',methods=["GET"])
def get_event_comments():
    event_id = request.args.get("eid")
    event_id = int(event_id)
    event = Event.query.filter_by(id=event_id).first()
    if event:
        return jsonify({
            "comments":[comment.get_dict() for comment in event.event_comments],
            "message":"获取成功",
            "status":1
        })
    else:
        return jsonify({
            "message":"获取失败",
            "status":0
        })


@comment_bp.route('/api/event/comment',methods=["POST"])
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
            return jsonify({
                "message":"请求数据错误",
                "status":0
            })
        return jsonify({
            "message":"发送成功",
            "status":1
        })
    else:
        return jsonify({
            "message":"发送失败",
            "status":0
        })
