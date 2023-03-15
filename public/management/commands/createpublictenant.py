
from tenant_users.tenants.utils import create_public_tenant
from django.core.management import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        create_public_tenant(domain_url='localhost', owner_email='b@gmail.com', is_verified=True )