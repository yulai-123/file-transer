from django.shortcuts import render
from main.models import File
from django.http import JsonResponse, StreamingHttpResponse
from django.core.serializers import serialize
import json
import os
from django.db import models

# Create your views here.

def index(request):
    return render(request, 'main/index.html', {})

def list(request):
    queryset = File.objects.all()
    instances = serialize(format="json", queryset=queryset)
    instances = json.loads(instances)
    data = {'instances': instances,}
    return JsonResponse(data)

def test(request):
    for i in range(2, 10):
        name = "test" + str(i) + ".txt"
        size = 1024
        path = "storage/" + name
        File.objects.create(name=name, size=size, path=path)
        print(name)
    return JsonResponse({"good": "good"})



def down(request, pk):
        model = File.objects.get(pk=pk)
        path = model.path
        file_name = model.name
        def down_iterator(path, chunk_size=1024):
            with open(path, 'rb') as f:
                while True:
                    e = f.read(chunk_size)
                    if e:
                        yield e
                    else:
                        break
        
        response = StreamingHttpResponse(down_iterator(path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)

        return response

def up(request):
    myfile = request.FILES.get("file", None)
    if not myfile:
        return JsonResponse({"data": "No file!"})
    print(myfile.name)
    print(myfile.size)

    path = 'storage/' + myfile.name
    with open(path, 'wb') as f:
        for chunk in myfile.chunks():
            f.write(chunk)
    
    File.objects.create(name=myfile.name, size=myfile.size, path=path)

    return JsonResponse({"data": "good!"})

    
def remove(request, pk):
    try:
        f = File.objects.get(pk=pk)
    except models.ObjectDoesNotExist:
        return JsonResponse({"data": "already delete!"})
    print(f.name)
    f.delete()
    path = f.path
    if os.path.exists(path):
        os.remove(path)
        result = "good!"
    else:
        result = "error!"
    return JsonResponse({"data": result})