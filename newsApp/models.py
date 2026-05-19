from django.db import models
import django.utils.timezone as timezone


class MyNew(models.Model):
    NEWS_CHOICES = (
        ('主线剧情', '主线剧情'),
        ('限时活动', '限时活动'),
        ('召唤公告', '召唤公告'),
    )

    title = models.CharField(max_length=50, verbose_name='新闻标题')
    description = models.TextField(verbose_name='内容', default='')
    newType = models.CharField(
        choices=NEWS_CHOICES,
        max_length=50,
        verbose_name='新闻类型'
    )
    publishDate = models.DateTimeField(
        max_length=20,
        default=timezone.now,
        verbose_name='发布时间'
    )
    views = models.PositiveIntegerField('浏览量', default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publishDate']
        verbose_name = "新闻"
        verbose_name_plural = verbose_name