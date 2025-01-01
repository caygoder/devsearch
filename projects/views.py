from django.shortcuts import render
from django.http import HttpResponse

projects_list = {
    1: {'name': 'Website Redesign', 'description': 'Redesign the company website to improve user experience.'},
    2: {'name': 'Mobile App Development', 'description': 'Develop a mobile application for our e-commerce platform.'},
    3: {'name': 'SEO Optimization', 'description': 'Optimize the website for search engines to increase traffic.'},
}

# Create your views here.
def projects(request):
    msg = 'Hello, you are in the projects app'
    number = 622
    context = {
        'msg': msg,
        'number': number,
        'projects': projects_list,
    }
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    try:
        project = projects_list[int(pk)]
    except KeyError:
        project = None
    return render(request, 'projects/single-project.html', {'pk': pk, 'project': project})