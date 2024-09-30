from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('uang', '0002_rename_jumlah_pinjaman_peminjaman_jumlah_peminjaman_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='limit_peminjaman',
            name='nominal_limit',
            field=models.PositiveIntegerField(),
        ),
    ]