from django.shortcuts import render, redirect
from WeatherApp import main
from .forms import SearchCityForm, ChangePreferenceForm
from .models import City, Pref
from django.http import response
from django.contrib import messages
import string




def home(request): ##todo add in more data variables to the dictionary hourly_weather

    max_wind = Pref.objects.last().max_wind
    min_temp = Pref.objects.last().min_temp




    def good_to_fly(i, max_wind, min_temp):
        why = []
        if i.temp > min_temp and (i.wind_speed < max_wind) and i.dark == False and i.main != 'Rain' and i.main != 'Snow':
            return '', True

        else:
            if i.temp < min_temp:
                why.append('Too Cold,')

            if i.wind_speed > max_wind:
                why.append('Too Windy,')

            if i.dark == True:
                why.append('Too Dark,')

            if i.main == 'Rain':
                why.append("It's Raining")

            if i.main == 'Snow':
                why.append("It's Snowing")

            if len(why) == 0:
                why = ''
            else:
                why = ' '.join(why).strip(',')
            return why, False

##### FORM STUFF ##########################

    if request.method == 'POST' and 'city' in request.POST:
        city_form = SearchCityForm(request.POST)
        if city_form.is_valid():
            city = request.POST.get('city')
            if city == '':
                city = City.objects.last().city
            c = City(city=city)
            d = City.objects.last()
            d.delete()
            c.save()
            initial_data = main.General(city)
            if initial_data.fail == True:
                messages.warning(request, f'The city you searched for could not be found. Please check your spelling')
                return response.HttpResponseRedirect('/')

            return response.HttpResponseRedirect('/')
        else:
            last_search = City.objects.last().city
            initial_data = main.General(last_search)

    else:
        city_form = SearchCityForm()
        last_search = City.objects.last().city
        initial_data = main.General(last_search)


    if request.method == 'POST' and 'max_wind' in request.POST:
        pref_form = ChangePreferenceForm(request.POST)
        if pref_form.is_valid():
            max_wind = int(request.POST.get('max_wind'))
            min_temp = int(request.POST.get('min_temp'))
            if max_wind > 50 or max_wind < 0:
                messages.warning(request, 'Wind Speed: Please enter a number between 0 and 50')
                if min_temp > 40 or min_temp < -20:
                    messages.warning(request, 'Minimum Temperature: Please enter a number between -20 and 40')
                return response.HttpResponseRedirect('/')

            if min_temp > 40 or min_temp < -20:
                messages.warning(request, f'Minimum Temperature: Please enter a number between -20 and 40')
                if max_wind > 50 or max_wind < 0:
                    messages.warning(request, f'Wind Speed: Please enter a number between 0 and 50')
                return response.HttpResponseRedirect('/')

            p = Pref(max_wind=max_wind,min_temp=min_temp)
            d = Pref.objects.last()
            d.delete()
            p.save()
            messages.success(request, f'Your preferences have been updated')
            return response.HttpResponseRedirect('/')


    else:
        pref_form = ChangePreferenceForm()

    weather_data = []
    day_list = []

##############################################

    for i in initial_data.dates:
        dates = {
            'date': i.lstrip('0')
        }
        day_list.append(dates)
    general_data = {}


    for i in initial_data.weather_data_list: #todo add i.date (e.g Friday 26th January)to compare to current date

        general_data = {
            'city': i.city,
            'country': i.country,
            'sunset': i.sunset,
            'sunrise': i.sunrise,
        }


        hourly_weather = {
            'good_to_fly': good_to_fly(i,max_wind,min_temp)[1],
            'temperature': i.temp,
            'time': i.tf_time,
            'wind_speed': i.wind_speed,
            'wind_direction': i.cardinal,
            'date': i.date.lstrip('0'),
            'icon': i.iconname,
            'main': i.main,
            'why': good_to_fly(i,max_wind,min_temp)[0],
            'description': i.description.capitalize(),
            'dark': i.dark,
            'timezone': i.timezone
        }

        weather_data.append(hourly_weather)
    general_data['timezone'] = weather_data[0]['timezone']
    general_data['max_wind'] = max_wind
    general_data['min_temp'] = min_temp



    context = {
        'pref_form': pref_form,
        'city_form': city_form,
        'weather_data': weather_data,
        'day_list': day_list,
        'general_data': general_data,

    }
    return render(request, 'weather/home.html',context)