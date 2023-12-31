# Generated by Django 4.2.2 on 2023-07-12 04:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='book',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to='books.book'),
        ),
        migrations.RemoveField(
            model_name='customer',
            name='book',
        ),
        migrations.AlterField(
            model_name='publisher',
            name='book',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='publishers', to='books.book'),
        ),
        migrations.AddField(
            model_name='customer',
            name='book',
            field=models.ManyToManyField(to='books.book'),
        ),
    ]
