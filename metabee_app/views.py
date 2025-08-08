from django.shortcuts import render
from django.http import request

# Create your views here.
def index(request):
    context = {'printers': [
        {'status': True, 'name': 'Ender-3 V2'},
        {'status': False, 'name': 'Prusa i3 MK4'},
        {'status': False, 'name': 'Anycubic Kobra Go'},
        {'status': False, 'name': 'Elegoo Neptune 4'},
        {'status': True, 'name': 'Bambu Lab P1P'},
        {'status': False, 'name': 'Voxelab Aquila X2'},
    ]}

    return render(request, 'index.html', context)