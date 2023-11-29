from django.db import models

from common.models import Audit


class PlatformInfo(Audit):
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = "platform Information"

    def __str__(self):
        return self.name


class Tags(Audit):
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = "tags"

    def __str__(self):
        return self.name


class Category(Audit):
    name = models.CharField(max_length=20, unique=True)
    tags = models.ManyToManyField(Tags, related_name="categories")

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.name


class Credentials(Audit):
    platform = models.ForeignKey(PlatformInfo, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=20, unique=True, blank=False)
    client_id = models.TextField(null=True, blank=True)
    client_secret = models.TextField(null=True, blank=True)
    access_token = models.TextField(null=True, blank=True)
    api_key = models.TextField(null=True, blank=True)
    username = models.TextField(null=True, blank=True)
    password = models.TextField(null=True, blank=True)
    extra_conf = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = "credential"

    def __str__(self):
        return "{}/{}".format(self.platform.name, self.identifier)
