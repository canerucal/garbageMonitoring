from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib import messages
#import RPi.GPIO as GPIO

# bu alana hesaplama gelecek, index fonksiyonunda simüle edildi. canlı çalışması için while döngüsü kurulmalı
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

def index(request):
    return render(request, 'index.html')

def get_ratio(request):
    binCapacity = 0
    distance = 19

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

    #debugging
    print("distance: ", distance)
    print("binCapacity: ", binCapacity)

    return render(request, 'partials/show.html', {
        'binCapacity': binCapacity
    })

def records(request):
    return render(request, 'records.html')

def efficiency(request):
    return render(request, 'efficiency.html')

def loginUser(request):
    return render(request, 'login.html')

def landing(request):
    return render(request, 'landing.html')