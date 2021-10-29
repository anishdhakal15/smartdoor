# Generated by Django 3.1.7 on 2021-10-27 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUsers',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=500)),
                ('pub_date', models.DateField()),
                ('thumbnail', models.ImageField(default='', upload_to='media/image')),
            ],
        ),
    ]
