from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from fire.models import Locations, Incident, FireStation, Firefighters, FireTruck,WeatherConditions

from fire.forms  import LocationForm, IncidentForm, FirefigthersForm,FireStationForm,FireTruckForm,WeatherConditionForm
from django.urls import reverse_lazy
from django.db import connection
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth
from django.contrib import messages

from django.db.models import Count
from datetime import datetime, date
# from django.utils import date
from django.utils.dateparse import parse_datetime
from django.db.models import Q


class HomePageView(ListView):
    model = Locations
    context_object_name = 'home'
    template_name = "home.html"

class ChartView(ListView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_queryset(self, *args, **kwargs):
        pass

# location
class LocationsListView(ListView):
    model = Locations
    context_object_name = 'locations'
    template_name = "locations/locations_list.html"
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(LocationsListView, self).get_queryset(*args, **kwargs)
        if self.request.GET.get('q') != None:
            query = self.request.GET.get('q')
            qs = qs.filter(
                Q(name__icontains=query) | 
                Q(latitude__icontains=query)|
                Q(longtitude__icontains=query)|
                Q(address__icontains=query)|
                Q(city__icontains=query)|
                Q(country__icontains=query)
                )
            
        return qs

class LocationCreateView(CreateView):
    model = Locations
    form_class = LocationForm
    template_name = 'locations/location_add.html'
    success_url = reverse_lazy('location-list')

    def form_valid(self,form):
        name = form.instance.name
        messages.success(self.request, f'{name} has been successfully added.')

        return super().form_valid(form)

class LocationUpdateView(UpdateView):
    model = Locations
    form_class = LocationForm
    template_name = 'locations/location_edit.html'
    success_url = reverse_lazy('location-list')

    def form_valid(self,form):
        name = form.instance.name
        messages.success(self.request, f'{name} has been successfully updated.')

        return super().form_valid(form)

class LocationDeleteView(DeleteView):
    model = Locations
    template_name = 'locations/location_del.html'
    success_url = reverse_lazy('location-list')
        
    def form_valid(self,form):
        messages.success(self.request, 'Successfully deleted.')

        return super().form_valid(form)

# incidents
class IncidentListView(ListView):
    model = Incident
    context_object_name = 'incident'
    template_name = "incident/incident_list.html"
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(IncidentListView, self).get_queryset(*args, **kwargs)
        if self.request.GET.get('q') != None:
            query = self.request.GET.get('q')
            qs = qs.filter( 
                Q(location__name__icontains=query)|
                Q(date_time__icontains=query)|
                Q(severity_level__icontains=query)|
                Q(description__icontains=query)
                )
            
        return qs


    
class IncidentCreateView(CreateView):
    model = Incident
    form_class = IncidentForm
    template_name = 'incident/incident_add.html'
    success_url = reverse_lazy ('incident-list')

    def form_valid(self,form):
        severity_level = form.instance.severity_level
        messages.success(self.request, f'{severity_level} has been successfully added.')

        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        self.object = None
        date_time_str = request.POST.get('date_time')
        current_date_time = datetime.now()
        date_time = datetime.strptime(date_time_str, '%Y-%m-%d')
        
        try:
            if date_time > current_date_time:
                messages.error(request, "Date cannot be in the future")
                return self.form_invalid(self.get_form())

        except (ValueError, TypeError):
            messages.error(request, "Date time must be in the correct format (YYYY-MM-DD HH:MM:SS).")
            return self.form_invalid(self.get_form())

        
        
        return super().post(request, *args, **kwargs)

class IncidentUpdateView(UpdateView):
    model = Incident
    form_class = IncidentForm
    template_name = 'incident/incident_edit.html'
    success_url = reverse_lazy('incident-list')

    def form_valid(self,form):
        severity_level = form.instance.severity_level
        messages.success(self.request, f'New incident has been successfully updated.')

        return super().form_valid(form)

class IncidentDeleteView(DeleteView):
    model = Incident
    template_name = 'incident/incident_del.html'
    success_url = reverse_lazy('incident-list')

    def form_valid(self,form):
        messages.success(self.request, 'Successfully deleted.')

        return super().form_valid(form)

# firefighters
class FirefightersListView(ListView):
    model = Firefighters 
    context_object_name = 'firefighter'
    template_name = "firefighters/firefighter_list.html"
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(FirefightersListView, self).get_queryset(*args, **kwargs)
        if self.request.GET.get('q') != None:
            query = self.request.GET.get('q')

            qs = qs.filter(
                Q(name__icontains=query)|
                Q(rank__icontains=query)|
                Q(experience_level__icontains=query)|
                Q(station__in=[choice[0] for choice in Firefighters.XP_CHOICES if query.lower() in choice[0].lower()])
                )
            
        return qs
    
class FirefightersCreateView(CreateView):
    model = Firefighters
    form_class = FirefigthersForm
    template_name = 'firefighters/firefighter_add.html'
    success_url = reverse_lazy ('firefighter-list')

    def form_valid(self,form):
        name = form.instance.name
        messages.success(self.request, f'{name} has been successfully added.')

        return super().form_valid(form)

class FirefightersUpdateView(UpdateView):
    model = Firefighters
    form_class = FirefigthersForm
    template_name = 'firefighters/firefighter_edit.html'
    success_url = reverse_lazy('firefighter-list')

    def form_valid(self,form):
        name = form.instance.name
        messages.success(self.request, f'{name} has been successfully updated.')

        return super().form_valid(form)

class FirefightersDeleteView(DeleteView):
    model = Firefighters
    template_name = 'firefighters/firefighter_del.html'
    success_url = reverse_lazy('firefighter-list')

    def form_valid(self,form):
        messages.success(self.request, 'Successfully deleted.')

        return super().form_valid(form)

# firestation
class FireStationListView(ListView):
    model = FireStation 
    context_object_name = 'firestation'
    template_name = "firestation/firestation_list.html"
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(FireStationListView, self).get_queryset(*args, **kwargs)
        if self.request.GET.get('q') != None:
            query = self.request.GET.get('q')
            qs = qs.filter(
                Q(name__icontains=query) | 
                Q(latitude__icontains=query)|
                Q(longitude__icontains=query)|
                Q(address__icontains=query)|
                Q(city__icontains=query)|
                Q(country__icontains=query)
                )
            
        return qs
    
class FireStationCreateView(CreateView):
    model = FireStation
    form_class = FireStationForm
    template_name = 'firestation/firestation_add.html'
    success_url = reverse_lazy ('firestation-list')

    def form_valid(self,form):
        name = form.instance.name
        messages.success(self.request, f'{name} has been successfully added.')

        return super().form_valid(form)

class FireStationUpdateView(UpdateView):
    model = FireStation
    form_class = FireStationForm
    template_name = 'firestation/firestation_edit.html'
    success_url = reverse_lazy('firestation-list')

    def form_valid(self,form):
        name = form.instance.name
        messages.success(self.request, f'{name} has been successfully added.')

        return super().form_valid(form)

class FireStationDeleteView(DeleteView):
    model = FireStation
    template_name = 'firestation/firestation_del.html'
    success_url = reverse_lazy('firestation-list')

    def form_valid(self,form):
        messages.success(self.request, 'Successfully deleted.')

        return super().form_valid(form)

#firetruck

class FireTruckListView(ListView):
    model = FireTruck 
    context_object_name = 'firetruck'
    template_name = "firetruck/firetruck_list.html"
    paginate_by = 5
    
    def get_queryset(self, *args, **kwargs):
        qs = super(FireTruckListView, self).get_queryset(*args, **kwargs)
        if self.request.GET.get('q') != None:
            query = self.request.GET.get('q')
            qs = qs.filter(
                Q(truck_number__icontains=query) | 
                Q(model__icontains=query)|
                Q(capacity__icontains=query)|
                Q(station__name__icontains=query)
                )
            
        return qs
class FireTruckCreateView(CreateView):
    model = FireTruck
    form_class = FireTruckForm
    template_name = 'firetruck/firetruck_add.html'
    success_url = reverse_lazy ('firetruck-list')

    def form_valid(self,form):
        truck_number = form.instance.truck_number
        messages.success(self.request, f'{truck_number} has been successfully added.')

        return super().form_valid(form)

class FireTruckUpdateView(UpdateView):
    model = FireTruck
    form_class = FireTruckForm
    template_name = 'firetruck/firetruck_edit.html'
    success_url = reverse_lazy('firetruck-list')

    def form_valid(self,form):
        truck_number = form.instance.truck_number
        messages.success(self.request, f'{truck_number} has been successfully updated.')

        return super().form_valid(form)

class FireTruckDeleteView(DeleteView):
    model = FireTruck
    template_name = 'firetruck/firetruck_del.html'
    success_url = reverse_lazy('firetruck-list')

    def form_valid(self,form):
        messages.success(self.request, 'Successfully deleted.')

        return super().form_valid(form)

# weather
class WeatherConditionListView(ListView):
    model = WeatherConditions 
    context_object_name = 'weathercondition'
    template_name = "weather/weather_list.html"
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(WeatherConditionListView, self).get_queryset(*args, **kwargs)
        if self.request.GET.get('q') != None:
            query = self.request.GET.get('q')
            qs = qs.filter(
                Q(temperature__icontains=query)|
                Q(humidity__icontains=query)|
                Q(wind_speed__icontains=query)|
                Q(weather_description__icontains=query)
                )
            
        return qs
    
class WeatherConditionCreateView(CreateView):
    model = WeatherConditions
    form_class = WeatherConditionForm
    template_name = 'weather/weather_add.html'
    success_url = reverse_lazy ('weather-list')

    def form_valid(self,form):
        weather_description = form.instance.weather_description
        messages.success(self.request, f'{weather_description} has been successfully added.')

        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        self.object = None
        temperature = request.POST.get('temperature')
        humidity = request.POST.get('humidity')
        wind_speed = request.POST.get('wind_speed')

        errors = []
        for field_name, value in [('temperature', temperature), ('humidity', humidity), ('wind_speed', wind_speed)]:
            try:
                if float(value) < 0:
                    errors.append(
                        f"{field_name.capitalize()} must be a positive number."
                    )
            except (ValueError, TypeError):
                errors.append(f"{field_name.capitalize()} must be a valid positive number.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return self.form_invalid(self.get_form())
        
        return super().post(request, *args, **kwargs)
    
    

class WeatherConditionsUpdateView(UpdateView):
    model = WeatherConditions
    form_class = WeatherConditionForm
    template_name = 'weather/weather_edit.html'
    success_url = reverse_lazy('weather-list')

    def form_valid(self,form):
        weather_description = form.instance.weather_description
        messages.success(self.request, f'{weather_description} has been successfully added.')

        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        temperature = request.POST.get('temperature')
        humidity = request.POST.get('humidity')
        wind_speed = request.POST.get('wind_speed')

        errors = []
        for field_name, value in [('temperature', temperature), ('humidity', humidity), ('wind_speed', wind_speed)]:
            try:
                if float(value) < 0:
                    errors.append(
                        f"{field_name.capitalize()} must be a positive number."
                    )
            except (ValueError, TypeError):
                errors.append(f"{field_name.capitalize()} must be a valid positive number.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return self.form_invalid(self.get_form())
        
        return super().post(request, *args, **kwargs)

class WeatherConditionDeleteView(DeleteView):
    model = WeatherConditions
    template_name = 'weather/weather_del.html'
    success_url = reverse_lazy('weather-list')

    def form_valid(self,form):
        messages.success(self.request, 'Successfully deleted.')

        return super().form_valid(form)

def PieCountbySeverity(request):
    query = """
        SELECT severity_level, COUNT(*) as count
        FROM fire_incident
        GROUP BY severity_level
        """
    data = {}
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    if rows:
        data = {severity: count for severity, count in rows}
    else:
        data = {}

    return JsonResponse(data)
    
def LineCountbyMonth(request):

        current_year = datetime.now().year

        result = {month: 0 for month in range(1, 13)}

        incidents_per_month = Incident.objects.filter(date_time__year=current_year)\
            .values_list('date_time', flat=True)
        
        for date_time in incidents_per_month:
            if date_time:
                month = date_time.month
                result[month] += 1
        
        month_names = {
            1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 
            7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
        }

        result_with_month_names = {
            month_names[month]: count for month, count in result.items()
        }

        return JsonResponse(result_with_month_names)

def MultilineIncidentTop3Country(request):

        query = '''
            SELECT
            fl.country,
            strftime('%m', fi.date_time) AS month,
            COUNT(fi.id) AS incident_count
        FROM
            fire_incident fi
        JOIN
            fire_locations fl ON fi.location_id = fl.id
        WHERE
            fl.country IN (
                SELECT
                    fl_top.country
                FROM
                    fire_incident fi_top
                JOIN
                    fire_locations fl_top ON fi_top.location_id = fl_top.id
                WHERE
                    strftime('%Y', fi_top.date_time) = strftime('%Y', 'now')
                GROUP BY
                    fl_top.country
                ORDER BY
                    COUNT(fi_top.id) DESC
                LIMIT 3
            )
            AND strftime('%Y', fi.date_time) = strftime('%Y', 'now')
        GROUP BY
            fl.country, month
        ORDER BY
            fl.country, month;
        '''

        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        result = {}

        months = set(str(i).zfill(2) for i in range(1, 13))

        for row in rows:
            country = row[0]
            month = row[1]
            total_incidents = row[2]

            if country not in result:
              result[country] = {month: 0 for month in months}

            result[country][month] = total_incidents
        
        while len(result) < 3:
            missing_country = f"Country {len(result) + 1}"
            result[missing_country] = {month: 0 for month in months}

        for country in result:
            result[country] = dict(sorted(result[country].items()))
        
        return JsonResponse(result)
    
def multipleBarbySeverity(request):
        query = '''
        SELECT
            fi.severity_level,
            strftime('%m', fi.date_time) AS month,
            COUNT(fi.id) AS incident_count
        FROM
            fire_incident fi
        GROUP BY fi.severity_level, month
        '''

        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
        
        result = {}
        months = set(str(i).zfill(2) for i in range(1, 13))

        for row in rows:
            level = str(row[0])
            month = row[1]
            total_incidents = row[2]

            if level not in result:
                result[level] = {month: 0 for month in months}

            result[level][month] = total_incidents

        for level in result:
             result[level] = dict(sorted(result[level].items()))
        
        return JsonResponse(result)

def map_station(request):
     fire_stations = FireStation.objects.values("name", "latitude", "longitude")
     fire_stations_list = [
          {
               "name": station["name"],
               "latitude": float(station["latitude"]),
               "longitude": float(station["longitude"]),
          }
          for station in fire_stations
     ]
     return render(request, "map_station.html", {"fireStations": fire_stations_list})

def map_incidents(request):
     incidents = Incident.objects.select_related("location").values(
          "location__name", "location__latitude", "location__longitude", 
          "date_time", "severity_level", "description"
     )

     incidents_list = [
          {
               "name": incident["location__name"],
               "latitude": float(incident["location__latitude"]),
               "longitude": float(incident["location__longitude"]),
               "date_time": incident["date_time"].strftime("%Y-%m-%d %H:%H:%S") if incident["date_time"] else "N/A",
               "severity_level": incident["severity_level"],
               "description": incident["description"],
          }
          for incident in incidents
     ]
     return render(request, "map_incidents.html", {"fireIncidents": incidents_list})






