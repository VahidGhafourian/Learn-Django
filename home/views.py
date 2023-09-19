from django.shortcuts import render
from .models import Todo
# Create your views here.

def home(request):
    all = Todo.objects.all()
    return render(request, 'home.html', {'all_todos': all})

def say_hello(request):
    person = {'name': 'vahid'}
    return render(request, 'hello.html', context=person)