# Generated by Django 2.0.1 on 2018-02-08 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hostmanager', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='address',
            new_name='password',
        ),
        migrations.RemoveField(
            model_name='group',
            name='host',
        ),
        migrations.AddField(
            model_name='hosts',
            name='group',
            field=models.ManyToManyField(to='Hostmanager.Group'),
        ),
    ]
