from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponseServerError
from django.http import JsonResponse

import YtinreteDjangoGallery.configs
from PIL import Image
from . import Tools
import os


# Create your views here.

def index(request):
    return render(request, 'Gallery/index.html')


def index2(request):
    ctx = {}
    data_list = []

    try:
        if request.GET.get('path'):
            path = Tools.url_decode(request.GET.get('path'))
            print(path)
        else:
            path = '/Users/lirui/Desktop'

        if path != '/':
            back_block = {}
            back_block['enter'] = '?path=' + Tools.url_encode(os.path.abspath(os.path.join(path, os.pardir)))
            back_block['name'] = '上层'
            back_block['path'] = path
            data_list.append(back_block)

        for file_name in os.listdir(path):
            block = {}
            full_path = os.path.abspath(os.path.join(path, file_name))
            block['path'] = full_path
            print('full_path:' + full_path)

            if Tools.is_image_file(file_name):
                block['img'] = 'getImage?path=' + Tools.url_encode(full_path)
            if os.path.isdir(full_path):
                block['name'] = '文件夹:' + file_name
                block['enter'] = '?path=' + Tools.url_encode(full_path)
                print('enter:' + block['enter'])
            else:
                block['name'] = '文件:' + file_name
            data_list.append(block)

        ctx['data_list'] = data_list
        return render(request, 'Gallery/index2.html', ctx)
    except IOError:
        return HttpResponseServerError('无法访问当前文件夹,请返回')
    except BaseException as e:
        print('error:' + str(e))
        return HttpResponseServerError()


def get_image(request):
    try:
        if request.GET.get('path'):
            path = Tools.url_decode(request.GET.get('path'))
            print(path)
        else:
            raise FileNotFoundError()
        with open(path, "rb") as f:
            response = HttpResponse(f.read(), content_type="image/jpeg")
            response['Cache-Control'] = 'no-cache'
            return response
    except IOError:
        red = Image.new('RGBA', (300, 300), (255, 0, 0, 0))
        response = HttpResponse(content_type="image/jpeg")
        response['Cache-Control'] = 'no-cache'
        red.save(response, "JPEG")
        return response


def gallery_photo(request):
    return render(request, 'Gallery/gallery_photo.html')


def get_js_tree_path(request):
    try:
        if request.GET.get('path'):
            path = Tools.url_decode(request.GET.get('path'))
            print(path)
        else:
            path = YtinreteDjangoGallery.configs.PHOTO_DIST_PATH
        return JsonResponse(Tools.get_js_tree_path(path), safe=False)
    except IOError:
        return HttpResponseServerError()


def search_photo(request):
    try:
        data = request.GET.get('data')
        if data:
            res = []
            print(data)
            for root, dirs, files in os.walk(YtinreteDjangoGallery.configs.PHOTO_SEARCH_PATH):
                for name in files:
                    if name.find('.') != -1 and name.split('.')[-1] == "jpg" and name.find(data) != -1:
                        block = {}
                        block['name'] = name
                        block['path'] = Tools.url_encode(root + '/' + name)
                        res.append(block)
            return JsonResponse(res, safe=False)
        else:
            return HttpResponseNotFound()

    except IOError:
        return HttpResponseServerError()


def jump_photo(request):
    try:
        if not request.GET.get('path') or request.GET.get('path') == "":
            path = Tools.get_random(YtinreteDjangoGallery.configs.PHOTO_DIST_PATH)
        else:
            path = Tools.url_decode(request.GET.get('path'))
        type = request.GET.get('type')
        print(path)
        if path and type and os.path.exists(path) and os.path.isfile(path):
            print(path)
            print(type)
            res = Tools.opt_jump_photo(path, type, YtinreteDjangoGallery.configs.PHOTO_DIST_PATH)
            if res:
                return JsonResponse(res, safe=False)
            else:
                return HttpResponseNotFound()
        else:
            return HttpResponseNotFound()
    except IOError:
        return HttpResponseServerError()
