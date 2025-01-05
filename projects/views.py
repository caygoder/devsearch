from django.shortcuts import render
from django.http import HttpResponse
from .models import Project, Tag, Review    

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