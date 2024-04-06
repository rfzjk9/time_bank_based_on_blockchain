from templates.config import conn
from model.tot import create_account

cur = conn.cursor()


def add_user(username, password):
    acc = create_account()
    address = str(acc.address)
    key = str(acc.key.hex())
    sql = (
        "INSERT INTO users(username, password, address, private_key) VALUES ('%s','%s','%s','%s')"
        % (username, password, address, key)
    )
    # 防报错
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()
    # execute(sql)
    conn.close()
