from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class ConfigList(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_defaults(self, request_data={}):
        list = {}
        for pair in self.configpair_set.all():
            value = request_data.get(pair.value) if pair.is_request_data_key else pair.value
            list[pair.key] = value
        return list


class ConfigPair(models.Model):
    key = models.CharField(max_length=255, help_text="Key for the configuration.")
    value = models.CharField(max_length=255, help_text="Value to assign to the configuration key.")
    is_request_data_key = models.BooleanField(default=False, help_text="If checked, uses the value provided as a key to get a value from the request data.")
    config_list = models.ForeignKey(ConfigList, on_delete=models.CASCADE)
