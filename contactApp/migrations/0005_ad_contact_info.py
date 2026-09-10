from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactApp', '0004_auto_20260518_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='contact_info',
            field=models.CharField(
                blank=True,
                default='',
                max_length=100,
                verbose_name='联系方式',
            ),
        ),
    ]
