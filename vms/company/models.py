from django.db import models
from public.building.models import Building

# Create your models here.
class Company(models.Model):
    company_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telephone_number = models.CharField(max_length=15)
    building_floor = models.IntegerField(null=False, blank=False)
    description = models.TextField(max_length=500)
    date_joined = models.DateTimeField(auto_now=True)
    building = models.ForeignKey(Building, on_delete=models.SET_NULL, null=True, related_name='building')

    def __str__(self):
        return self.company_name
    
    def create_company(self):
        """
        A method that creates a company
        """
        self.save()

    def delete_company(self):
        """
        A method that deletes a company
        """
        self.delete()

    @classmethod
    def find_company(cls, company_id):
        """
        A method that finds a company using its id
        """
        return cls.objects.filter(id=company_id)
    
    @classmethod
    def update_company(cls, id):
        """
        A method that updates a company
        """
        company = cls.objects.filter(id=id).update(id=id)
        return company
    
    @classmethod
    def search_companies(cls, search_term):
        """
        A method that searches a company
        """
        companies = cls.objects.filter(name__icontains=search_term).all()
        return companies