from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib import messages
import geocoder
from .models import garbageLog
from datetime import datetime
from dateutil.relativedelta import *
#import RPi.GPIO as GPIO

# bu alana hesaplama gelecek, index fonksiyonunda simüle edildi.
# def distanceFunction():
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setwarnings(False)
    # TRIG = 23
    # ECHO = 24
    # GPIO.setup(TRIG,GPIO.OUT)
    # GPIO.setup(ECHO,GPIO.IN)
    # binCapacity = "Empty"
    # global val1
    # GPIO.output(TRIG, False)
    # time.sleep(2)

    # GPIO.output(TRIG, True)
    # time.sleep(0.00001)
    # GPIO.output(TRIG, False)
    # while GPIO.input(ECHO)==0:
    #     pulse_start = time.time()

    # while GPIO.input(ECHO)==1:
    #         pulse_end = time.time()

    # pulse_duration = pulse_end - pulse_start

    # distance = pulse_duration * 17150
    # distance = round(distance, 2)

def get_ratio(request):
    global binCapacity
    global distance
    binCapacity = 0
    distance = 50 #sensör verisi buraya gelecek.

    if distance >= 0:
        if 0 < distance <= 20:
            binCapacity = 100
        elif 20 < distance <= 50:
            binCapacity = 75
        elif 51 <= distance <= 80:
            binCapacity = 50
        elif 81 <= distance < 120:
            binCapacity = 25
        else:
            binCapacity = 0
    else:
        print('Distance must be over 0 !')
    global binCapacityPercentage
    binCapacityPercentage = binCapacity/100

    #debugging
    # print("distance: ", distance)
    # print("binCapacity: ", binCapacity)

    return render(request, 'partials/show.html', {
        'binCapacity': binCapacity,
        'binCapacityPercentage': binCapacityPercentage
    })

def AllRecords(request):
    filteredList = garbageLog.objects.filter(
    creationDate__range=[datetime.today() + relativedelta(weeks=-8), datetime.today()]
    ).order_by('-creationDate')
    return render(request, 'records.html', {
        'filteredList': filteredList
    })

def efficiency(request):
    return render(request, 'efficiency.html')

def loginUser(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Hoşgeldin"))
            return redirect('landing')
        else:
            messages.success(request, ("Kullanıcı adı veya şifre hatalı!"))
            return redirect('login')

    else:
        return render(request, 'login.html')

def landing(request):
    return render(request, 'landing.html')

def measurement(request):
    g = geocoder.ip('me')
    latitude = g.latlng[0]
    longitude = g.latlng[1]
    place = g[0]

    submitted = False
    if request.method == "POST":            
        ratio = binCapacityPercentage
        form = garbageLog(ratio = ratio)
        if ratio == 0:
            messages.success(request, ("Çöp kutusu zaten boş !"))
            return HttpResponseRedirect('/measurement?submitted=False')
        else:
            form.save()
            return HttpResponseRedirect('/measurement?submitted=True')
    else:
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'measurement.html',{
        'latitude': latitude,
        'longitude' : longitude,
        'place': place,
        'submitted': submitted,
    })

def update(request, eventID):
    if request.method == "POST":
        eventID = request.POST.get('eventID')
        creationDate = request.POST.get('creationDate')
        ratio = request.POST.get('ratio')

        updated = garbageLog(
            eventID = eventID,
            creationDate = creationDate,
            ratio = ratio
        )
        updated.save()
        return redirect('kayitlar')

    return redirect(request, 'records.html')

def delete(request, eventID):
    deleteRecord = garbageLog.objects.filter(eventID = eventID)
    deleteRecord.delete()
    context = {
        'deleteRecord': deleteRecord
    }
    return redirect('kayitlar')