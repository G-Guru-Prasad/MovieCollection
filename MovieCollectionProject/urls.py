"""
URL configuration for MovieCollectionProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.urls import re_path as url
from movies.views import RegisterUser, RequestCount, ResetRequestCount
from movies.movie_collection_views import GetMovies, CollectionViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movies.urls')),
    path('api-auth/', include('rest_framework.urls')),

    url(r'^movies/', GetMovies.as_view(), name='movies'),
    url(r'^register/', RegisterUser.as_view(), name='register'),
    path('request-count/', RequestCount.as_view(), name='request-count'),
    path('request-count/reset/', ResetRequestCount.as_view(), name='request-count-reset'),
    path('collection/', CollectionViewSet.as_view(), name='collection'), # can also use CollectionViewSet.as_view({"put":"updateCollection"})
    path('collection/<uuid:collection_uuid>/', CollectionViewSet.as_view(), name='collection'),
]

