# Generated by Django 4.2.7 on 2024-10-26 21:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Fashion', '0004_rename_img_id_wardrobe_w_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='rec',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]