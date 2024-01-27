from typing import Any, Dict
from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView
from django.conf import settings
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib import messages
from django.views.generic import ListView
import datetime
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.core.exceptions import ValidationError
from .models import Appointment
from django.contrib.auth.mixins import LoginRequiredMixin





def Index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        admin_email = 'tkayurvedicpharmacy@gmail.com'  # Set the admin's email address
        
        send_mail(
            f"Form Submission from {name}",
            message,
            email,
            [admin_email],
            fail_silently=False,
        )
        return render(request, "success.html")

    return render(request, 'base.html')



class BookingTemplateView(TemplateView, LoginRequiredMixin):
    template_name = "booking.html"
    login_url = "/Login"
 
    def post(self, request):
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        message = request.POST.get("request")

        appointment = Appointment.objects.create(
            first_name = fname,
            last_name = lname,
            email = email,
            phone = mobile,
            request = message,
        )

        appointment.save()

        messages.add_message(request, messages.SUCCESS, f"Thanks {fname} for making a booking we will mail you ASAP!")
        return HttpResponseRedirect(request.path)
    
    

class ManageBookingTemplateView(ListView):
    template_name = "managebooking.html"
    model = Appointment
    context_object_name = "appointments"
    paginate_by = 3

    def post(self, request, *args, **kwargs):
        if 'action' in request.POST:
            action = request.POST.get("action")
            appointment_id = request.POST.get('appointment_id')

            if action == "Accept":
                date = request.POST.get("date")
                appointment = Appointment.objects.get(id=appointment_id)
                appointment.accepted = True
                appointment.accepted_date = datetime.datetime.now()
                appointment.save()

                data = {
                    "fname": appointment.first_name,
                    "date": date
                }

                message = get_template('email.html').render(data)

                email = EmailMessage(
                    "Review of Your Booking",
                    message,
                    settings.EMAIL_HOST_USER,
                    [appointment.email],
                )
                email.content_subtype = "html"
                email.send()
                messages.add_message(request, messages.SUCCESS, f"Accepted the date on {date}")

            elif action == "Delete":
                appointment = get_object_or_404(Appointment, id=appointment_id)
                appointment.delete()
                messages.add_message(request, messages.SUCCESS, f"Deleted appointment with ID {appointment_id}")

        return HttpResponseRedirect(request.path)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            "title": "Manage Booking"
        })
        return context


def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    # You can add any messages or additional logic here if needed
    return redirect('ManageBooking')
    
def About(request):
    return render(request, "about.html")

def Treatment(request):
    return render(request, "treatment.html")


@csrf_exempt
def Contact_View(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        admin_email = 'tkayurvedicpharmacy@gmail.com'  # Set the admin's email address
        
        send_mail(
            f"Form Submission from {name}",
            message,
            email,
            [admin_email],
            fail_silently=False,
        )
        return render(request, "success.html")

    return render(request, 'contact.html')


@csrf_exempt
def Login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return redirect('Login')

    return render(request,'login.html')

    

def Register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password == confirm_password:
            if User.objects.filter(username = username).exists():
                messages.info(request,'Username is already exists')
                return redirect(Register)
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                user.set_password(password)
                user.save()
                print("Success")
                return redirect("Login")
    else:
        print("this is not post method")
    return render(request, "login.html")

def Logout(request):
    logout(request)
    return render(request, "base.html")

