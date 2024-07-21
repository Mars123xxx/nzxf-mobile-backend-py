import hashlib


def encode_pwd(pwd: str):
    return hashlib.sha3_256(pwd.encode()).hexdigest()


if __name__ == '__main__':
    print(encode_pwd('123'))