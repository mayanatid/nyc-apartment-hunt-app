# Generated by Django 4.0.1 on 2022-01-10 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_listing_neighborhood'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
