from django.shortcuts import render


from CareApp.models import *


# Create your views here.

def home(request):
    return render(request, 'index.html')

def starter(request):
    return render(request, 'starter-page.html')

def appointment(request):
    
    if request.method == 'POST':

        all =MyAppointments(
            name = request.POST['name'],
            email = request.POST['email'],
            phone = request.POST['phone'],
            date= request.POST['date'],
            department = request.POST['department'],
            doctor = request.POST['doctor'],
            message = request.POST['message'],
        )

        all.save()
        return render(request, 'appointment.html')
    
    else:
        return render(request, 'appointment.html')
     

def about(request):
    return render(request, 'about.html')




