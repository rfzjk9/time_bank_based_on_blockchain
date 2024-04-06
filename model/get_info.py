from templates.config import conn

cur = conn.cursor()


def select(username):
    sql = "SELECT address,private_key FROM users WHERE username = '%s'" % (username)
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()
    result = cur.fetchone()
    return {"address": result[0], "key": result[1]}
