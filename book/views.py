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
        # 获取前端传入的请求体数据
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
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


"""以下是继承GenericAPIView的视图"""


class BookListGenericView(GenericAPIView):
    """列表视图"""
    # 指定序列化器类
    serializer_class = BookInfoModelSerializer
    # 指定查询集'数据来源'
    queryset = BookInfo.objects.all()

    def get(self, request):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class BookDetailGenericView(GenericAPIView):
    """详情视图"""
    # 指定序列化器类
    serializer_class = BookInfoModelSerializer
    # 指定查询集'数据来源'
    queryset = BookInfo.objects.all()

    def get(self, request, pk):
        book = self.get_object()  # queryset.get(self.kwargs)
        serializer = self.get_serializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = self.get_object()
        serializer = self.get_serializer(book, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


"""以下是GenericAPIView和mixin的混合使用视图"""


class BookListGenericMixinView(CreateModelMixin, ListModelMixin, GenericAPIView):
    """列表视图"""
    # 指定序列化器类
    serializer_class = BookInfoModelSerializer
    # 指定查询集'数据来源'
    queryset = BookInfo.objects.all()

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class BookDetailGenericMixinView(UpdateModelMixin, RetrieveModelMixin, GenericAPIView):
    """详情视图"""
    # 指定序列化器类
    serializer_class = BookInfoModelSerializer
    # 指定查询集'数据来源'
    queryset = BookInfo.objects.all()

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)


"""以下是GenericAPIView和Mixin合成的子类视图"""
# class BookListGenericView(ListCreateAPIView):
#     """列表视图"""
#     # 指定序列化器类
#     serializer_class = BookInfoModelSerializer
#     # 指定查询集'数据来源'
#     queryset = BookInfo.objects.all()
#
#
# class BookDetailGenericView(RetrieveUpdateDestroyAPIView):
#     """详情视图"""
#     # 指定序列化器类
#     serializer_class = BookInfoModelSerializer
#     # 指定查询集'数据来源'
#     queryset = BookInfo.objects.all()

"""以下是APIView的视图集"""


class BookViewSet(ViewSet):
    """视图集"""

    def list(self, request):
        qs = BookInfo.objects.all()
        serializer = BookInfoModelSerializer(qs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BookInfoModelSerializer(book)
        return Response(serializer.data)

"""以下是GenericAPIView的视图集"""
# class BookViewSet(GenericViewSet):
# class BookViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
# class BookViewSet(ReadOnlyModelViewSet):
class BookModelViewSet(ModelViewSet):
    """视图集"""
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoModelSerializer

    # def list(self, request):
    #     qs = self.get_queryset()
    #     serializer = self.get_serializer(qs, many=True)
    #     return Response(serializer.data)

    # 查询最后一本书  books/latest/  get:latest
    @action(methods=['get'], detail=False)
    # @action(methods=[指定下面的行为接收什么请求], detail=是不是详情视图如果是不详情视图就是 books/latest)
    def latest(self, request):
        """
        返回最新的图书信息
        """
        book = BookInfo.objects.latest('id')  # 获取最后一本书
        serializer = self.get_serializer(book)
        return Response(serializer.data)

    # books/pk/read/
    @action(methods=['put'], detail=True)
    def read(self, request, pk):
        """
        修改图书的阅读量数据
        """
        book = self.get_object()
        book.bread = request.data.get('bread')
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data)
