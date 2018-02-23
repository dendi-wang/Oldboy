from django.db import models


# create your models here.


class UserInfo(models.Model):
    name = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    user_info = models.ForeignKey(to='Group', to_field='nid', on_delete=False)

    def __str__(self):
        return self.name


class Group(models.Model):
    nid = models.AutoField(primary_key=True)
    groupname = models.CharField(max_length=50)
    host = models.ManyToManyField('Hosts')

    def __str__(self):
        return self.groupname


class Hosts(models.Model):
    nid = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=50)
    ip = models.GenericIPAddressField()
    port = models.IntegerField()


    def __str__(self):
        return self.hostname

