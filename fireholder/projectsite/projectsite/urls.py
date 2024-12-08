from django.contrib import admin
from django.urls import path

from fire.views import HomePageView, ChartView, PieCountbySeverity, LineCountbyMonth, MultilineIncidentTop3Country,multipleBarbySeverity, map_station, map_incidents
from fire.views import (
         LocationsListView, LocationCreateView, LocationUpdateView, LocationDeleteView,
         IncidentListView, IncidentCreateView, IncidentUpdateView, IncidentDeleteView,
         FirefightersListView, FirefightersCreateView, FirefightersUpdateView, FirefightersDeleteView,
         FireStationListView,FireStationCreateView,FireStationUpdateView,FireStationDeleteView,
         FireTruckListView,FireTruckCreateView,FireTruckUpdateView,FireTruckDeleteView,
         WeatherConditionListView, WeatherConditionCreateView,WeatherConditionsUpdateView, WeatherConditionDeleteView
         )

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('dashboard_chart', ChartView.as_view(),name='dashboard-chart'),
    path('chart/', PieCountbySeverity, name='pie-chart'),
    path('lineChart/', LineCountbyMonth, name='line-chart'),
    path('multilineChart/', MultilineIncidentTop3Country, name='multiline-chart'),
    path('multiBarChart/', multipleBarbySeverity, name='multibar-chart'),
    path('stations/', map_station, name="map-station"),
    path('incidents/', map_incidents, name="map-incidents"),


    # locations
    path('location/location_list/', LocationsListView.as_view(), name='location-list'),
    path('location/location_list/add', LocationCreateView.as_view(), name="location-add"),
    path('location/location_list/<pk>', LocationUpdateView.as_view(), name="location-update"),
    path('location/location_list/<pk>/delete', LocationDeleteView.as_view(), name="location-delete"),

    # incidents
    path('incident/incident_list/', IncidentListView.as_view(), name='incident-list'),
    path('incident/incident_list/add', IncidentCreateView.as_view(), name="incident-add"),
    path('incident/incident_list/<pk>', IncidentUpdateView.as_view(), name="incident-update"),
    path('incident/incident_list/<pk>/delete', IncidentDeleteView.as_view(), name="incident-delete"),

    # firefighter
    path('firefighter/firefighter_list/', FirefightersListView.as_view(), name='firefighter-list'),
    path('firefighter/firefighter_list/add', FirefightersCreateView.as_view(), name="firefighter-add"),
    path('firefighter/firefighter_list/<pk>', FirefightersUpdateView.as_view(), name="firefighter-update"),
    path('firefighter/firefighter_list/<pk>/delete', FirefightersDeleteView.as_view(), name="firefighter-delete"),

    # firestation
    path('firestation/firestation_list/', FireStationListView.as_view(), name='firestation-list'),
    path('firestation/firestation_list/add', FireStationCreateView.as_view(), name="firestation-add"),
    path('firestation/firestation__list/<pk>', FireStationUpdateView.as_view(), name="firestation-update"),
    path('firestation/firestation__list/<pk>/delete', FireStationDeleteView.as_view(), name="firestation-delete"),

    # firetruck
    path('firetruck/firetruck_list/', FireTruckListView.as_view(), name='firetruck-list'),
    path('firetruck/firetruck_list/add', FireTruckCreateView.as_view(), name="firetruck-add"),
    path('firetruck/firetruck_list/<pk>', FireTruckUpdateView.as_view(), name="firetruck-update"),
    path('firetruck/firetruck_list/<pk>/delete', FireTruckDeleteView.as_view(), name="firetruck-delete"),
    # weather
    path('weather/weather_list/', WeatherConditionListView.as_view(), name='weather-list'),
    path('weather/weather_list/add', WeatherConditionCreateView.as_view(), name="weather-add"),
    path('weather/weather_list/<pk>', WeatherConditionsUpdateView.as_view(), name="weather-update"),
    path('weather/weather_list/<pk>/delete', WeatherConditionDeleteView.as_view(), name="weather-delete"),
]       