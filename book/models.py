from django.db import models


# 定义图书模型类BookInfo
class BookInfo(models.Model):
    btitle = models.CharField(max_length=20, verbose_name='名称')
    bpub_date = models.DateField(verbose_name='发布日期')
    bread = models.IntegerField(default=0, verbose_name='阅读量')
    bcomment = models.IntegerField(default=0, verbose_name='评论量')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')
    # 如果模型已经迁移建表,并且表中已经有数据了,那么后添加的新字段必须可以为空或给了默认值,不然迁移报错
    # upload_to 表示上传的图片文件存储到MEDIA_ROOT指定目录中的book
    image = models.ImageField(verbose_name='图书', null=True, upload_to='book')

    class Meta:
        db_table = 'tb_books'  # 指明数据库表名
        verbose_name = '图书'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.btitle

    def bpub_date_format(self):
        return self.bpub_date.strftime('%Y-%m-%d')

    bpub_date_format.short_description = '发布日期'  # 修改方法名在列表页展示的成中文
    bpub_date_format.admin_order_field = 'bpub_date'  # 此方法中的数据依据模型的那个字段进行排序


# 定义英雄模型类HeroInfo
class HeroInfo(models.Model):
    GENDER_CHOICES = (
        (0, 'female'),
        (1, 'male')
    )
    hname = models.CharField(max_length=20, verbose_name='名称')
    hgender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name='性别')
    hcomment = models.CharField(max_length=200, null=True, verbose_name='描述信息')
    hbook = models.ForeignKey(BookInfo, on_delete=models.CASCADE, verbose_name='图书')  # 外键
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_heros'
        verbose_name = '英雄'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.hname

    def read(self):
        return self.hbook.bread

    read.short_description = '阅读量'
    read.admin_order_field = 'hbook__bread'
