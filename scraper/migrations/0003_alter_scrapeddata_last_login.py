# Generated by Django 3.2.14 on 2022-07-22 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_alter_scrapeddata_mydashid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrapeddata',
            name='last_login',
            field=models.CharField(max_length=120),
        ),
    ]
