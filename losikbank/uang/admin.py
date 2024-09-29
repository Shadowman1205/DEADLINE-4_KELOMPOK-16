from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.nasabah)
admin.site.register(models.peminjaman)
admin.site.register(models.jenis_pekerjaan)
admin.site.register(models.limit_peminjaman)
