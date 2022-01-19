from django.db.models.signals import post_save #signal that gets fired after an object is saved
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

#in this case we want post_save signal when an user is created
#User will be the sender here since it's going to be what is sending the signal
#Receiver is the function that receives singal and then performs some task
@receiver(post_save, sender=User) #when an user is saved send the signal
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User) #when an user is saved send the signal
def save_profile(sender, instance, **kwargs): #**kwargs accepts any additional keyword arguments onto the end of the function
    instance.profile.save()
