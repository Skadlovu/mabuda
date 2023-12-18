# Generated by Django 4.2.7 on 2023-12-05 14:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(default='videos', max_length=100)),
                ('slug', models.SlugField(default='', max_length=100)),
                ('number_of_videos', models.IntegerField(blank=True, default=0)),
                ('status', models.BooleanField(default=False, help_text='0=default, 1=hidden')),
            ],
        ),
        migrations.CreateModel(
            name='VidStream',
            fields=[
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField(max_length=600)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('video', models.FileField(upload_to='videos', verbose_name='Video')),
                ('thumb', models.ImageField(blank=True, default='', upload_to='thumbs')),
                ('views', models.IntegerField(blank=True, default=0)),
                ('likes', models.IntegerField(blank=True, default=0)),
                ('dislikes', models.IntegerField(blank=True, default=0)),
                ('slug', models.SlugField(default='', max_length=100)),
                ('status', models.BooleanField(default=False, help_text='0=default, 1=hidden')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='videos.category', verbose_name='Category')),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'ordering': ['-upload_date'],
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.vidstream')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=300)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.vidstream')),
            ],
        ),
    ]