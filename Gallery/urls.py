from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^getImage', views.get_image, name='get_image'),
    url(r'^editPhotoGallery', views.edit_photo_gallery, name='edit_photo_gallery'),
]
