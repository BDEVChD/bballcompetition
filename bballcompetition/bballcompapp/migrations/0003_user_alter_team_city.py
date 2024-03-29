# Generated by Django 5.0.3 on 2024-03-14 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bballcompapp', '0002_alter_game_current_period'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='team',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
