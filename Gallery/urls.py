from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^getImage', views.get_image, name='get_image'),
    url(r'^getJsTreePath', views.get_js_tree_path, name='get_js_tree_path'),
    url(r'^galleryPhoto', views.gallery_photo, name='gallery_photo'),
    url(r'^searchPhoto', views.search_photo, name='search_photo'),
]
