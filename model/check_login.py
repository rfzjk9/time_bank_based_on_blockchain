from templates.config import conn

cur = conn.cursor()


def is_null(username, password):
    if username == "" or password == "":
        return True
    else:
        return False


def is_existed(username, password):
    sql = "SELECT * FROM users WHERE username ='%s' and password ='%s'" % (
        username,
        password,
    )
    # 防报错
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()

    result = cur.fetchall()
    if len(result) == 0:
        return False
    else:
        return True


def exist_user(username):
    sql = "SELECT * FROM users WHERE username ='%s'" % (username)
    # 防报错
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()

    result = cur.fetchall()
    if len(result) == 0:
        return False
    else:
        return True
