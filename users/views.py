from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Skill
from .forms import CustomUserCreationForm

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Username does not exist")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, "Username OR password is incorrect")
        
    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.success(request, "User successfully logged out")
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        print("user creation...")
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            print("user created")
            messages.success(request, 'User account was successfully created!')
            
            login(request, user)
            return redirect('profiles')
        
        else:
            messages.error(request, 'Error occured during registration!')
            print("Error creating user account")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    
    context = {"page": page, "form": form}
    return render(request, 'users/login_register.html', context)
    

def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context)