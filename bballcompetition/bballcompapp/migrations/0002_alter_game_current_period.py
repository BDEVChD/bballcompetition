

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bballcompapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='current_period',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
