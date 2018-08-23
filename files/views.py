import errno
from django.http import HttpResponse, Http404, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render, redirect, render_to_response
from .models import Directory
from pathlib import Path
from django.core.files import File
from pget.down import Downloader
from wsgiref.util import FileWrapper
from django.utils.encoding import smart_str
import requests
import mimetypes
from django.contrib import messages
# from .models import Files
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import CreateView
from django.template import RequestContext
from django.conf import settings
import os, tempfile
import pdb #python debugger
from django.core.files.storage import default_storage
from .forms import UploadFileForm, DirectoryForm
from django.views import generic
from django.contrib.sessions.models import Session
from django.template import loader
# Create your views here.

# pdb.set_trace()

# def homepage(request):
#     all_directories = Directory.objects.all()
#     html = ''
#     print(all_directories)
#     for directory in all_directories:
#         url = str(directory.id) + '/'
#         html += r'<a href="'+url+'">' + directory.dir_name + '</a><br>'
#
#     return HttpResponse(html)

# def homepage(request):
#     all_directories = Directory.objects.all()
#     template = loader.get_template('files/homepage.html')
#     context = {
#         'all_directories' : all_directories
#     }
#     return HttpResponse(template.render(context, request))


def homepage(request):
    all_directories = Directory.objects.all()
    context = {'all_directories': all_directories}
    return render(request, 'files/homepage.html', context)


# def detail(request, pk):
#     try:
#         directory = Directory.objects.get(pk=pk)
#     except Directory.DoesNotExist:
#         raise Http404("Album Does not Exist")
#
#     return render(request, 'files/detail.html', {'directory': directory})
#

def myfiles_page(request, pk):
    path = os.path.dirname(os.path.abspath(__file__))
    directory = Directory.objects.get(id=pk).dir_name
    # space_removed_dir = directory.replace(" ", "_")
    # real_path = 'media/' + space_removed_dir + '/media/'
    real_path = 'media/' + str(pk) + '/media/'
    myfiles = os.path.join(path, real_path)
    abc = 'g'
    if not os.path.exists(myfiles):
        os.makedirs(myfiles)

    os.chdir(myfiles)
    x = 0
    d = {}
    trimmed = {}
    size = {}
    for file in os.listdir("."):
        d[x] = file
        trimmed[x] = file
        size[x] = round(os.path.getsize(file)/(1024*1024), 2)
        x = x + 1

    variables = {'user': request.user, 'filedict': d, 'size': size, 'trimmed': trimmed, 'directory_name': directory}

    return render(request, 'files/detail.html', variables)


# class UploadFile(CreateView):
#     model = Files
#     fields = ['dir_name', 'file']
#
#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         return HttpResponseRedirect(reverse('homepage'))
#

def upload(request, pk):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], request, pk)
            return HttpResponseRedirect(reverse('detail', kwargs={'pk': pk}))
    else:
        form = UploadFileForm()
    return render(request, 'files/files_upload.html', {'form': form})


def handle_uploaded_file(file, request,pk):
    filename = file.name
    if not os.path.exists(filename):
        with open(filename, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
    else:
        messages.error(request, 'The file with same name already exists!! Please rename it or add another file')
        return HttpResponseRedirect(reverse('detail', kwargs={'pk': pk}))


def create_directory(request):

    form = DirectoryForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        directory = form.save(commit=False)
        directory.save()
        return render(request, 'files/detail.html', {'directory': directory})
    context = {
        "form": form,
    }
    return render(request, 'files/create_directory.html', context)


def download(request, pk, file_path):
    file_path = '/home/spygaurad/PycharmProjects/ShareHere/files/media/'+str(pk)+'/media/'+file_path
    new_file_name = Path(file_path).name
    # file_wrapper = FileWrapper(open(file_path, 'rb'))
    # file_mimetype = mimetypes.guess_type(file_path)
    # response = HttpResponse(file_wrapper, content_type=file_mimetype)
    # response['X-Sendfile'] = file_path
    # response['Content-Length'] = os.stat(file_path).st_size
    # response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(new_file_name)
    # return response

    the_file = file_path
    filename = new_file_name
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(the_file, 'rb'), chunk_size),
                                     content_type=mimetypes.guess_type(the_file)[0])
    response['Content-Length'] = os.path.getsize(the_file)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


def user_login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect(reverse('homepage'))
        else:
            context["error"] = "Provide valid Credentials"
            return render(request, "files/login.html", context)
    else:
        return render(request, "files/login.html", context)


def user_logout(request):

    if request.method == 'POST':
        logout(request)

        return redirect(reverse('homepage'))

    elif request.method == 'GET':
        logout(request)
        return redirect(reverse('homepage'))
