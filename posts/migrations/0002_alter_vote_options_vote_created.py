# Generated by Django 4.1 on 2022-08-08 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vote',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='vote',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]