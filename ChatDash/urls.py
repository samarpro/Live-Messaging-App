from django.urls import path
from . import views
from django.contrib.auth import views as Default_View
# REGISTERING NAMESPACE
app_name = 'ChatDash'

urlpatterns = [
    path('DashBoard/get_chats/<str:receiver_name>/<int:render_all>/',views.ChatProvider,name="ChatProvider"),
    path("DashBoard/",views.DashBoardHandler, name="DashBoardHandler"),
    path("Logout/",Default_View.LogoutView.as_view(),name="Logout"),
    path("demo/",views.Demo),
]
