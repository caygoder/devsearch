from projects.models import Project
from django.db.models import Q
from .models import Tag

def searchProjects(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    print('search_query=', search_query)

    # skills = Skill.objects.filter(name__icontains=search_query)
    tags = Tag.objects.filter(name__icontains=search_query)
    projects = Project.objects.filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    ).distinct()  # Ensures unique projects
    return projects, search_query