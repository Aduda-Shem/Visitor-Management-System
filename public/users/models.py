from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from tenant_users.tenants.models import UserProfile

from public.building.models import Building


class TenantUser(UserProfile):
    full_name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField( max_length=50, null=True)
    national_id = models.CharField( max_length=50, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

