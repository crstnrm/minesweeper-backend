# Generated by Django 3.2.5 on 2021-07-21 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_alter_board_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='boardcell',
            name='show',
            field=models.BooleanField(default=False),
        ),
    ]
