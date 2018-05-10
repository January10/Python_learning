from django.contrib import admin
from .models import BookInfo, HeroInfo


# Register your models here.
class HeroInfoInline(admin.TabularInline):
    model = HeroInfo
    extra = 2


class BookInfoAdmin(admin.ModelAdmin):
    list_display = ['pk', 'btitle', 'bpub_date']
    list_filter = ['btitle']
    list_per_page = 10
    search_fields = ['btitle']

    inlines = [HeroInfoInline]


admin.site.register(BookInfo, BookInfoAdmin)
