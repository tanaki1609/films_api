"""
URL configuration for films_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from movies import views
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/films/test/', views.test_api_view),
    path('api/v1/films/', views.MovieListAPIView.as_view()),  # GET->list, POST->create
    path('api/v1/films/<int:id>/',
         views.movie_detail_api_view),  # GET->item, PUT->update, DELETE->destroy
    path('api/v1/users/register/', users_views.register_api_view),
    path('api/v1/users/login/', users_views.AuthAPIView.as_view()),
    path('api/v1/directors/', views.DirectorListAPIView.as_view()),
    path('api/v1/directors/<int:id>/', views.DirectorDetailAPIView.as_view()),
    path('api/v1/genres/', views.GenreAPIViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('api/v1/genres/<int:id>/',
         views.GenreAPIViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}))
]
