from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class OrganizerManager(BaseUserManager):
    def create_user(self, email, company_name=None, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        
        email = self.normalize_email(email)
        organizer = self.model(email=email, company_name=company_name, **extra_fields)
        organizer.set_password(password)
        organizer.save(using=self._db)
        
        return organizer
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email=email, password=password, **extra_fields)
