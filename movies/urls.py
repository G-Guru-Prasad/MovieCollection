# myapp/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import html_render

# router = DefaultRouter()
# router.register(r'movies', MovieViewSet)
# router.register(r'collections', CollectionViewSet)
# router = DefaultRouter()
# router.register(r'collections', CollectionViewSet)

urlpatterns = [
    # path('', include(router.urls)),  # Include router URLs
    path('', html_render, name='home'),
]
