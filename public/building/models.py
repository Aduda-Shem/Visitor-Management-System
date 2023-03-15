from django.conf import settings
from django.db import models
from django_tenants.models import DomainMixin
from tenant_users.tenants.models import TenantBase

BUIDLING_CHOICES = (
    ("COMMERCIAL", "COMMERCIAL"),
    ("RESIDENTIAL", "RESIDENTIAL"),
    ("FACTORY", "FACTORY"),
    
)
class Building(TenantBase):
    name = models.CharField(max_length=100, blank=True)
    website = models.URLField()
    email = models.EmailField(max_length=45, blank=True)
    telephone = models.CharField(max_length=45)
    physical_address = models.CharField(max_length=45, blank=True)
    nature_of_business = models.CharField(max_length=40, choices = BUIDLING_CHOICES, default='1')

    SUBDOMAIN_FOR_ROOT_DOMAIN = ""

    class Meta:
        db_table = "buildings"
        verbose_name = "Building"
        verbose_name_plural = "Buildings"

    @property
    def subdomain(self):
        return self.slug

    # @property
    # def uri(self):
    #     return settings.EXTERNAL_URI_SCHEME + self.host

    # @property
    # def host(self):
    #     return self.host_for_subdomain(self.subdomain)

    # @staticmethod
    # def host_for_subdomain(subdomain):
    #     if subdomain == Building.SUBDOMAIN_FOR_ROOT_DOMAIN:
    #         return settings.EXTERNAL_HOST
    #     default_host = f"{subdomain}.{settings.EXTERNAL_HOST}"
    #     return default_host


def get_tenant(slug):
    return Building.objects.get(slug=slug)


class Domain(DomainMixin):
    class Meta:
        db_table = "domains"
        verbose_name = "Domain"
        verbose_name_plural = "Domains"