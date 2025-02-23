from users.models import Skill, Profile
from django.db.models import Q

def searchProfiles(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    print('search_query=', search_query)

    skills = Skill.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)
    ).distinct()  # Ensures unique profiles
    return profiles, search_query