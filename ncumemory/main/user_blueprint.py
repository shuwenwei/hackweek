from werkzeug.security import check_password_hash, generate_password_hash
from . import user_bp
from flask import request,jsonify
from .tools import get_user_by_username, add_user, get_password, generate_token
from ..models import db


@user_bp.route('/api/username',methods=["GET"])
def check_username():
    if "username" in request.args:
        username = request.args.get("username")
        if len(username) == 0:
            return jsonify({
                "message":"用户名不能为空",
                "status":0
            })
        elif get_user_by_username(username):
            return jsonify({
                "message":"用户名已存在",
                "status":0
            })
        else:
            return jsonify({
                "message":"用户名可用",
                "status":1
            })
    return jsonify({
        "message":"请输入用户名",
        "status":0
    })


@user_bp.route('/api/token',methods=["POST"])
def login():
    username = request.json["username"]
    password = request.json["password"]
    # if password == get_password(username):
    if check_password_hash(get_password(username),password):
        token = generate_token(get_user_by_username(username))
        return jsonify({
            "token":token,
            "message":"获取成功",
            "status":1
        })
    else:
        return jsonify({
            "message": "账户名或密码错误",
            "status": 0
        })


@user_bp.route('/api/register',methods=["POST"])
def register():
    username = request.json["username"]
    password = request.json["password"]
    if add_user(username,password):
        return jsonify({
            "message":"注册成功",
            "status":1
        })
    else:
        return jsonify({
            "message":"注册失败",
            "status":0
        })


@user_bp.route('/api/password',methods=["PUT"])
def modify_password():
    username = request.json["username"]
    password = request.json["password"]
    new_password = request.json["newPassword"]
    if check_password_hash(get_password(username), password):
        user = get_user_by_username(username)
        user.password = generate_password_hash(new_password)
        db.session.add(user)
        db.session.commit()
        return jsonify({
            "message":"修改成功",
            "status":1
        })
    else:
        return jsonify({
            "message":"修改失败",
            "status":0
        })
