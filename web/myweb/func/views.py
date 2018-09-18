from django.shortcuts import render
from django.http import HttpResponse
import os
from myweb.settings import BASE_DIR


# Create your views here.
def home(request):
    return render(request, 'home.html')


def func(request):
    return render(request, 'func.html')


def upload(request):
    folder = '_upload'
    path = os.path.join(BASE_DIR, 'func', 'func', folder)
    uploads = os.listdir(path)
    data = ''.join([str(x) + '、' + y + '\n' for x, y in enumerate(uploads)])
    return render(request, 'upload.html', {'data': data})


def upload_post(request):
    if request.method == 'POST':
        files = request.FILES.getlist('old_input')
        if files:
            folder = '_upload'
            path = os.path.join(BASE_DIR, 'func', 'func', folder)
            if not os.path.exists(path):
                os.makedirs(path)
            for file in files:
                with open(os.path.join(path, file.name), 'wb+') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
            return HttpResponse('Upload success!')
        else:
            return HttpResponse('Please choose files upload!')
