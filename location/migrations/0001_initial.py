# Generated by Django 3.1.1 on 2020-11-06 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Districts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'tbldistricts',
            },
        ),
        migrations.CreateModel(
            name='States',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'tblstates',
            },
        ),
        migrations.CreateModel(
            name='Tehsils',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.districts')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.states')),
            ],
            options={
                'db_table': 'tbltehsils',
            },
        ),
        migrations.CreateModel(
            name='Towns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.districts')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.states')),
                ('tehsil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.tehsils')),
            ],
            options={
                'db_table': 'tbltowns',
            },
        ),
        migrations.AddField(
            model_name='districts',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.states'),
        ),
    ]
