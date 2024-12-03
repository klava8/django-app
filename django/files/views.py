from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from .models import UploadedFile
from .forms import UploadFileForm

from django.views.decorators.csrf import csrf_exempt
import os


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            if not uploaded_file.file_type:
                uploaded_file.file_type = uploaded_file.file.name.split('.')[-1]
                uploaded_file.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error'})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

@csrf_exempt
def upload_chunk(request):
    if request.method == 'POST':
        chunk = request.FILES.get('chunk')
        chunk_number = request.POST.get('chunk_number')
        total_chunks = request.POST.get('total_chunks')
        file_name = request.POST.get('file_name')

        # Проверяем, что все необходимые параметры переданы
        if not chunk or not chunk_number or not total_chunks or not file_name:
            return JsonResponse({'status': 'error', 'message': 'Missing required parameters'})

        chunk_number = int(chunk_number)
        total_chunks = int(total_chunks)

        # Создаем директорию для временных файлов, если она не существует
        temp_dir = os.path.join('media', 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Сохраняем пакет файла
        with open(os.path.join(temp_dir, f'{file_name}.part{chunk_number}'), 'wb+') as destination:
            for chunk in chunk.chunks():
                destination.write(chunk)

        # Если это последний пакет, объединяем все пакеты в один файл
        if chunk_number == total_chunks:
            with open(os.path.join('media', file_name), 'wb+') as destination:
                for i in range(1, total_chunks + 1):
                    chunk_path = os.path.join(temp_dir, f'{file_name}.part{i}')
                    with open(chunk_path, 'rb') as chunk_file:
                        destination.write(chunk_file.read())
                    os.remove(chunk_path)

            # Сохраняем файл в базу данных
            uploaded_file = UploadedFile(file=file_name)
            uploaded_file.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


def index(request):
    sort_by = request.GET.get('sort_by', 'uploaded_at')  # По умолчанию сортировка по времени загрузки
    sort_order = request.GET.get('sort_order', 'desc')  # По умолчанию сортировка по убыванию

    if sort_order == 'asc':
        sort_order_prefix = ''
    else:
        sort_order_prefix = '-'
    file_objects = UploadedFile.objects.all().order_by(f'{sort_order_prefix}{sort_by}')

    return render(request, 'index.html', {'file_objects': file_objects, 'sort_by': sort_by, 'sort_order': sort_order})

def download_file(request, file_id):
    file_obj = get_object_or_404(UploadedFile, id=file_id)
    file_obj.increment_download_count()
    response = FileResponse(file_obj.file, as_attachment=True)
    return response

def delete_file(request, file_id):
    file_obj = get_object_or_404(UploadedFile, id=file_id)
    file_obj.delete()
    return redirect('index')