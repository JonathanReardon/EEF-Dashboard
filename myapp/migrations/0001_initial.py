# Generated by Django 4.1.1 on 2023-03-28 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('index', models.BigAutoField(db_column='index', primary_key=True, serialize=False)),
                ('text_field', models.TextField()),
                ('edu_setting_data', models.TextField(default='')),
                ('level_assign', models.TextField()),
                ('student_gender', models.TextField()),
                ('eppi_id', models.TextField(default='')),
                ('short_title', models.TextField(default='')),
                ('main_title', models.TextField(default='')),
                ('year', models.TextField(default='')),
                ('abstract', models.TextField(default='')),
                ('admin_strand_data', models.TextField(default='')),
                ('url', models.TextField(default='')),
                ('smd_value', models.TextField(default='')),
                ('sesmd_value', models.TextField(default='')),
                ('smd_red_value', models.TextField(default='')),
                ('sesmd_red_value', models.TextField(default='')),
                ('smd_sci_value', models.TextField(default='')),
                ('sesmd_sci_value', models.TextField(default='')),
            ],
        ),
    ]
