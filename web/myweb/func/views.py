from django.shortcuts import render
from django.http import HttpResponse
from django.http import StreamingHttpResponse
import os
import zipfile
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
        uploads_str = ''.join([x + '\n' for x in uploads if os.path.isfile(os.path.join(path, x))])
        return render(request, 'upload.html', {'data': data, 'uploads_str': uploads_str})


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

        if request.method == 'GET':
            files = request.GET['text2']
            if files:
                folder = '_upload'
                path = os.path.join(BASE_DIR, 'func', 'func', folder)
                file_list = files.split('\r')
                file_lis = [x for x in file_list if x.strip('\n')]
                f = zipfile.ZipFile(os.path.join(BASE_DIR, 'func', 'func', 'download.zip'), 'w', zipfile.ZIP_DEFLATED)
                for ff in file_lis:
                    f.write(os.path.join(path, ff), ff)
                f.close()
                download = open(os.path.join(BASE_DIR, 'func', 'func', 'download.zip'), 'rb')
                response = StreamingHttpResponse(download)
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename="download.zip"'
                return response
            else:
                return HttpResponse('Download error!')
