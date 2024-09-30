from django.shortcuts import render, redirect 
from . import models 
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .decorators import role_required

# Create your views here.

def loginview(request) : 
    if request.user.is_authenticated :
        group = None 
        if request.user.groups.exists() : 
            group = request.user.groups.all()[0].name

        if group == 'nasabah' : 
            return redirect('read_peminjaman') 
        elif group in ['admin','owner'] : 
            return redirect('read_peminjaman')
        else :
            return redirect('read_peminjaman')
    else : 
        return render(request, "base/login.html")

def performlogin(request) : 
    if request.method !="POST" :
        return HttpResponse("Method not Allowed")
    else:
        username_login = request.POST['username']
        password_login = request.POST['password'] 
        userobj = authenticate(request, username=username_login, password=password_login)
        if userobj is not None : 
            login(request, userobj) 
            messages.success(request, "Login success")
            if userobj.groups.filter(name='admin').exists() or userobj.groups.filter(name='owner') : 
                return redirect("read_peminjaman") 
            elif userobj.groups.filter(name='nasabah').exists() : 
                return redirect("read_peminjaman")
            elif userobj.groups.filter(name='produksi').exists() :
                return redirect('read_peminjaman')
        else : 
            messages.error(request,"Username atau Password salah !!!")
            return redirect("login") 

@login_required(login_url="login")
def logoutview(request) : 
    logout(request)
    messages.info(request, "Berhasil Logout")
    return redirect('Login')

@login_required(login_url="login")
def performlogout(request) : 
    logout(request)
    return redirect("login")

#CRUD PEMINJAMAN
@role_required(['owner', 'admin', 'nasabah'])
def read_peminjaman(request) : 
    peminjamanobj = models.peminjaman.objects.all()
    if not peminjamanobj.exists() : 
        messages.error(request, "Data peminjaman Tidak Ditemukan!")

    return render(request, 'peminjaman/read_peminjaman.html', { 
        'peminjamanobj' : peminjamanobj
    })    

@login_required(login_url='login')
@role_required(['owner','admin'])
def create_peminjaman(request):
    if request.method == 'GET':
        return render(request, 'peminjaman/create_peminjaman.html')

    else :
        jumlah_peminjaman = request.POST['jumlah_peminjaman']
        tanggal_pengajuan = request.POST['tanggal_pengajuan']
        periode_peminjaman = request.POST['periode_peminjaman']

        peminjamanobj = models.peminjaman.objects.filter(jumlah_peminjaman = jumlah_peminjaman, id_nasabah__nama_nasabah = nama_nasabah)
        if peminjamanobj.exist():
            messages.error(request, 'peminjaman sudah ada')

        else :
            models.peminjaman(
                id_nasabah = models.nasabah.objects.get(jumlah_peminjaman = jumlah_peminjaman),
                tanggal_pengajuan = tanggal_pengajuan,
                periode_peminjaman = periode_peminjaman,
            ).save()
            mesaages.success(request, 'Data peminjaman Berhasil Ditambahkan!')

        return redirect('read_peminjaman')
            
