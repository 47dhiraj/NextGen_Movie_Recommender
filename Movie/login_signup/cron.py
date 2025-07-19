from django.contrib.auth.models import User
from .models import User
from datetime import datetime


def registration_expiry_check():
    print('cron page running......')
    today = datetime.today()
    users = User.objects.filter(is_verified=False)
    for u in users:
        print(u)
        expdate = u.expiration_date
        if expdate < today:
            u.delete()







