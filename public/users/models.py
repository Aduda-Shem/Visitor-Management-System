from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

from tenant_users.tenants.models import UserProfile

from public.building.models import Building

# Create here
class TenantUser(UserProfile):
    full_name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField( max_length=50, null=True)
    national_id = models.CharField( max_length=50, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

class Profile(models.Model):
    user = models.OneToOneField(TenantUser, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

@receiver(post_save, sender=TenantUser)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()


def get_user_profile_id(user_profile_id):
    return TenantUser.objects.select_rated().get(id=user_profile_id)