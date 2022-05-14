from calendar import month
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib import messages
import geocoder
from .models import garbageLog
from datetime import datetime
from dateutil.relativedelta import *
from django.db.models import Sum, Avg
import io
import matplotlib
import base64, urllib
matplotlib.use('Agg')
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from django.db.models.functions import TruncMonth
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
    ).order_by('-eventID')
    return render(request, 'records.html', {
        'filteredList': filteredList
    })

def efficiency(request):
    dataCount = garbageLog.objects.all().count()
    dataTotal = garbageLog.objects.aggregate(Sum('ratio'))
    dataTotal = dataTotal['ratio__sum']

    if dataTotal is None:
        dataAverage = 0
    else:
        dataAverage = round((dataTotal / dataCount) *100)
    
    
    today = datetime.today()
    beforeSixMonths = today + relativedelta(months=-5)
    beforeSixMonths = beforeSixMonths.replace(day=1)
    print(today)

    months = {
        '1': 'Ocak',
        '2': 'Şubat',
        '3': 'Mart',
        '4': 'Nisan',
        '5': 'Mayıs',
        '6': 'Haziran',
        '7': 'Temmuz',
        '8': 'Ağustos',
        '9': 'Eylül',
        '10': 'Ekim',
        '11': 'Kasım',
        '12': 'Aralık'
    }

    graph = garbageLog.objects.annotate(
    month=TruncMonth('creationDate')).filter(
        creationDate__range=[beforeSixMonths, today]
    ).values('month').annotate(totalOfMonth=Avg('ratio')).order_by('month')

    print(month)
    
    lastSixTotals = []
    for i in graph:
        lastSixTotals.append(i['totalOfMonth'])
        if i is None:
            print()


    #key-value yap. boş olan ayı bul ve orayı 0 yap
    xAxisGraph = []
    xAxisGraph.append(beforeSixMonths.month)

    for i in xAxisGraph:
        if len(xAxisGraph) > 5:
            break
        elif i == 12:
            i -= 11
            xAxisGraph.append(i)
        else:
            i += 1
            xAxisGraph.append(i)

    if len(lastSixTotals) < len(xAxisGraph):
        for i in lastSixTotals:
            if i <= 0:
                print('burada değil')
            else:
                lastSixTotals.append(0)

    figure : Figure = plt.figure()
    ax = figure.add_subplot(111)
    xAxisGraph = list(map(str, xAxisGraph))
    xAxisGraph = [months.get(e, e) for e in xAxisGraph]
    addlabels(xAxisGraph, lastSixTotals)
    ax.bar(xAxisGraph, lastSixTotals, color="#98C1FF")
    ax.get_yaxis().set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.plot()
    url = get_image_url(figure)
    plt.close()

    return render(request, 'efficiency.html', {
        'dataCount': dataCount,
        'dataAverage': dataAverage,
        'image': url
        })

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

# def update(request, eventID):
#     if request.method == "POST":
#         eventID = request.POST.get('eventID')
#         creationDate = request.POST.get('creationDate')
#         ratio = request.POST.get('ratio')

#         updated = garbageLog(
#             eventID = eventID,
#             creationDate = creationDate,
#             ratio = ratio
#         )
#         updated.save()
#         return redirect('kayitlar')

#     return redirect(request, 'records.html')

def delete(request, eventID):
    deleteRecord = garbageLog.objects.filter(eventID = eventID)
    deleteRecord.delete()
    context = {
        'deleteRecord': deleteRecord
    }
    return redirect('kayitlar')

def get_image_url(figure:Figure):
    buffer = io.BytesIO()
    figure.savefig(buffer,format='png')
    buffer.seek(0)
    value = base64.b64encode(buffer.read())
    url = urllib.parse.quote(value)
    return url

def addlabels(x,y):
    for i in range(len(x)):
        dataLabel = f'{y[i]:,}%'
        plt.text(i, y[i]*1.03, dataLabel.format(dataLabel).replace(',', '.'),
        ha = 'center',
        c = 'black', 
        fontweight = 400,
        fontfamily = 'roboto',
        fontsize = 10.5
    )