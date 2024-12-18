# Generated by Django 5.1.3 on 2024-12-01 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='download_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='exported_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='file_type',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='uploadedfile',
            name='file',
            field=models.FileField(upload_to='./'),
        ),
    ]
