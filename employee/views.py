from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm

# Create your views here.


def home(request):
    
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in ")
            return redirect('home') 
        else:
            messages.success(request, "there was an error in login details")
            return redirect('home')
    else:    
        return render(request, 'home.html', {'Message':"Login Succesfully"})


def logout_user(request):
    logout(request)
    messages.success(request, "You have logout")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})


def adminlogin(request):
    user_all = User.objects.all()
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in ")
            return redirect('adminlogin') 
        
        else:
            messages.success(request, "there was an error in login details")
            return redirect('adminlogin')
    else:    
        return render(request, 'adminlogin.html', {'user_all':user_all})


def logout_user(request):
    logout(request)
    messages.success(request, "You have logout")
    return redirect('adminlogin')



def delete_record(request, pk):
	if request.user.is_authenticated:
		delete_it = User.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "User Deleted Successfully...")
		return redirect('adminlogin')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('adminlogin')
 

def edit_record(request, pk):
	if request.user.is_authenticated:
		current_record = User.objects.get(id=pk)
		form = SignUpForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('adminlogin')
		return render(request, 'userupdate.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('adminlogin')
