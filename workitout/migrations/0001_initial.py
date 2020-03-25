# Generated by Django 2.2.3 on 2020-03-25 13:25

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
            name='Description',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primer', models.CharField(max_length=256)),
                ('steps', models.TextField()),
                ('tips', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('difficulty', models.IntegerField()),
                ('slug', models.SlugField(unique=True)),
                ('description', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='workitout.Description')),
                ('equipment', models.ManyToManyField(to='workitout.Equipment')),
            ],
        ),
        migrations.CreateModel(
            name='Muscle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='MuscleGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('duration', models.IntegerField()),
                ('difficulty', models.IntegerField()),
                ('isPrivate', models.BooleanField(default=False)),
                ('slug', models.SlugField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workout_creator', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(related_name='workout_likes', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(to='workitout.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField()),
                ('picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('isPrivate', models.BooleanField(default=False)),
                ('isVerified', models.BooleanField(default=False)),
                ('followers', models.ManyToManyField(blank=True, related_name='user_followers', to=settings.AUTH_USER_MODEL)),
                ('following', models.ManyToManyField(blank=True, related_name='user_following', to=settings.AUTH_USER_MODEL)),
                ('saved', models.ManyToManyField(to='workitout.Workout')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExInWorkout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sets', models.IntegerField()),
                ('reps', models.IntegerField()),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workitout.Exercise')),
                ('workout', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='workitout.Workout')),
            ],
        ),
        migrations.AddField(
            model_name='exercise',
            name='muscle_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='workitout.MuscleGroup'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='muscles',
            field=models.ManyToManyField(to='workitout.Muscle'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='tags',
            field=models.ManyToManyField(to='workitout.Tag'),
        ),
    ]
