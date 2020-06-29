from django.urls import path, include
from . import views

urlpatterns = [
    path(r'',views.music, name='music'),
    path(r'work', views.get_music, name='get')
]