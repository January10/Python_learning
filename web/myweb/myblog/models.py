from django.db import models
from django.utils import timezone


# Create your models here.
class Blog(models.Model):
    description = models.CharField(default='描述', max_length=100)
    title = models.CharField(default='标题', max_length=100)
    date = models.DateTimeField('SaveTime', default=timezone.now)
    image = models.ImageField(default='default.png', upload_to='images/')
    body = models.TextField(default='正文')

    def __str__(self):
        return self.title
