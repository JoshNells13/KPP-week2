# Task 3 : Navigator

Navigator adalah Coach yang duduk di sebelah Miru. Ia memegang peta lintasan, mencari rute terpendek, lalu membacakannya sedikit demi sedikit sebagai instruksi. Aturan lomba, spesifikasi instruksi, dan tabel antarmuka ada di [Task 1](/README.md).

Edit `route.py` dan `navigator_node.py` di `src/rally_navigator`. Bagian B sampai D adalah fungsi biasa, jadi bisa dikerjakan tanpa ROS dan tanpa menunggu pasanganmu.

## Soal (_Tasks_)

### A. Menerima Peta _(6 Points)_

Terima peta lintasan dari wasit.

- Subscribe ke topic peta dengan QoS `transient_local`, karena peta cuma dikirim sekali dan navigator bisa menyala terlambat.
- Tolak peta yang rusak, dan abaikan peta kedua.

#### Contoh Output:
Peta dikirim tanpa wasit:
```
ros2 topic pub --once --qos-durability transient_local --qos-reliability reliable /race/map rally_interfaces/msg/RaceMap "{width: 3, height: 3, rocks: [0,0,0, 1,1,0, 0,0,0], start_col: 0, start_row: 0, finish_col: 0, finish_row: 2}"
```
```
[navigator] peta diterima: 3x3, 2 batu, start (0, 0), finis (0, 2)
```

Note : Rute dan instruksinya baru muncul setelah bagian B sampai D selesai.

### B. Mencari Rute _(8 Points)_

Cari rute terpendek dari start ke finis dengan BFS.

- Telusuri peta kotak demi kotak dari start. Kotak yang pertama kali ditemukan lewat jalur terpendek.
- Batu tidak boleh dilewati.
- Urutan tetangga: timur, utara, barat, selatan.
- Kalau tidak ada jalan, hasilnya kosong.

#### Contoh Output:
Semua tes lolos:
```
test_find_route.py ......
```

Note : Kamu cukup mengisi pencariannya, penyusunan rute (`trace_back`) sudah disediakan.

### C. Rute Menjadi Arah _(6 Points)_

Ubah rute (daftar kotak) jadi daftar arah per langkah.

- Arah dikodekan 0 untuk timur, 1 utara, 2 barat, 3 selatan.
- Rute dengan N kotak menghasilkan N - 1 arah.

#### Contoh Output:
Semua tes lolos:
```
test_directions.py .....
```

### D. Arah Menjadi Instruksi _(8 Points)_

Gabungkan arah yang lurus berturut-turut jadi instruksi "maju sekian, lalu belok".

- Langkah pertama bukan ke timur: belok dulu, instruksi pertama berjarak 0.
- Putar balik 180° ditulis dua belokan kiri, yang kedua berjarak 0.
- Instruksi terakhir tanpa belokan (`TURN_NONE`).

#### Contoh Output:
Semua tes lolos:
```
test_instructions.py .......
```

### E. Mengirim Instruksi _(6 Points)_

Kirim instruksi ke Miru, dan tambah lagi setiap kali Miru melapor ada yang selesai.

- Navigator mengirim kalau sudah ada rute, Miru sudah melapor sekali, dan ada yang subscribe topic instruksi.
- Jaga sejumlah instruksi di depan `done_id` Miru. Untuk sekarang pakai konstanta `DEFAULT_INSTRUCTIONS_AHEAD` (nilainya 2).
- Setiap instruksi hanya dikirim sekali.

#### Contoh Output:
Tanpa Miru asli (setelah peta bagian A dikirim), dengan `ros2 topic echo /navigator/instruction` di terminal lain dan `ros2 topic pub -r 5 /miru/status rally_interfaces/msg/DriverStatus "{state: 3, done_id: 0}"`:
```
[navigator] kirim instruksi 1: ...
[navigator] kirim instruksi 2: ...
```

Note : Masing-masing sekali saja. Kalau `done_id` diganti jadi 2, instruksi 3 terkirim.

### F. Parameter `instructions_ahead` _(6 Points)_

Ganti konstanta tadi dengan parameter yang bisa diatur.

- Daftarkan parameter `instructions_ahead`. Nilai di luar `MIN_INSTRUCTIONS_AHEAD` sampai `MAX_INSTRUCTIONS_AHEAD` ditolak.
- Jumlah instruksi di depan `done_id` mengikuti nilai parameter.

#### Contoh Output:
```
ros2 param set /navigator instructions_ahead 0     -> ditolak
ros2 param set /navigator instructions_ahead 6     -> ditolak
ros2 param set /navigator instructions_ahead 1     -> diterima
```

Note : Ulangi uji bagian E dengan nilai 1: `done_id: 0` hanya mengirim instruksi 1, dan instruksi 2 baru terkirim saat `done_id: 1`.

### G. Bonus: DFS lawan BFS _(+10 Points)_

BFS menjamin rute terpendek. Bagaimana kalau memakai DFS (depth-first search)? Tulis versi DFS dan bandingkan dengan BFS.

- Tulis `find_route_dfs(grid)` di `route.py`. Urutan tetangganya sama dengan BFS (timur, utara, barat, selatan), dan hasilnya juga rute dalam bentuk daftar kotak.
- Buat skrip kecil sendiri (tanpa ROS) yang membuat peta untuk seed 1 sampai 10 dengan `generate_stage(seed)` dari paket wasit, lalu hitung untuk BFS dan DFS: panjang rute dan jumlah kotak yang dikunjungi sebelum finis ditemukan.
- Ganti pencarian di `navigator_node.py` dengan DFS, lalu jalankan lomba untuk dua seed dan catat waktu lombanya untuk BFS dan DFS.
- Hasilnya dibuat tabel seed × (panjang rute, kotak dikunjungi, waktu lomba) untuk BFS dan DFS, disertai penjelasan singkat kenapa hasilnya berbeda.

#### Contoh Output:
Tabel di laporan (angka hanya contoh):

| Seed | Panjang BFS | Panjang DFS | Dikunjungi BFS | Dikunjungi DFS | Waktu BFS | Waktu DFS |
|---|---|---|---|---|---|---|
| 7 | 18 | 34 | 71 | 36 | 27,3 s | 49,5 s |

Note : Tes bawaan hanya untuk BFS. Kembalikan navigator ke BFS setelah selesai mengukur.
