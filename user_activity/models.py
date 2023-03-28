from utils.tz_datetime import datetime

from django.db import models


class UserActivity(models.Model):
    last_login = models.DateTimeField(default=datetime.now)
    last_activity = models.DateTimeField(default=datetime.now)

    def set_last_login(self):
        self.last_login = datetime.now()
        self.save()

    def set_last_activity(self):
        self.last_activity = datetime.now()
        self.save()
