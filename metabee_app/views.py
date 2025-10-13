from django.shortcuts import render, redirect
from django.http import request
from .models import Printer
from .utils import get_printers_state_func, update_printers_state_in_db, DEVICE_IP, LOCAL_KEY

# Create your views here.
def index(request):
    return redirect('dashboard')

def dashboard(request):
    # context = {'printers': [
    #     {'status': 0, 'name': 'Ender-3 V2'},
    #     {'status': 2, 'name': 'Prusa i3 MK4'},
    #     {'status': 1, 'name': 'Anycubic Kobra Go'},
    #     {'status': 2, 'name': 'Elegoo Neptune 4'},
    #     {'status': 1, 'name': 'Bambu Lab P1P'},
    #     {'status': 2, 'name': 'Voxelab Aquila X2'},
    # ]}

    printers = Printer.objects.all()

    context = {'printers': printers}

    return render(request, 'dashboard.html', context)

def get_printers_state(request):
    # printers = Printer.objects.all()
    # printers_state = {}

    # for printer in printers:
    #     device_id = printer.device_id
    #     printer_state = obter_status_tomada(device_id, DEVICE_IP, LOCAL_KEY)
    #     #{'corrente_A': float, 'potencia_W': float, 'tensao_V': float}
    #     printers_state[device_id] = printer_state

    printers_state = get_printers_state_func()

    try:
        print(printers_state)
        update_printers_state_in_db(printers_state)

    except Exception as e:
        print(e)
        
    return redirect("dashboard")

def manage_printers(request):
    printers = Printer.objects.all()

    context = {'printers': printers}

    return render(request, "manage_printers.html", context)

def add_printer(request):
    if request.method == 'POST':
        printer_name = request.POST.get('name')
        printer_status = request.POST.get('status')
        device_id = request.POST.get('deviceId')
        
        try:
            if (device_id):
                new_printer = Printer.objects.create(name=printer_name, status=printer_status, device_id=device_id)
            else:
                new_printer = Printer.objects.create(name=printer_name, status=printer_status)

            new_printer.save()
            return redirect("manage_printers")

        
        except Exception as e:
            print(e)

    return render(request, "add_printer.html")

def delete_printer(request, printer_id):
    try:
        printer = Printer.objects.filter(id=printer_id).first()

        printer.delete()

        return redirect("manage_printers")

    except Exception as e:
        print(e)
        return redirect("manage_printers")