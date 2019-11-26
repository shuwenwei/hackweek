from . import event_bp
from flask import request,jsonify
from .tools import get_public_events, events_to_dicts, add_event, to_datetime, check_token


@event_bp.route('/api/ground/events',methods=["GET"])
def ground():
    page_number = str(request.args.get("pageNumber"))
    place = str(request.args.get("place"))
    if (not page_number.isdigit()) or int(page_number) < 1:
        page_number = 1
    else:
        page_number = int(page_number)
    public_events = get_public_events(page_number,place)
    next_length = len(get_public_events(page_number + 1,place))
    # code:0 这一页没有活动
    # code:1 已到最后一页
    # code:2 获取成功,且不是最后一页
    if len(public_events) == 0:
        return jsonify({
            "message":"当前页面没有内容",
            "code":0
        })
    if next_length == 0:
        return jsonify({
            "message":"已经是最后一页",
            "code":1,
            "events":events_to_dicts(public_events)
        })
    return jsonify({
        "message":"获取成功",
        "code":2,
        "events":events_to_dicts(public_events)
    })


@event_bp.route('/api/event',methods=["POST"])
def post_event():
    token = request.headers["Authorization"][9:]
    user = check_token(token)
    if user:
        author = user.username
        content = request.json["content"]
        is_private = request.json["isPrivate"]
        # 接收eventDate为字符串格式 %Y-%m-%d %H:%M
        event_date = to_datetime(request.json["eventDate"])
        is_story = request.json["isStory"]
        title = request.json["title"]
        place_number = request.json["placeNumber"]
        add_event(author,content,event_date,is_private,int(place_number),is_story,title)
        return jsonify({
            "message":"发送成功",
            "status":1
        })
    else:
        return jsonify({
            "message":"发送失败",
            "status":0
        })
