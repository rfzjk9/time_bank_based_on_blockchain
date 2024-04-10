from flask import Flask, render_template, session
from flask import redirect
from flask import url_for
from flask import request
from model.check_login import is_existed, exist_user, is_null
from model.check_regist import add_user
from model.get_info import select
import datetime
from model.encode import sha256d
from model.deal_job import post_job

# Flask基础设置
app = Flask(__name__)
app.secret_key = "12345678"
app.permanent_session_lifetime = datetime.timedelta(seconds=10 * 60)  # cookie过期时间


@app.route("/")
def index():
    if session.get("logged_in"):
        username = session["username"]
        info = select(username)
        return render_template(
            "info.html",
            username=username,
            address=info["address"],
            private_key=info["key"],
            balance=info["balance"]
        )
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":  # 注册发送的请求为POST请求
        username = request.form["username"]
        password = sha256d(request.form["password"])
        if is_null(username, password):
            login_message = "温馨提示：账号和密码是必填"
            return render_template("login.html", message=login_message)
        elif is_existed(username, password):
            session["logged_in"] = True
            session["username"] = username
            session.permanent = True
            return redirect(url_for("index"))
        elif exist_user(username):
            login_message = "温馨提示：密码错误，请输入正确密码"
            return render_template("login.html", message=login_message)
        else:
            login_message = "温馨提示：不存在该用户，请先注册"
            return render_template("login.html", message=login_message)
    if session.get("logged_in"):
        return redirect(url_for("index"))
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = sha256d(request.form["password"])
        password2 = sha256d(request.form["password2"])
        if is_null(username, password):
            login_message = "温馨提示：账号和密码是必填"
            return render_template("register.html", message=login_message)
        elif password != password2:
            login_message = "温馨提示：两次密码不一样"
            return render_template("register.html", message=login_message)
        elif exist_user(username):
            login_message = "温馨提示：用户已存在，请直接登录或者更换用户名"
            # return redirect(url_for("login", register="repeats"))
            return render_template("register.html", message=login_message)
        else:
            add_user(username, password)
            return redirect(url_for("index"))
    if session.get("logged_in"):
        return redirect(url_for("index"))
    else:
        return render_template("register.html")


@app.route("/add_job", methods=["POST"])
def add_job():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    else:
        if request.method == "POST":
            username = session["username"]
            title = request.form["title"]
            job = request.form["job"]
            date = request.form["date"]
            value = request.form["time"]
            post_job(title, job, username, int(value))
            print(title, job, username, date, value)
            return redirect(url_for("index"))


@app.route("/add", methods=["GET"])
def add():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    else:
        return render_template("add_job.html")


@app.route("/logout")
def logout():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    else:
        session.pop("logged_in")
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
