from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
from .decorators import analyst_required

# Create your views here.
def login_view(request):
    if request.method=="POST":

        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(request,
                          username=username,
                          password=password)
        if user is not None:
            login(request, user)

            next_url = request.POST.get("next") or request.GET.get("next")

            if next_url:
                return redirect(next_url)

            return redirect("login")
        return render(request,"accounts/login.html",
                        {"error": "Invalid username or password"})

    return render(request,"accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")



