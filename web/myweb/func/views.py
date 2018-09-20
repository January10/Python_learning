from django.shortcuts import render
from django.http import HttpResponse
import os
from myweb.settings import BASE_DIR

auth = False


# Create your views here.
def login(request):
    global auth
    auth = False
    return render(request, 'login.html')


def login_post(request):
    global auth
    if auth:
        return render(request, 'home.html')
    elif request.method == 'POST':
        user = request.POST['user']
        passwd = request.POST['passwd']
        if str(user) == 'wzq' and str(passwd) == 'January10':
            auth = True
            return render(request, 'home.html')
        else:
            return render(request, 'login.html')


def home(request):
    if not auth:
        return render(request, 'login.html')
    else:
        return render(request, 'home.html')


def func(request):
    if not auth:
        return render(request, 'login.html')
    else:
        return render(request, 'func.html')


def upload(request):
    if not auth:
        return render(request, 'login.html')
    else:
        folder = '_upload'
        path = os.path.join(BASE_DIR, 'func', 'func', folder)
        uploads = os.listdir(path)
        data = ''.join(
            [str(x) + '、' + y + ' __' + '{0:.2f}'.format(
                os.path.getsize(os.path.join(path, y)) / 1024 / 1024) + 'MB' + '\n'
             for x, y in enumerate(uploads)])
        return render(request, 'upload.html', {'data': data})


def upload_post(request):
    if not auth:
        return render(request, 'login.html')
    else:
        if request.method == 'POST':
            files = request.FILES.getlist('old_input')
            if files:
                folder = '_upload'
                path = os.path.join(BASE_DIR, 'func', 'func', folder)
                if not os.path.exists(path):
                    os.makedirs(path)
                for file in files:
                    uploads = os.listdir(path)
                    if len(uploads) > 20:
                        return HttpResponse('Max length out,Please connect administrator!')
                    if file.size > 1024 * 1024 * 10:
                        return HttpResponse('Scale out,Please less than 10MB!')
                    with open(os.path.join(path, file.name), 'wb+') as f:
                        for chunk in file.chunks():
                            f.write(chunk)
                return HttpResponse('Upload success!')
            else:
                return HttpResponse('Please choose files upload!')
