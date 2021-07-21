# Generated by Django 3.2.5 on 2021-07-20 20:48

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('height', models.IntegerField()),
                ('width', models.IntegerField()),
                ('score', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='games', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BoardCell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('value', models.IntegerField(default=0)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='board_cells', to='board.board')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
