# Generated by Django 2.2.13 on 2020-08-05 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200802_1827'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='birthday',
        ),
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='categories',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='study',
            name='category',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='user',
            name='cellphone',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
