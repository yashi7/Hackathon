# Generated by Django 4.2.7 on 2024-11-27 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Fashion', '0008_currentbalance_ngo_transaction_remove_category_u_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DonationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ngo_name', models.CharField(max_length=100)),
                ('food_needed', models.CharField(max_length=200)),
                ('donor_name', models.CharField(max_length=100)),
                ('donor_contact', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]