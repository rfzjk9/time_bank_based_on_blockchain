from templates.config import conn
from model.tot import get_balance, private_transfer, admin_address, admin_key, check_tot
from model import get_info


cur = conn.cursor()


def post_job(title, info, username, value):
    if not check_tot(username, value):
        return False
    else:
        sql = (
            "INSERT INTO articles(post_username, title, info, value, Ordered, Finished) VALUES ('%s','%s','%s','%d', 0,"
            " 0)"
            % (username, title, info, value)
        )
        # 防报错
        conn.ping(reconnect=True)
        cur.execute(sql)
        conn.commit()
        conn.close()
        info = get_info.select(username)
        if private_transfer(
            info["address"],
            admin_address,
            value,
            info["key"],
        ):
            return True
        else:
            return False


def get_job(job_id, username):
    sql = "SELECT Ordered FROM articles WHERE id = '%d' " % job_id
    # 防报错
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()

    result = cur.fetchall()
    print(result)
    if result[0][0]:
        conn.close()
        return False
    else:
        sql = (
            "UPDATE articles SET take_username = '%s', Ordered = 1 WHERE id = '%d'"
            % (username, job_id)
        )
        conn.ping(reconnect=True)
        cur.execute(sql)
        conn.commit()
        # execute(sql)
        conn.close()
        return True


def finish_job(job_id):
    sql = (
        "SELECT articles.value,users.address FROM articles JOIN users ON articles.take_username = users.username "
        "WHERE id = '%d' "
        % job_id
    )
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()
    result = cur.fetchall()
    value = result[0][0]
    to_address = result[0][1]
    private_transfer(admin_address, to_address, value, admin_key)
    sql = "UPDATE articles SET Finished = 1 WHERE id = '%d'" % job_id
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()
    # execute(sql)
    conn.close()
    return True


def cancel_order(job_id):
    sql = "SELECT Finished FROM articles WHERE id = '%d' " % job_id
    # 防报错
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()

    result = cur.fetchall()
    if result[0][0]:
        conn.close()
        return False
    else:
        sql = "UPDATE articles SET Ordered = 0,take_username = NULL WHERE id = '%d'" % job_id

        conn.ping(reconnect=True)
        cur.execute(sql)
        conn.commit()
        # execute(sql)
        conn.close()
        return True


def delete_job(job_id):
    sql = "SELECT Ordered,Finished FROM articles WHERE id = '%d' " % job_id
    # 防报错
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()

    result = cur.fetchall()
    if result[0][0] or result[0][1]:
        conn.close()
        return False
    else:
        sql = "DELETE FROM articles WHERE id = '%d'" % job_id
        conn.ping(reconnect=True)
        cur.execute(sql)
        conn.commit()
        # execute(sql)
        conn.close()
        return True
