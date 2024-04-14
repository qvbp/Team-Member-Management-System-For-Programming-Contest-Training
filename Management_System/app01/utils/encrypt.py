from django.conf import settings
import hashlib


def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8')) # django 中自己随机生成的字符串
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()