from django.contrib import admin
from django.urls import path, include  # include impoted to impoer urls in files page
from django.conf import settings
from files import views
urlpatterns = [

    path(r'', views.homepage, name="homepage"),
    # path(r'<int:pk>/', views.detail, name="detail"),
    path(r'<int:pk>/', views.myfiles_page, name="detail"),
    path(r'create_directory/', views.create_directory, name="create_directory"),
    #path(r'<int:pk>/upload/', views.UploadFile.as_view(), name="upload"),
    path(r'<int:pk>/upload/', views.upload, name='upload'),
    path(r'<int:pk>/<str:file_path>/', views.download, name='download'),
    path(r'login/', views.user_login, name="login"),
    path(r'logout/', views.user_logout, name="logout"),
    # path(r'<int:pk>/add')

]