# @receiver(post_save, sender=Profile)
from django.contrib.auth.models import User
from users.models import Profile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

def upsertProfile(sender, instance, created, **kwargs):
    if created:
        print('User Created:', instance)
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )
        if profile:
            print('Profile created:', profile)
    else:
        profile = Profile.objects.get(user=instance.id)
        print('Update profile', profile)
        if profile:
            profile.name = instance.first_name
            profile.email = instance.email
            profile.username = instance.username
            profile.save()
            print('Profile updated:', profile)
        

@ receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    print('Deleting User', instance)
    print('User deleted')
    user = instance.user
    user.delete()

post_save.connect(upsertProfile, sender=User)
# post_delete.connect(deleteUser, sender=Profile)