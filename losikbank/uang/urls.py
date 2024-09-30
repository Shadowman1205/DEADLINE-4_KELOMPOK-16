from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginview, name='login'),
    path('performlogin', views.performlogin, name="performlogin"),
    path('performlogout', views.performlogout, name="performlogout"),
    #CRUD Peminjaman
    path('create_peminjaman', views.create_peminjaman, name='create_peminjaman'),
    path('read_peminjaman', views.read_peminjaman, name='read_peminjaman'),
    path('update_peminjaman/<str:id>', views.update_peminjaman, name='update_peminjaman'),
    path('delete_peminjaman/<str:id>', views.delete_peminjaman, name='delete_peminjaman'),
    #CRUD Jenis Pekerjaan
    path('create_jenis_pekerjaan', views.create_jenis_pekerjaan, name='create_jenis_pekerjaan'),
    path('read_jenis_pekerjaan', views.read_jenis_pekerjaan, name='read_jenis_pekerjaan'),
    path('update_jenis_pekerjaan/<str:id>', views.update_jenis_pekerjaan, name='update_jenis_pekerjaan'),
    path('delete_jenis_pekerjaan/<str:id>', views.delete_jenis_pekerjaan, name='delete_jenis_pekerjaan'),
    #CRUD Nasabah
    path('create_nasabah', views.create_nasabah, name='create_nasabah'),
    path('read_nasabah', views.read_nasabah, name='read_nasabah'),
    path('update_nasabah/<str:id>', views.update_nasabah, name='update_nasabah'),
    path('delete_nasabah/<str:id>', views.delete_nasabah, name='delete_nasabah'),
    #CRUD Limit Peminjaman
    path('create_limit_peminjaman', views.create_limit_peminjaman, name='create_limit_peminjaman'),
    path('read_limit_peminjaman', views.read_limit_peminjaman, name='read_limit_peminjaman'),
    path('update_limit_peminjaman/<str:id>', views.update_limit_peminjaman, name='update_limit_peminjaman'),
    path('delete_limit_peminjaman/<str:id>', views.delete_limit_peminjaman, name='delete_limit_peminjaman'),
]

