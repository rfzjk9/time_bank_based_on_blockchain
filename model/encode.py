from hashlib import sha256


def sha256d(data):
    if not isinstance(data, bytes):
        data = data.encode()
    return sha256(sha256(data).digest()).hexdigest()
