from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login

# View for Logging in or Siggning in
def Authenticate_SignUp(req):
    print("Running Authentication SignUp View", req.method)
    if req.method == "POST":
        form = CustomUserCreationForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req,user)
            return redirect("ChatAuth:Login") 
        return render(req,'ChatAuth/index.html',{'form':form})    

    form = CustomUserCreationForm()
    return render(req,'ChatAuth/index.html',{'form':form})

