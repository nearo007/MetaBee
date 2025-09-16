from django.shortcuts import render
from django.http import request

# Create your views here.
def index(request):
    return render(request, 'index.html')

def dashboard(request):
    context = {'printers': [
        {'status': 0, 'name': 'Ender-3 V2'},
        {'status': 2, 'name': 'Prusa i3 MK4'},
        {'status': 1, 'name': 'Anycubic Kobra Go'},
        {'status': 2, 'name': 'Elegoo Neptune 4'},
        {'status': 1, 'name': 'Bambu Lab P1P'},
        {'status': 2, 'name': 'Voxelab Aquila X2'},
    ]}

    return render(request, 'dashboard.html', context)

def manage_printers(request):
    return render(request, "manage_printers.html")