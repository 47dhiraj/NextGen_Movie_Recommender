from django.db import models
from django.db import models

from django.contrib.auth.models import Permission, User
from django.contrib.auth.models import AbstractUser

from datetime import datetime, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class User(AbstractUser):
    # email = models.EmailField(unique=True)
    is_client = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    image = models.ImageField(upload_to='uploads/', null=True, blank=True, default='uploads/img_avatar.png')
    expiration_date = models.DateTimeField(default=datetime.now() + timedelta(days=1))

    # Yedi Template bata directly kunai function lai object.property use garera values lina cha vani yestari function use huncha ..
    def count_rated_movies(self):
        count = self.client_user.all().count()
        return count

# yo talako signal chai social site bata login huney user lai direct is_active= True ani is_verified=True banaidina use gareko..
# yo tala ko code lekhena vani social site bata user login hunai paundaina..

@receiver(post_save, sender=User)  # sender ma model class ko name aaucha
def user_post_save_receiver(sender, instance, created, *args, **kwargs):  # post_save has created argument  # yo line ko instance le sender ma vayeko model class ma vayeko instance or object lai refer garcha
    """
    after saved in the database
    """
    if created:
        if instance.email == '':
            instance.is_active = True
            instance.is_verified = True
            # instance.email = instance.username
            instance.save()

