from django.conf.urls import url
from . import views

app_name='homepage'

urlpatterns = [
    url(r'^search',views.search,name='search'),
    url('',views.index,name='index'),
]