import logging
from django.contrib.auth.models import User
from users.models import Profile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

logger = logging.getLogger(__name__)

def upsertProfile(sender, instance, created, **kwargs):
    if created:
        logger.info('User Created: %s', instance)
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )
        if profile:
            logger.info('Profile created: %s', profile)
    else:
        profile = Profile.objects.get(user=instance.id)
        logger.info('Updating profile for user: %s', instance.username)
        if profile:
            profile.name = instance.first_name
            profile.email = instance.email
            profile.username = instance.username
            profile.save()
            logger.info('Profile updated - Username: %s, Name: %s, Email: %s', profile.username, profile.name, profile.email)

@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    logger.info('Deleting User: %s', instance)
    user = instance.user
    user.delete()
    logger.info('User deleted: %s', user)

post_save.connect(upsertProfile, sender=User)
# post_delete.connect(deleteUser, sender=Profile)
