from django.db import models
import datetime
from django.contrib.auth.models import User

class Entry(models.Model):
    user = models.ForeignKey(User)
    action = models.CharField( max_length=100, unique=False, blank=False)
    datetime = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = "admin_entries"