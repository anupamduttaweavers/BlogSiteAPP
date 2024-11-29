# Generated by Django 5.1.3 on 2024-11-28 12:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('postId', models.AutoField(primary_key=True, serialize=False)),
                ('postTitle', models.CharField(max_length=250)),
                ('postContent', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='home/wadmin/Downloads/BlogSiteAPP/BlogApp/static/jpeg/Posts/')),
                ('postDate', models.DateTimeField(auto_now_add=True)),
                ('postEditDate', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.account')),
            ],
        ),
    ]
