from django.shortcuts import render
from django.http import request

# Create your views here.
def index(request):
    context = {'printer_count': (range(6))}
    return render(request, 'index.html', context)