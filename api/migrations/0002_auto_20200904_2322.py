# Generated by Django 2.2.13 on 2020-09-04 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='s3_profile_img',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]