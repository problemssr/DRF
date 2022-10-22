from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from . import views

urlpatterns = [
    # 列表视图的路由APIView
    path(r'books/', views.BookListAPIView.as_view()),
    # 详情视图的路由APIView
    path(r'books/<int:pk>/', views.BookDetailAPIView.as_view()),
    # 列表视图的路由GenericAPIView
    path('booksGeneric/', views.BookListGenericView.as_view()),
    # 详情视图的路由GenericAPIView
    path(r'booksGeneric/<int:pk>/', views.BookDetailGenericView.as_view()),
    # 列表视图的路由GenericAPIView
    path('booksGenericMixin/', views.BookListGenericMixinView.as_view()),
    # 详情视图的路由GenericAPIView
    path(r'booksGenericMixin/<int:pk>/', views.BookDetailGenericMixinView.as_view()),
    # ViewSet视图集指定路由
    # 列表视图的路由GenericAPIView
    path(r'booksViewSet/', views.BookViewSet.as_view({'get': 'list'})),
    # 详情视图的路由GenericAPIView
    path(r'booksViewSet/<int:pk>/', views.BookViewSet.as_view({'get': 'retrieve'})),

    # 如果在增删改查之外额外增加的行为 应该单独定义路由
    # 如果此行为不需要pk 那么它就是列表视图 但是列表视图默认只有list, create
    path(r'BookModelViewSet/latest/', views.BookModelViewSet.as_view({'get': 'latest'})),
    path(r'BookModelViewSet/<int:pk>/read/', views.BookModelViewSet.as_view({'put': 'read'})),
]
