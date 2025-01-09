from django.shortcuts import render, redirect
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

def createProject(request):
    form = ProjectForm()
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, )
        if form.is_valid():
            form.save()
            return redirect('projects')
    
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)

def updateProject(request, id):
    project = Project.objects.get(id=id)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)

def deleteProject(request, id):
    project = Project.objects.get(id=id)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'projects/delete_template.html', context)
