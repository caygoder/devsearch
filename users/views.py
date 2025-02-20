from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Skill
from .forms import CustomUserCreationForm, ProfileForm, SkillForm

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').lower().strip()
        password = request.POST.get('password', '')
        
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profiles')
            else:
                messages.error(request, "Invalid username or password")
                print(f"Failed login attempt for username: {username}")
        except Exception as e:
            messages.error(request, "An error occurred during login")
            print(f"Login error: {str(e)}")
        
    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.success(request, "User successfully logged out")
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        try:
            if form.is_valid():
                # Create user instance but don't save yet
                user = form.save(commit=False)
                
                # Sanitize username: convert to lowercase and strip whitespace
                user.username = user.username.lower().strip()
                
                # Save the user
                user.save()
                
                messages.success(request, 'User account was successfully created!')
                login(request, user)
                return redirect('edit-account')
            else:
                messages.error(request, 'Error occurred during registration!')
                # Log form validation errors in detail
                # for field, errors in form.errors.items():
                #     for error in errors:
                #         messages.error(request, f"{field}: {error}")
                #         print(f"Registration validation error - {field}: {error}")
        except Exception as e:
            messages.error(request, 'An unexpected error occurred during registration.')
            print(f"Unexpected registration error: {str(e)}")
    
    context = {"page": page, "form": form}
    return render(request, 'users/login_register.html', context)
    

def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {"profile": profile, 'skills': skills, "projects": projects}
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editAccount(request):
    form = ProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully')
                return redirect('account')
            else:
                messages.error(request, 'An error occurred during profile update')
        except Exception as e:
            messages.error(request, 'An unexpected error occurred during profile update')
            print(f"Profile update error: {str(e)}")

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)

@login_required(login_url='login')
def createSkill(request):
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = request.user.profile
            skill.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def updateSkill(request, pk):
    skill = request.user.profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('account')
        else:
            print('Error')
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)