@login_required(login_url='login')
@role_required(['owner'])
def update_peminjaman(request, id):
    nasabahobj = models.grade.objects.all()
    getpeminjaman = models.peminjaman.objects.get(id_peminjaman = id)
    nama_nasabah = getpeminjaman.id_nasabah.nama_nasabah
    if request.method == 'GET':
        return render(request, 'peminjaman/update_peminjaman.html', {
            'getpeminjaman' : getpeminjaman,
            'nama_nasabah' : nama_nasabah,
            'nasabahobj' : nasabahobj,
            'id' : id
        })
    
    else :
        nama_nasabah = request.POST['nama_nasabah']
        jumlah_peminjaman = request.POST['jumlah_peminjaman']
        tanggal_pengajuan = request.POST['tanggal_pengajuan']
        periode_peminjaman = request.POST['periode_peminjaman']

        peminjamanobj = models.peminjaman.objects.filter(nama_peminjaman = nama_peminjaman, id_nasabah__nama_nasabah = nama_nasabah)
        if peminjamanobj.exist() and getpeminjaman.jumlah_peminjaman != jumlah_peminjaman and getpeminjaman.id_nasabah.nama_nasabah != nama_nasabah :
            messages.error(request, 'Data peminjaman Sudah Ada!')
            return redirect('update_peminjaman', id)

        getpeminjaman.id_peminjaman = getpeminjaman.id_peminjaman
        getpeminjaman.id_nasabah = models.nasabah.objects.get(nama_nasabahh = nama_nasabah)
        getpeminjaman.jumlah_peminjaman = jumlah_peminjaman
        getpeminjaman.tanggal_pengajuan = tanggal_pengajuan
        getpeminjaman.periode_peminjaman = periode_peminjaman

        getpeminjaman.save()

        messages.succes(request, 'Data peminjaman berhasil diperbarui!')
        return redirect('read_peminjaman')

@login_required(login_url='login')
@role_required(['owner'])
def delete_peminjaman(request, id):
    getpeminjaman = models.peminjaman.objects.get(id_peminjaman = id)
    getpeminjaman.delete()

    messages.error(request, "Data peminjaman berhasil dihapus!")
    return redirect('read_peminjaman')

#CRUD JENIS PEKERJAAN
@login_required(login_url='login')
@role_required(['owner', 'admin', 'nasabah'])
def read_jenis_pekerjaan(request) : 
    jenis_pekerjaanobj = models.jenis_pekerjaan.objects.all()
    if not jenis_pekerjaanobj.exists() : 
        messages.error(request, "Jenis Pekerjaan Tidak Ditemukan!")

    return render(request, 'jenis_pekerjaan/read_jenis_pekerjaan.html', { 
        'jenis_pekerjaanobj' : jenis_pekerjaanobj
    })    

@login_required(login_url='login')
@role_required(['owner'])
def create_jenis_pekerjaan(request):
    if request.method == 'GET':
        return render(request, 'jenis_pekerjaan/create_jenis_pekerjaan.html')

    else :
        nama_pekerjaan = request.POST['nama_pekerjaan']
        penghasilan_perbulan = request.POST['penghasilan_perbulan']

        jenis_pekerjaanobj = models.jenis_pekerjaan.objects.filter(nama_pekerjaan = nama_pekerjaan)
        if jenis_pekerjaanobj.exists():
            messages.error(request, 'Jenis Pekerjaan sudah ada')
            return redirect('create_jenis_pekerjaan')
        else :
            models.jenis_pekerjaan(
                nama_pekerjaan = nama_pekerjaan,
                penghasilan_perbulan = penghasilan_perbulan,
            ).save()
            messages.success(request, 'Jenis Pekerjaan berhasil ditambahkan!')
            return redirect('read_jenis_pekerjaan')

@login_required(login_url='login')
@role_required(['owner'])
def update_jenis_pekerjaan(request, id):
    getjenis_pekerjaan = models.jenis_pekerjaan.objects.get(id_jenis_pekerjaan = id)
    if request.method == 'GET':
        return render(request, 'jenis_pekerjaan/update_jenis_pekerjaan.html', {
            'getjenis_pekerjaan' : getjenis_pekerjaan,
        })
    
    else :
        nama_pekerjaan = request.POST['nama_pekerjaan']
        penghasilan_perbulan = request.POST['penghasilan_perbulan']
       
        getjenis_pekerjaan.id_jenis_pekerjaan = getjenis_pekerjaan.id_jenis_pekerjaan
        getjenis_pekerjaan.nama_pekerjaan = nama_pekerjaan
        getjenis_pekerjaan.penghasilan_perbulan = penghasilan_perbulan
        getjenis_pekerjaan.save()
        messages.success(request, 'Data Jenis Pekerjaan berhasil diperbarui!')
        return redirect('read_jenis_pekerjaan')

