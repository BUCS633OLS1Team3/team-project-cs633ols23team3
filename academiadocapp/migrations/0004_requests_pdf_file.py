# Generated by Django 4.1.5 on 2023-02-18 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academiadocapp', '0003_alter_requests_approve_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='requests',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='pdfs/'),
        ),
    ]