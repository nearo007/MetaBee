from django.shortcuts import render, redirect
from django.http import request
from .models import Printer

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
    printers = Printer.objects.all()

    context = {'printers': printers}

    return render(request, "manage_printers.html", context)

def add_printer(request):
    if request.method == 'POST':
        printer_name = request.POST.get('name')
        printer_status = request.POST.get('status')
        
        print(printer_name, printer_status)
        try:
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