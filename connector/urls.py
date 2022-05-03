
from client_talent_connector import settings
from django.urls import path
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('',views.register),
    path('home/',views.home,name='home'),
    path('your-name/',views.upload,name='your-name'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    