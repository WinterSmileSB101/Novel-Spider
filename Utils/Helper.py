import os
import hashlib

from Utils.Models.Md5Info import Md5Info


class Helper:

    _SALT_BYTE_SIZE_: int = 24
    _HASH_BYTE_SIZE_: int = 24

    @classmethod
    def md5_hash(self, target: str, use_salt: bool):
        """
        hash target with salt
        :param target:
        :param use_salt: is use salt to safe md5
        :return: md5info{salt,md5}
        """
        md5Info = Md5Info()
        if(use_salt):
            md5Info.Salt = os.urandom(self._SALT_BYTE_SIZE_)
        else:
            md5Info.Salt = b''
        # print(md5Info.Salt)
        md5Info.MD5 = hashlib.md5(md5Info.Salt + target.encode(encoding="UTF-8") + md5Info.Salt).hexdigest()
        return md5Info



# md51 = Helper.md5_hash("A3部队",True)
# md52 = Helper.md5_hash("A3部队",False)
# print(md51.MD5)
# print(md52.MD5)