from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^postThread', views.post_thread, name='postThread'),
    url(r'^getImage', views.get_image, name='get_image'),
]