from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from .models import Customer


def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')  # assign a new user to the 'customer' group
        instance.groups.add(group)  # add the users group to Django Group
        Customer.objects.create(user=instance, name=instance.username,
                                email=instance.email)  # create a Customer from the user object


post_save.connect(customer_profile, sender=User)