@login_required(login_url='login')
@role_required(['owner'])
def delete_jenis_pekerjaan(request, id):
    getjenis_pekerjaan = models.jenis_pekerjaan.objects.get(id_jenis_pekerjaan = id)
    getjenis_pekerjaan.delete()

    messages.error(request, "Data Jenis Pekerjaan berhasil dihapus!")
    return redirect('read_jenis_pekerjaan')

#CRUD NASABAH
@login_required(login_url='login')
@role_required(['owner', 'admin', 'nasabah'])
def read_nasabah(request) : 
    nasabahobj = models.nasabah.objects.all()
    if not nasabahobj.exists() : 
        messages.error(request, "Data Nasabah Tidak Ditemukan!")

    return render(request, 'nasabah/read_nasabah.html', { 
        'nasabahobj' : nasabahobj
    })    

@login_required(login_url='login')
@role_required(['owner','nasabah'])
def create_nasabah(request):
    if request.method == 'GET':
        return render(request, 'nasabah/create_nasabah.html')

    else :
        nama_pekerjaan = request.POST['nama_pekerjaan']
        nama_nasabah = request.POST['nama_nasabah']
        umur_nasabah = request.POST['umur_nasabah']
        jenis_kelamin = request.POST['jenis_kelamin']
        alamat_nasabah = request.POST['alamat_nasabah']
        nama_perusahaan = request.POST['nama_perusahaan']
        tingkat_pendidikan = request.POST['tingkat_pendidikan']
        status_pernikahan = request.POST['status_pernikahan']
        nama_orang_tua = request.POST['nama_orang_tua']
        nama_lengkap_kontak_darurat = request.POST['nama_lengkap_kontak_darurat']
        nomor_kontak_darurat = request.POST['nomor_kontak_darurat']
        hubungan_dengan_peminjam = request.POST['hubungan_dengan_peminjam']
        sisa_kontrak_kerja = request.POST['sisa_kontrak_kerja']

        models.nasabah(
            id_jenis_pekerjaan = models.jenis_pekerjaan.objects.get(nama_pekerjaan = nama_pekerjaan),
            nama_nasabah = nama_nasabah,
            umur_nasabah = umur_nasabah,
            jenis_kelamin = jenis_kelamin,
            alamat_nasabah = alamat_nasabah
            nama_perusahaan = nama_perusahaan,
            tingkat_pendidikan = tingkat_pendidikan,
            status_pernikahan = status_pernikahan,
            nama_orang_tua = nama_orang_tua,
            nama_lengkap_kontak_darurat = nama_lengkap_kontak_darurat,
            nomor_kontak_darurat = nomor_kontak_darurat,
            hubungan_dengan_peminjam = hubungan_dengan_peminjam,
            sisa_kontrak_kerja = sisa_kontrak_kerja,
        ).save()
        messages.success(request, 'Data Nasabah berhasil ditambahkan!')

        return redirect('read_nasabah')

