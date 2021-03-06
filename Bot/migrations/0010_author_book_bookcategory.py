# Generated by Django 3.2.12 on 2022-03-27 04:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Bot', '0009_alter_test_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, verbose_name='Ismi')),
            ],
            options={
                'verbose_name': 'Muallif',
                'verbose_name_plural': 'Mualliflar',
            },
        ),
        migrations.CreateModel(
            name='BookCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Kategoriya nomi')),
            ],
            options={
                'verbose_name': 'Kitoblar kategoriyasi',
                'verbose_name_plural': 'Kitoblar kategoriyalari',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Nomi')),
                ('language', models.CharField(choices=[('english', '๐ฌ๐ง English'), ('uzbek', "๐บ๐ฟ O'zbekcha"), ('russian', '๐ท๐บ ะ ัััะบะธะน')], default='uzbek', max_length=100, verbose_name='Til')),
                ('total_pages', models.IntegerField(verbose_name='Sahifalar soni')),
                ('published_date', models.DateField(verbose_name='Nashr etilgan yili')),
                ('file', models.FileField(blank=True, upload_to='books/', verbose_name='Test')),
                ('source_id', models.CharField(max_length=255)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bot.author', verbose_name='Muallif')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bot.bookcategory', verbose_name='Kategoriya')),
            ],
            options={
                'verbose_name': 'Kitob',
                'verbose_name_plural': 'Kitoblar',
            },
        ),
    ]
