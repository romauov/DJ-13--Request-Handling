import datetime
from django.http import HttpResponse
from django.shortcuts import render
import os
from django.conf import settings


def file_list(request, date=None):
    template_name = 'index.html'
    my_path = settings.FILES_PATH

    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    files = os.listdir(my_path)
    files_content = [{'name': file,
             'ctime': datetime.datetime.fromtimestamp(os.stat(os.path.abspath(f'{my_path}\{file}')).st_ctime), #эту монструозную конструкцию можно как-то упростить?
             'mtime': datetime.datetime.fromtimestamp(os.stat(os.path.abspath(f'{my_path}\{file}')).st_mtime)} for file in files]

    context = {
        'files': files_content,
        'date': date  # Этот параметр необязательный
    }

    return render(request, template_name, context)


def file_content(request, file_name):

    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    file_path = os.path.abspath(f'files\{file_name}')
    with open(file_path) as f:
        f_content = f.read()

    return render(
        request,
        'file_content.html',
        context={'file_name': file_name, 'file_content': f_content}
    )

