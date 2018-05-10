from django.db import models


# Create your models here.
class BookInfo(models.Model):
    btitle = models.CharField(max_length=20)
    bpub_date = models.DateTimeField()

    def __str__(self):
        return "%d" % self.pk


class HeroInfo(models.Model):
    hname = models.CharField(max_length=20)
    # hgender = models.BooleanField()
    gender_list = ((1, '男'), (2, '女'))
    hgender = models.IntegerField(choices=gender_list)
    hcontent = models.CharField(max_length=100)
    hBook = models.ForeignKey('BookInfo', on_delete=models.CASCADE)

    def __str__(self):
        return "%d" % self.pk
