from django.urls import path
from .views import ImageListCreateView, ImageDetailView

urlpatterns = [
    path('images/', ImageListCreateView.as_view(), name='image-list'),
    path('images/<int:pk>/', ImageDetailView.as_view(), name='image-detail'),
]