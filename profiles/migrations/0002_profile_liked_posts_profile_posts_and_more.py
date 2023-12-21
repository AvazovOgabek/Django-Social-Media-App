# Generated by Django 5.0 on 2023-12-14 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactions', '0001_initial'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='liked_posts',
            field=models.ManyToManyField(blank=True, related_name='liked_by_profiles', to='interactions.post'),
        ),
        migrations.AddField(
            model_name='profile',
            name='posts',
            field=models.ManyToManyField(blank=True, related_name='associated_profiles', to='interactions.post'),
        ),
        migrations.AddField(
            model_name='profile',
            name='viewed_posts',
            field=models.ManyToManyField(blank=True, related_name='viewed_by_profiles', to='interactions.post'),
        ),
    ]