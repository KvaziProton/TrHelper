# Generated by Django 2.0.7 on 2018-08-22 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tr_helper', '0003_auto_20180822_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlecase',
            name='published',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='translationstatistic',
            name='translated',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
