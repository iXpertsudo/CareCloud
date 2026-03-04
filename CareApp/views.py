from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from CareApp.models import *

import requests

import json

from requests.auth import HTTPBasicAuth

from CareApp.credentials import get_mpesa_access_token, generate_stk_password




#Authentication imports
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login







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



def show(request):
    allappointments = MyAppointments.objects.all()
    return render(request, 'show.html', {'allappointments': allappointments})



def delete(request, id):
    myappoint = MyAppointments.objects.get(id = id)
    myappoint.delete()
    return redirect('/show')


def edit(request, id):
    editappointment= get_object_or_404(MyAppointments, id=id)


    if request.method =='POST':
        editappointment.name = request.POST.get('name')
        editappointment.email = request.POST.get('email')
        editappointment.phone = request.POST.get('phone')
        editappointment.date = request.POST.get('date')
        editappointment.department = request.POST.get('department')
        editappointment.doctor = request.POST.get('doctor')
        editappointment.message = request.POST.get('message')

        editappointment.save()
        return redirect('/show')
    
    else:
        return render(request,'edit.html', {'editappointment': editappointment})
    
        




    

#Mpesa Views
def token(request):
    access_token = get_mpesa_access_token()
    return render(request, 'token.html', {"token": access_token})

def pay(request):
    return render(request, 'pay.html')

def payment_result(request):
    return render(request, 'payment_result.html')

def stk(request):
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']

        access_token = get_mpesa_access_token()
        if not access_token:
            return render(request, 'payment_result.html', {'success': False, 'error_message': 'Failed to get M-Pesa access token'})

        business_short_code, password, lipa_time = generate_stk_password()

        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": f"Bearer {access_token}"}

        request_data = {
            "BusinessShortCode": business_short_code,
            "Password": password,
            "Timestamp": lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://yourdomain.com/mpesa/callback",
            "AccountReference": "Medilab",
            "TransactionDesc": "Appointment"
        }

        try:
            response = requests.post(api_url, json=request_data, headers=headers, timeout=10)
            response_data = response.json()
        except Exception as e:
            return render(request, 'payment_result.html', {'success': False, 'error_message': f"Request failed: {str(e)}"})

        transaction_id = response_data.get("CheckoutRequestID", "N/A")
        result_code = response_data.get("ResponseCode", "1")

        if result_code == "0":
            transaction = Transaction(
                phone_number=phone,
                amount=amount,
                transaction_id=transaction_id,
                status="Pending"
            )
            transaction.save()
            context = {
                'success': True,
                'transaction_id': transaction_id,
                'amount': amount,
                'phone': phone
            }
        else:
            error_message = response_data.get("ResponseDescription", "Transaction failed")
            context = {
                'success': False,
                'error_message': error_message,
                'result_code': result_code,
                'amount': amount,
                'phone': phone
            }

        return render(request, 'payment_result.html', context)

    return HttpResponse("Invalid Request method")

def mpesa_callback(request):
    if request.method == "POST":
        try:
            callback_data = json.loads(request.body)
            stk_callback = callback_data.get('Body', {}).get('stkCallback', {})
            result_code = stk_callback.get('ResultCode')
            checkout_request_id = stk_callback.get('CheckoutRequestID')

            try:
                transaction = Transaction.objects.get(transaction_id=checkout_request_id)
                if result_code == 0:
                    transaction.status = "Success"
                    metadata_items = stk_callback.get('CallbackMetadata', {}).get('Item', [])
                    for item in metadata_items:
                        if item.get('Name') == 'MpesaReceiptNumber':
                            transaction.mpesa_receipt = item.get('Value')
                            break
                else:
                    transaction.status = "Failed"
                transaction.save()
            except Transaction.DoesNotExist:
                pass
        except Exception as e:
            print(f"Callback error: {str(e)}")
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Success"})

def transactions_list(request):
    transactions = Transaction.objects.filter(status="Success").order_by('-date')
    return render(request, 'transactions.html', {'transactions': transactions})

# ==========================
# Auth Pages
# ==========================
def register(request):
     if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check the password
        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()

                # Display a message
                messages.success(request, "Account created successfully")
                return redirect('/login')
            except:
                # Display a message if the above fails
                messages.error(request, "Username already exist")
        else:
            # Display a message saying passwords don't match
            messages.error(request, "Passwords do not match")

     return render(request, 'register.html')


    

def login_view(request):
     if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        # Check if the user exists
        if user is not None:
            # login(request, user)
            login(request,user)
            messages.success(request, "You are now logged in!")
            # Admin
            if user.is_superuser:
                return redirect('/show')

            # For Normal Users
            return redirect('/home')
        else:
            messages.error(request, "Invalid login credentials")

     return render(request, 'login.html')



    


