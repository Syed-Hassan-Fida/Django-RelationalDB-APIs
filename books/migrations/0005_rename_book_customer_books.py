# Generated by Django 4.2.2 on 2023-07-12 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_customer_total_book_customer_total_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='book',
            new_name='books',
        ),
    ]
