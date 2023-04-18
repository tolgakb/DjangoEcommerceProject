from django.shortcuts import redirect, render
from .models import Account
from .forms import RegistirationForm
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required


# Create your views here.

def register(request):
    if request.method == "POST":
        form = RegistirationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name= first_name, last_name= last_name, email= email, username= username, password= password)
            user.phone_number = phone_number
            user.save()
            messages.success(request, 'Registration succesful.')
            return redirect('login')
    else:
        form = RegistirationForm()
    context = {
        'form': form,
    }
    return render(request, 'account/register.html', context)

def login(request):
    if request.method =='POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email= email, password= password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')

    return render(request, 'account/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')

@login_required(login_url = 'login')
def dashboard(request):
    return render(request,'account/dashboard.html')