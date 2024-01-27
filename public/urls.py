from django.urls import path
from . import views
from .views import BookingTemplateView,ManageBookingTemplateView, delete_appointment

urlpatterns = [
    path("",views.Index,name="home"),
    path("Booking",BookingTemplateView.as_view(),name="Booking"),
    path("ManageBooking",ManageBookingTemplateView.as_view(),name="ManageBooking"),
    path("About",views.About,name="About"),
    path("Treatment",views.Treatment,name="Treatment"),
    path("Contact",views.Contact_View,name="Contact"),
    path("Login",views.Login,name="Login"),
    path("Register",views.Register,name="Register"),
    path("Logout",views.Logout,name="Logout"),
    path('delete/<int:appointment_id>/', delete_appointment, name='delete_appointment'),
]
