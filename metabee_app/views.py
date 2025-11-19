from django.shortcuts import render, redirect
from django.http import request, JsonResponse
from .models import Printer
from .utils import get_printers_state_func, update_printers_state_in_db, DEVICE_IP, LOCAL_KEY, api_get_outlet_status, api_state_from_range

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
        device_id = request.POST.get('device_id')
        idle_range = request.POST.get('idle_range')
        operating_range = request.POST.get('operating_range')
        
        try:
            new_printer = Printer.objects.create(name=printer_name, device_id=device_id, idle_range=idle_range, operating_range=operating_range)

            new_printer.save()
            return redirect("manage_printers")

        
        except Exception as e:
            print(e)

    return render(request, "add_printer.html")

def edit_printer(request, printer_id):
    printer = Printer.objects.filter(id=printer_id).first()
    
    if request.method == 'POST':
        printer_name = request.POST.get('name')
        device_id = request.POST.get('device_id')
        idle_range = request.POST.get('idle_range')
        operating_range = request.POST.get('operating_range')
        
        printer.name = printer_name
        printer.device_id = device_id
        printer.idle_range = idle_range
        printer.operating_range = operating_range

        printer.save()
        
        return redirect("manage_printers")
    
    context = {'printer': printer}
    return render(request, "edit_printer.html", context)

def delete_printer(request, printer_id):
    try:
        printer = Printer.objects.filter(id=printer_id).first()

        printer.delete()

        return redirect("manage_printers")

    except Exception as e:
        print(e)
        return redirect("manage_printers")
    
def api_get_printer_status_id(request, device_id):
    printer = Printer.objects.filter(device_id=device_id).first()
    printer_info = api_get_outlet_status(device_id=device_id)
    printer_state = api_state_from_range({device_id: printer_info})
    return JsonResponse(printer_state, safe=False)

def api_get_printer_status_name(request, printer_name):
    printer = Printer.objects.filter(name=printer_name).first()
    printer_info = api_get_outlet_status(printer.device_id)
    printer_state = api_state_from_range({printer.device_id: printer_info})
    return JsonResponse(printer_state, safe=False)

def api_all_printer_status(request):
    printers = Printer.objects.all()

    printers_state = []
    for printer in printers:
        printer_info = {
            'id': printer.id,
            'name': printer.name,
            'state': printer.state,
        }

        printers_state.append(printer_info)
    return JsonResponse(printers_state, safe=False)