import os
import base64
import urllib.parse
import json


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


def construct_data_structure_to_json_object(path):
    if not os.path.exists(path):
        return
    current_data = {}
    current_data['path'] = path
    current_data['name'] = path.split('/')[-1]
    if os.path.isfile(path):
        current_data['isFile'] = True
    else:
        current_data['isFile'] = False
        current_data['subFiles'] = []
        for sub in os.listdir(path):
            if sub.startswith('.'):
                continue
            sub_file = construct_data_structure_to_json_object(path + '/' + sub)
            if sub_file:
                current_data['subFiles'].append(sub_file)
    return current_data


def get_js_tree_path(path):
    json_data = []
    for sub in os.listdir(path):
        block = {}
        block['text'] = sub
        block['id'] = url_encode(path + '/' + sub)
        if os.path.isfile(path + '/' + sub):
            block['type'] = 'file'
        else:
            block['type'] = 'folder'
            if len(os.listdir(path + '/' + sub)) > 0:
                block['children'] = True
        json_data.append(block)
    return json_data


if __name__ == '__main__':
    # print(json.dumps(construct_data_structure_to_json_object('/Users/lirui/Desktop/testPic')))
    print(json.dumps(get_js_tree_path('/Users/lirui/Desktop/testPic')))
    pass
