from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Project, Tag, Review
from .forms import ProjectForm

# Create your views here.
def projects(request):
    projectsObj = Project.objects.all()
    context = {'projects': projectsObj,}
    return render(request, 'projects/projects.html', context)

def project(request, id):
    try:
        projectObj = Project.objects.get(id=id)
        tags = projectObj.tags.all()
    except Project.DoesNotExist:
        projectObj = None
    return render(request, 'projects/single-project.html', {'id': id, 'project': projectObj, 'tags': tags})

@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('projects')
    
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login')
def updateProject(request, id):
    profile = request.user.profile
    project = profile.project_set.get(id=id)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login')
def deleteProject(request, id):
    profile = request.user.profile
    project = profile.project_set.get(id=id)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'projects/delete_template.html', context)


