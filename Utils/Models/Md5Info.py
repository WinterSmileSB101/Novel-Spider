class Md5Info:
    MD5: str
    Salt: bytes

    def __init__(self):
        self.MD5 = ''
        self.Salt = b''