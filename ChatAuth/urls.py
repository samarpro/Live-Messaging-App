from django.urls import path
from django.contrib.auth import views as Default_View 
from . import views

# REGISTERING NAMESPACE
app_name="ChatAuth"

# Create your views here.
urlpatterns = [
    path('SignUp/',views.Authenticate_SignUp , name = "SignUp"),
    path('',Default_View.LoginView.as_view(template_name="ChatAuth/Login.html",redirect_authenticated_user='ChatDash.DashBoardHandler'), name = "Login")
]