# Generated by Django 3.0.6 on 2020-05-30 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Đang xử lý', 'Đang xử lý'), ('Đang vận chuyển', 'Đang vận chuyển'), ('Đã giao hàng', 'Đã giao hàng')], default='Đang xử lý', max_length=120),
        ),
    ]
