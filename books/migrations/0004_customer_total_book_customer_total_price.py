# Generated by Django 4.2.2 on 2023-07-12 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_book_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='total_book',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='total_price',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]
