import os
import base64
import urllib.parse

def list_sub_files(path):
    for file_name in os.listdir(path):
        full_path = os.path.join(path, file_name)
        stat_info = os.stat(full_path)
        print(full_path + ' size:' + convert_bytes(stat_info.st_size) + ' isFolder:' + str(os.path.isdir(full_path)))


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def is_image_file(file_name):
    if file_name:
        return file_name.endswith('.png') or file_name.endswith('.jpg') or file_name.endswith(
            '.jpes') or file_name.endswith('.gif') or file_name.endswith('.bmp')
    else:
        return False


def base64_encode(todo_str):
    return str(base64.b64encode(
        bytes(os.path.abspath(os.path.join(todo_str, os.pardir)), encoding='utf-8')), encoding='utf-8')


def base64_decode(todo_str):
    str(base64.b64decode(bytes(todo_str, encoding='utf-8')), encoding='utf-8')

def url_encode(content):
    return urllib.parse.quote_plus(content)


def url_decode(content):
    return urllib.parse.unquote(content)