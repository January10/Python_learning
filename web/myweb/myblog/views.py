from django.shortcuts import render
from myblog.models import Blog


# Create your views here.
def home(request):
    blogs = Blog.objects
    image = '/media/images/t3.jpg'
    return render(request, 'home.html', {'blogs': blogs, 'image': image})
