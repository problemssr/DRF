from rest_framework import serializers

from .models import BookInfo


class BookInfoSerializer(serializers.Serializer):
    """书籍的序列化器"""
    id = serializers.IntegerField(label='ID', read_only=True)
    btitle = serializers.CharField(max_length=20, label='名称', required=True)
    bpub_date = serializers.DateField(label='发布日期')
    bread = serializers.IntegerField(label='阅读量', required=False)
    bcomment = serializers.IntegerField(label='评论量', required=False)
    is_delete = serializers.BooleanField(label='逻辑删除', required=False)


"""
book 模型中有7个属性
book.aa = 10
{8个key: value}
BookInfoSerializer(instace, data)
如果直给instace 形参传递参数表示做序列化
serializer = BookInfoSerializer(instace = book)
serializer.data  获取到序列化后的数据
"""


class HeroInfoSerializer(serializers.Serializer):
    """英雄数据序列化器"""
    GENDER_CHOICES = (
        (0, 'female'),
        (1, 'male')
    )

    id = serializers.IntegerField(label='ID', read_only=True)
    hname = serializers.CharField(label='名字', max_length=20)
    hgender = serializers.ChoiceField(choices=GENDER_CHOICES, label='性别', required=False)
    hcomment = serializers.CharField(label='描述信息', max_length=200, required=False, allow_null=True)
    # hbook = serializers.PrimaryKeyRelatedField(label='书籍', read_only=True)  # 默认是将关联模型的id序列化
    # hbook = serializers.StringRelatedField(label='书籍', read_only=True)  # 默认是将关联模型的__str__方法返回值序列化出来
    # hbook = BookInfoSerializer()  # 关联模型对象的序列化器中所有字段序列化出来
    # hbook = serializers.PrimaryKeyRelatedField(label='书籍', queryset=BookInfo.objects.all())


class BookInfoModelSerializer(serializers.ModelSerializer):
    """图书数据序列化器"""

    class Meta:
        model = BookInfo
        fields = '__all__'
