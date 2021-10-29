from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .models import AdminUsers
from .detector import machine
import datetime as dt
import json
from random import choice
import shutil
import os
from django.conf import settings

machine = machine()

def home(request):
    return render(request, 'index.html')
def add(request):
    if request.method == 'GET':
        return render(request, 'add.html')
    elif request.method == 'POST':
        if request.is_ajax():
            name = request.POST.get('name')
            image = request.FILES.get('image')
            datetime= dt.datetime.now().strftime('%Y-%m-%d')
            print(datetime)
            image_new = AdminUsers(name=name,pub_date=datetime, image=image)
            image_new.save()
            # print(name,image.chunks())
            return JsonResponse({'hello':'hi'})
        else:
            return JsonResponse({'hello':'Some error occurs'})
def getAdmins(request):
    if request.method == 'GET':
        if request.is_ajax():
            users = AdminUsers.objects.all()
            lst = [i.__dict__ for i in users]
            lst2 = [{'post_id':i['post_id'],'name':i['name'],'image':i['image']} for i in lst]
            return JsonResponse({'admins':json.dumps(lst2)})
def deleteAdmin(request):
    if request.method == 'POST':
        if request.is_ajax():
            id = request.POST.get('id',None)
            if id!= None:
                report=AdminUsers.objects.filter(post_id=id).delete()
                print(report)
                return JsonResponse({'success':'true'})
            else:
                return JsonResponse({'success':'false'})

def updateAdmin(request):
    if request.method == 'POST':
        if request.is_ajax():
            id = request.POST.get('id',None)
            name = request.POST.get('name',None)
            image = request.FILES.get('image')
            if id!= None:
                # report=AdminUsers.objects.filter(post_id=id)
                print(id,name)
                return JsonResponse({'success':'true'})
            else:
                return JsonResponse({'success':'false'})
def doorStart(request):
    if request.method == 'GET':
        if request.is_ajax():
            machine.start()
            return JsonResponse({'response':'success'})
def doorStop(request):
    if request.method == 'GET':
        if request.is_ajax():
            machine.stop()
            return JsonResponse({'response':'success'})
def doorStatus(request):
    if request.method == 'GET':
        if request.is_ajax():
            return JsonResponse({'door':machine.door,'lastseen':machine.lastSeen})

def calibrate(request):
    if request.method == 'GET':
        if request.is_ajax():
            users = AdminUsers.objects.all()
            rootPath = os.path.join(settings.MEDIA_ROOT,'known_faces')
            if os.path.exists(rootPath):
                shutil.rmtree(rootPath)
            os.makedirs(rootPath)
            for i in users:
                tempSource =os.path.join(settings.MEDIA_ROOT,i.image.name)
                tempDest =os.path.join(rootPath,i.name)
                tempFile = os.path.join(tempDest,'1.jpg')
                os.mkdir(tempDest)
                if os.path.exists(tempFile):
                    os.remove(os.path.join(tempFile))
                shutil.copy(tempSource, tempDest)
            return JsonResponse({'response':'success'})