@login_required(login_url='login')
@role_required(['owner','nasabah'])
def update_nasabah(request, id):
    getnasabah = models.nasabah.objects.get(id_nasabah = id)
    if request.method == 'GET':
        return render(request, 'nasabah/update_nasabah.html', {
            'getnasabah' : getnasabah,
        })
    
    else :
        nama_nasabah = request.POST['nama_nasabah']
        umur_nasabah = request.POST['umur_nasabah']
        jenis_kelamin = request.POST['jenis_kelamin']
        alamat_nasabah = request.POST['alamat_nasabah']
        nama_perusahaan = request.POST['nama_perusahaan']
        tingkat_pendidikan = request.POST['tingkat_pendidikan']
        status_pernikahan = request.POST['status_pernikahan']
        nama_orang_tua = request.POST['nama_orang_tua']
        nama_lengkap_kontak_darurat = request.POST['nama_lengkap_kontak_darurat']
        nomor_kontak_darurat = request.POST['nomor_kontak_darurat']
        hubungan_dengan_peminjam = request.POST['hubungan_dengan_peminjam']
        sisa_kontrak_kerja = request.POST['sisa_kontrak_kerja']
       
        getnasabah.id_nasabah = getnasabah.id_nasabah
        getnasabah.nama_nasabah = nama_nasabah
        getnasabah.umur_nasabah = umur_nasabah
        getnasabah.jenis_kelamin = jenis_kelamin
        getnasabah.alamat_nasabah = alamat_nasabah
        getnasabah.nama_perusahaan = nama_perusahaan
        getnasabah.tingkat_pendidikan = tingkat_pendidikan
        getnasabah.status_pernikahan = status_pernikahan
        getnasabah.nama_orang_tua = nama_orang_tua
        getnasabah.nama_lengkap_kontak_darurat = nama_lengkap_kontak_darurat
        getnasabah.nomor_kontak_darurat = nomor_kontak_darurat
        getnasabah.hubungan_dengan_peminjam = hubungan_dengan_peminjam
        getnasabah.sisa_kontrak_kerja = sisa_kontrak_kerja
        getnasabah.save()
        messages.success(request, 'Data Nasabah berhasil diperbarui!')
        return redirect('read_nasabah')

@login_required(login_url='login')
@role_required(['owner'])
def delete_nasabah(request, id):
    getnasabah = models.nasabah.objects.get(id_nasabah = id)
    getnasabah.delete()

    messages.error(request, "Data Nasabah berhasil dihapus!")
    return redirect('read_nasabah')

#CRUD LIMIT PEMINJAMAN
@login_required(login_url='login')
@role_required(['owner', 'admin', 'nasabah'])
def read_limit_peminjaman(request) : 
    limit_peminjamanobj = models.limit_peminjaman.objects.all()
    if not limit_peminjamanobj.exists() : 
        messages.error(request, "Limit Peminjaman tidak ditemukan!")

    return render(request, 'limit_peminjaman/read_limit_peminjaman.html', { 
        'limit_peminjamanobj' : limit_peminjamanobj
    })    

@login_required(login_url='login')
@role_required(['owner','admin'])
def create_limit_peminjaman(request):
    if request.method == 'GET':
        return render(request, 'limit_peminjaman/create_limit_peminjaman.html')

    else :
        nama_pekerjaan = request.POST['nama_pekerjaan']
        nominal_limit = request.POST['nominal_limit']

        models.jenis_pekerjaan(
            id_jenis_pekerjaan = models.jenis_pekerjaan.objects.get(nama_pekerjaan = nama_pekerjaan)
            nominal_limit = nominal_limit,
        ).save()
        messages.success(request, 'Limit Pekerjaan berhasil ditambahkan!')
        return redirect('read_limit_pekerjaan')

@login_required(login_url='login')
@role_required(['owner','admin'])
def update_limit_peminjaman(request, id):
    getlimit_peminjaman = models.limit_peminjaman.objects.get(id_limit_peminjaman = id)
    if request.method == 'GET':
        return render(request, 'limit_peminjaman/update_limit_peminjaman.html', {
            'getlimit_peminjaman' : getlimit_peminjaman,
        })
    
    else :
        nominal_limit - request.POST['nominal_limit']
       
        getlimit_peminjaman.id_limit_peminjaman = getlimit_peminjaman.id_limit_peminjaman
        getlimit_peminjaman.nominal_limit = nominal_limit
        getlimit_peminjaman.save()
        messages.success(request, 'Data Limit Peminjaman berhasil diperbarui!')
        return redirect('read_limit_peminjaman')

@login_required(login_url='login')
@role_required(['owner'])
def delete_limit_peminjaman(request, id):
    getlimit_peminjaman = models.limit_peminjaman.objects.get(id_limit_peminjaman = id)
    getlimit_peminjaman.delete()

    messages.error(request, "Data Limit Peminjaman berhasil dihapus!")
    return redirect('read_limit_peminjaman')