from model.config import conn
from model.tot import get_balance

cur = conn.cursor()


def select(username):
    sql = "SELECT address,private_key FROM users WHERE username = '%s'" % username
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()
    result = cur.fetchone()
    print(username)
    try:
        return {"address": result[0], "key": result[1], "balance": get_balance(result[0])}
    except TypeError:
        return {"address": None, "key": None, "balance": 0}


def check_tot(username, value):
    balance = get_balance(select(username)["address"])
    if int(value) > balance:
        return False
    else:
        return True
