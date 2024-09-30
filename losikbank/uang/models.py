from django.db import models

# Create your models here.
class jenis_pekerjaan(models.Model):
    id_jenis_pekerjaan = models.AutoField(primary_key=True)
    nama_pekerjaan = models.CharField(max_length=100)
    penghasilan_perbulan = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.nama_pekerjaan} - {self.penghasilan_perbulan}"

class nasabah(models.Model):
    id_nasabah = models.AutoField(primary_key=True)
    nama_nasabah = models.CharField(max_length=100)
    umur_nasabah = models.PositiveIntegerField()
    jenis_kelamin = models.CharField(max_length=100)
    alamat_nasabah = models.TextField()
    id_jenis_pekerjaan = models.ForeignKey(jenis_pekerjaan, on_delete=models.CASCADE)
    nama_perusahaan = models.CharField(max_length=100)
    tingkat_pendidikan = models.CharField(max_length=100)
    status_pernikahan = models.BooleanField() 
    nama_orang_tua = models.CharField(max_length=100)
    nama_lengkap_kontak_darurat = models.CharField(max_length=100)
    nomor_kontak_darurat = models.PositiveBigIntegerField()
    hubungan_dengan_peminjam = models.CharField(max_length=100)
    sisa_kontrak_kerja = models.PositiveIntegerField(blank=True, null=True)


    def __str__(self):
        return f"{self.nama_nasabah}"

class limit_peminjaman(models.Model):
    id_limit_peminjaman = models.AutoField(primary_key=True)
    id_jenis_pekerjaan = models.ForeignKey(jenis_pekerjaan, on_delete=models.CASCADE)
    nominal_limit = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.id_jenis_pekerjaan} - {self.nominal_limit}"
    
class peminjaman(models.Model):
    id_peminjaman = models.AutoField(primary_key=True)
    id_nasabah = models.ForeignKey(nasabah, on_delete=models.CASCADE)
    id_limit_peminjaman = models.ForeignKey(limit_peminjaman, on_delete=models.CASCADE)
    jumlah_peminjaman = models.DecimalField(max_digits=12,decimal_places=2)
    tanggal_pengajuan = models.DateField()
    periode_peminjaman = models.PositiveIntegerField()
    status_peminjaman = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.id_nasabah} - {self.tanggal_pengajuan} - {self.status_peminjaman}"
    


    
