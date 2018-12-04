from django.conf.urls import url
from . import views

app_name='login'

urlpatterns = [
    url(r'^register',views.register,name='register'),
    url(r'^logout',views.logout,name='logout'),
    url(r'^repwd',views.repwd,name='repwd'),
    url(r'',views.login,name='login'),
]