from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from . import views

urlpatterns = [
    # 列表视图的路由APIView
    path(r'books/', views.BookListAPIView.as_view()),
    # 详情视图的路由APIView
    path(r'books/<int:pk>/', views.BookDetailAPIView.as_view()),
]
