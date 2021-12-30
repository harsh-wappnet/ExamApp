# Generated by Django 3.2.4 on 2021-10-25 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestTable',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('retailer_pool_id', models.CharField(max_length=50)),
                ('retailer_name', models.CharField(max_length=50)),
                ('logo_url', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'test_table',
            },
        ),
    ]