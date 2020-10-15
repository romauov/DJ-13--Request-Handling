from django.shortcuts import render, redirect
from django.urls import reverse
import csv
from django.conf import settings
from django.core.paginator import Paginator


def index(request):
      return redirect(reverse(bus_stations))

def bus_stations(request):

    items_by = 10
    stations_list = []

    with open(settings.BUS_STATION_CSV) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            stations_list.append(row)

    paginator = Paginator(stations_list, items_by)

    page_number = int(request.GET.get('page', '1'))
    page_obj = paginator.get_page(page_number)


    pp, np, prev_page_url, next_page_url = None, None, None, None

    if page_obj.has_previous():
        pp = page_obj.previous_page_number()
        prev_page_url = f'bus_stations?page={pp}'
    if page_obj.has_next():
        np = page_obj.next_page_number()
        next_page_url = f'bus_stations?page={np}'

    bus_stations_pick = [{'Name': line['Name'], 'Street': line['Street'], 'District': line['District']} for line in page_obj]

    return render(request, 'index.html', context={
        'bus_stations': bus_stations_pick,
        'current_page': page_number,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })