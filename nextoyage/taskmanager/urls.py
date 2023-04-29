from django.urls import path

from . import views
app_name = 'taskmanager'
urlpatterns = [
    path('', views.index, name='index'),
    path('done', views.done, name='done'),
    path('stats', views.stats, name='stats'),

]
