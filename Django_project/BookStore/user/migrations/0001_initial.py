# Generated by Django 3.0.4 on 2021-03-23 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, verbose_name='用户注册')),
                ('password', models.CharField(max_length=100, verbose_name='用户密码')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
