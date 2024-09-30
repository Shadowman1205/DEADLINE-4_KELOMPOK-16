from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('uang', '0003_terserah'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jenis_pekerjaan',
            name='penghasilan_perbulan',
            field=models.PositiveIntegerField(),
        ),
    ]