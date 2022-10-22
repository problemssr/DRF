"""
GET     /books/         提供所有记录
POST    /books/         新增一条记录
GET     /books/<pk>/    提供指定id的记录
PUT     /books/<pk>/    修改指定id的记录
DELETE  /books/<pk>/    删除指定id的记录

APIView  序列化器
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.viewsets import ViewSet, GenericViewSet, ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import action

from .models import BookInfo
from .serializers import BookInfoModelSerializer

"""以下是继承APIView的视图"""


class BookListAPIView(APIView):
    """列表视图"""

    def get(self, request):
        """查询所有"""
        qs = BookInfo.objects.all()
        serializer = BookInfoModelSerializer(instance=qs, many=True)
        print(serializer.data)
        response = Response(serializer.data)
        print(response.data)  # 响应对象未渲染处理的数据
        # print(response.content)  # 处理后要响应给前端的数据
        return response
        # return Response(serializer.data)

    def post(self, request):
        """新增"""
        # 获取前端传入的请求体数据
        data = request.data
        # 创建序列化器进行反序列化
        serializer = BookInfoModelSerializer(data=data)
        # 调用序列化器的is_valid方法进行校验
        serializer.is_valid(raise_exception=True)
        # 调用序列化器的save方法进行执行create方法
        serializer.save()
        # 响应
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookDetailAPIView(APIView):
    """详情视图"""

    def get(self, request, pk):
        # 查询pk指定的模型对象
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 创建序列化器进行序列化
        serializer = BookInfoModelSerializer(instance=book)
        # 响应
        return Response(serializer.data)

    def put(self, request, pk):
        # 查询pk所指定的模型对象
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 获取前端传入的请求体数据
        # 创建序列化器进行反序列化
        serializer = BookInfoModelSerializer(instance=book, data=request.data)
        # 校验
        serializer.is_valid(raise_exception=True)
        # save--->update
        serializer.save()
        # 响应
        return Response(serializer.data)

    def delete(self, request, pk):
        # 查询pk所指定的模型对象
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
