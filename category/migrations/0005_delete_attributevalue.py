# Generated by Django 5.1.2 on 2024-11-12 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0004_alter_attribute_name_attributevalue'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AttributeValue',
        ),
    ]
