import logging
from django.contrib.auth.models import User
from users.models import Profile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

logger = logging.getLogger(__name__)

def createProfile(sender, instance, created, **kwargs):
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

@receiver(post_save, sender=Profile)
def updateUser(sender, instance, created, **kwargs):
    logger.info('Profile Updated: %s', instance)
    profile = instance
    user = profile.user
    
    if created == False:
        logger.info('Updating User: %s', user)
        user.username = profile.username
        user.email = profile.email
        user.first_name = profile.name
        user.save()
        logger.info('User updated: %s', user)

@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    logger.info('Deleting User: %s', instance)
    user = instance.user
    user.delete()
    logger.info('User deleted: %s', user)

post_save.connect(createProfile, sender=User)
# post_delete.connect(deleteUser, sender=Profile)
