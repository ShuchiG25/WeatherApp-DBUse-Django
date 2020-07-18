import urllib

import requests
from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from .forms import CityForm
from .models import City


def weather(request):
     #  Displaying cities data stored in DB
    url ="http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=4cd80c1d9a852e8b859c4a09146c78b0"

    if request.method=='POST':
        form=CityForm(request.POST)
        # to check duplicate city in DB
        if form.is_valid():
            new_city=form.cleaned_data['name']
            existing_city_count=City.objects.filter(name=new_city).count()
            if existing_city_count==0:
                #to check if API returns correct value
                information = requests.get(url.format(new_city)).json()
                # if information.get('cod', 0) != "404": or
                if information['cod']==200:
                    form.save()
                else:
                    messages.warning(request, "City does not exist. Kindly check the spelling !!")
            else:
                messages.warning(request,"City already exists !!")

    form=CityForm()

    cities =City.objects.all()

    weather_data=[]
    for item in cities:
        information = requests.get(url.format(item)).json()

        city_weather = {
            'city': item.name,
            'temperature': information["main"]["temp"],
            'description': information["weather"][0]["description"],
            'icon': information["weather"][0]["icon"],
        }
        weather_data.append(city_weather)

    print("city_weather..................... -", weather_data)
    context = {'weather_data': weather_data, 'form':form}
    return render(request, 'weather.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect("weather")