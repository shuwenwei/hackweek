from flask import jsonify,request
from .tools import get_user_by_username, check_token, get_user_all_events, get_user_public_events, events_to_dicts
from . import history_bp


@history_bp.route('/api/user/comments',methods=["GET"])
def get_user_comments():
    if "username" in request.args:
        username = request.args.get("username")
        user = get_user_by_username(username)
        return jsonify({
            "message":"获取成功",
            "status":1,
            "comments":[comment.get_dict() for comment in user.author_comments]
        })
    else:
        return jsonify({
            "message":"获取失败",
            "status":0,
        })


@history_bp.route('/api/user/history',methods=["GET"])
def user_history():
    token = request.headers["Authorization"][9:]
    user = check_token(token)
    username = request.args.get("username")
    page_number = request.args.get("pageNumber")
    if not get_user_by_username(username):
        return jsonify({
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
        return jsonify({
            "message":"该用户当前页面没有内容",
            "code":0,
        })
    if len(next_events) == 0:
        return jsonify({
            "message":"已经是最后一页",
            "code":1,
            "events":events_to_dicts(events)
        })
    else:
        return jsonify({
            "message":"获取成功",
            "code":2,
            "events":events_to_dicts(events)
        })
