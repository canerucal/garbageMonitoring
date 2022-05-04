# Generated by Django 4.0.4 on 2022-05-04 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='garbageLog',
            fields=[
                ('eventID', models.AutoField(primary_key=True, serialize=False)),
                ('creationDate', models.DateField(auto_now_add=True)),
                ('ratio', models.FloatField()),
            ],
            options={
                'db_table': 'garbageLog',
            },
        ),
    ]
