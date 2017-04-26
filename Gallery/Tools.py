import os
import base64
import urllib.parse
import json
import random


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
    return urllib.parse.quote(content)


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
        if os.path.isfile(path + '/' + sub) and sub.startswith('.'):
            continue
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


def get_parent_folder(path):
    return os.path.abspath(os.path.join(path, os.pardir))


def jump_group(path, type):
    if type == '10' or type == '-10':
        parent = get_parent_folder(path)
        parent_name = os.path.basename(parent)
        root = get_parent_folder(parent)
        group_list = os.listdir(root)
        # sorted(group_list)
        index = 0
        for i in range(0, len(group_list)):
            if group_list[i] == parent_name:
                index = i
                break
        if type == "10":
            if index == len(group_list) - 1:
                index = 0
            else:
                index += 1
        else:
            if index == 0:
                index = len(group_list) - 1
            else:
                index -= 1
        print('group:' + str(index) + ' -' + group_list[index])
        return os.listdir(root + "/" + group_list[index]), root + "/" + group_list[index]
    else:
        print("type error")
        return [], ""


def opt_jump_photo(path, type, root):
    if type == '10' or type == '-10':
        # first one in next blok
        file_list, folder = jump_group(path, type)
        for tmp_file in file_list:
            if tmp_file.endswith('.jpg'):
                res_path = folder + '/' + tmp_file
                print(res_path)
                return {"name": os.path.basename(res_path), "path": url_encode(res_path)}
    elif type == '1' or type == '-1':
        file_name = os.path.basename(path)
        parent = get_parent_folder(path)
        sub_file_list_tmps = os.listdir(parent)
        sub_file_list = []
        for sub_file_list_tmp in sub_file_list_tmps:
            if sub_file_list_tmp.endswith('.jpg'):
                sub_file_list.append(sub_file_list_tmp)
        # sorted(sub_file_list)
        index = 0
        for i in range(0, len(sub_file_list)):
            if sub_file_list[i] == file_name:
                index = i
                break
        if type == '1':
            if index == len(sub_file_list) - 1:
                file_list_tmps, folder = jump_group(path, "10")
                file_list = []
                for file_list_tmp in file_list_tmps:
                    if file_list_tmp.endswith('.jpg'):
                        file_list.append(file_list_tmp)
                res_path = folder + '/' + file_list[0]
            else:
                res_path = parent + '/' + sub_file_list[index + 1]
        else:
            if index == 0:
                file_list_tmps, folder = jump_group(path, "-10")
                file_list = []
                for file_list_tmp in file_list_tmps:
                    if file_list_tmp.endswith('.jpg'):
                        file_list.append(file_list_tmp)
                res_path = folder + '/' + file_list[-1]
            else:
                res_path = parent + '/' + sub_file_list[index - 1]
        print(res_path)
        return {"name": os.path.basename(res_path), "path": url_encode(res_path)}

    elif type == '0':
        res_path = get_random(root)
        print(res_path)
        return {"name": os.path.basename(res_path), "path": url_encode(res_path)}
    else:
        print("unknow type")
        return None


def get_random(folder):
    sub_list = os.listdir(folder)
    pick_up = sub_list[random.randint(0, len(sub_list) - 1)]
    if os.path.isfile(folder + '/' + pick_up):
        if not str(pick_up).endswith('.jpg'):
            return get_random(folder)
        else:
            return folder + '/' + pick_up
    else:
        return get_random(folder + '/' + pick_up)


if __name__ == '__main__':
    # test = '/Users/lirui/Desktop/testPic2/movies/tag1/073ef62618a387a908d18776.jpg'
    # print(json.dumps(construct_data_structure_to_json_object('/Users/lirui/Desktop/testPic')))
    # print(json.dumps(get_js_tree_path('/Users/lirui/Desktop/testPic')))

    # opt_jump_photo(test, "0", '/Users/lirui/Desktop/testPic2')

    pass
