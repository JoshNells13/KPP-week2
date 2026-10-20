# Task 2 : Miru

Miru adalah pembalap yang hanya bisa menjalankan perintah. Ia tidak tahu peta, jadi ia mengandalkan instruksi dari navigator, menggerakkan kura-kura lewat turtlesim, dan terus melapor ke navigator. Aturan lomba, spesifikasi instruksi, dan tabel antarmuka ada di [Task 1](/README.md).

Edit `instruction_queue.py`, `motion.py`, dan `miru_node.py` di `src/rally_miru`.

## Soal (_Tasks_)

### A. Antrean Instruksi _(6 Points)_

Simpan instruksi dari navigator di antrean, dan abaikan instruksi yang `id`-nya sudah pernah diterima.

- Subscribe ke topic instruksi, lalu masukkan setiap instruksi ke antrean.
- Instruksi dengan `id` yang sama atau lebih kecil dari yang sudah diterima diabaikan.
- Instruksi yang diterima ditampilkan di log, yang diabaikan cukup log debug.

#### Contoh Output:
Instruksi `{id: 1, distance: 3, turn: 0}` dikirim dua kali lewat `ros2 topic pub`:
```
[miru] instruksi 1: maju 3, finis
```

Note : Hanya muncul satu kali. Tesnya `test/test_queue.py` (6 tes).

### B. Pose dan Perintah Gerak _(6 Points)_

Buat Miru bisa menggerakkan kura-kura dan tahu posisinya.

- Buat publisher untuk perintah gerak kura-kura.
- Buat subscriber untuk posisi kura-kura, dan simpan pose terbaru.

#### Contoh Output:
Keluaran `ros2 node info /miru` memuat:
```
Subscribers:
  /turtle1/pose: turtlesim/msg/Pose
Publishers:
  /turtle1/cmd_vel: geometry_msgs/msg/Twist
```

### C. Aba-aba GO dan Parameter _(6 Points)_

Buat Miru baru berjalan saat aba-aba GO, dan kecepatannya bisa diatur.

- Subscribe ke status lomba dan simpan status terbarunya.
- Daftarkan parameter `speed`. Nilai di luar `MIN_SPEED` sampai `MAX_SPEED` ditolak.

#### Contoh Output:
```
ros2 param set /miru speed 3.0       -> ditolak
ros2 param set /miru speed 0.05      -> ditolak
ros2 param set /miru speed 2.5       -> diterima
```

Note : Efek GO baru kelihatan setelah bagian D selesai.

### D. Maju _(8 Points)_

Buat Miru maju sekian kotak lalu berhenti pas di tengah kotak tujuan.

- Hitung titik tujuan dari posisi **rencana** (`planned_x`, `planned_y`), bukan dari posisi nyata.
- Miru terus maju sampai sisa jarak ke tujuan nol atau negatif, lalu berhenti.
- Kura-kura selalu berhenti sedikit melewati target karena ada jeda antara perintah dan gerakannya, sekitar 0,1 m untuk setiap 1 m/s.

#### Contoh Output:
Dengan GO palsu (`ros2 topic pub -r 5 /race/state rally_interfaces/msg/RaceState "{state: 2}"`) dan instruksi `{id: 1, distance: 3, turn: 0}`, kura-kura maju sekitar 3 m ke timur lalu berhenti:
```
[miru] instruksi 1 selesai, finis
```

Note : Butuh bagian A, B, dan C. Tesnya `test/test_forward.py`

### E. Belok _(8 Points)_

Buat Miru belok kiri atau kanan 90 derajat.

- Belok kiri menambah sudut, belok kanan mengurangi.
- Hasilnya dirapikan dengan `wrap_angle` supaya tetap di rentang -π sampai π.
- Miru berputar sampai selisih sudut ke arah tujuan cukup kecil, lalu berhenti. Gunakan fungsi `turn_rate` yang sudah disediakan.

#### Contoh Output:
Dengan GO palsu seperti bagian D, instruksi `{id: 1, distance: 0, turn: 1}` lalu `{id: 2, distance: 0, turn: 2}`:
```
ros2 topic echo --once /turtle1/pose --field theta    -> sekitar 1.57 (setelah belok kiri)
ros2 topic echo --once /turtle1/pose --field theta    -> sekitar 0    (setelah belok kanan)
```

Note : Tesnya `test/test_turn.py`

### F. Laporan Status _(6 Points)_

Buat Miru melapor ke navigator 20 kali per detik.

- Kirim `DriverStatus` berisi state, posisi, arah, `current_id`, `done_id`, dan jumlah antrean.
- Jangan kirim kalau pose pertama belum datang.

#### Contoh Output:
```
ros2 topic hz /miru/status    -> sekitar 20 Hz
```

Note : Isi laporan bisa dilihat dengan `ros2 topic echo /miru/status`.

### G. Bonus: Berhenti Lebih Tepat _(+10 Points)_

Saat berhenti, kura-kura selalu melewati tengah kotak tujuan karena ada jeda antara perintah dan gerakannya. Semakin cepat, semakin jauh lewatnya (sekitar 0,1 m untuk setiap 1 m/s). Kurangi galat itu.

- Ubah cara Miru maju di bagian D supaya berhenti lebih dekat ke tengah kotak, misalnya melambat saat mendekati target.
- Ukur sendiri galat berhenti, yaitu selisih posisi akhir kura-kura dengan titik tujuan, untuk kecepatan 0,5, 1,0, dan 2,5 m/s. Ukur sebelum dan sesudah perbaikan, masing-masing untuk satu instruksi maju 3 kotak.
- Ukur juga waktu tempuh instruksi itu pada setiap percobaan.
- Hasilnya dibuat tabel kecepatan × (galat, waktu) untuk versi lama dan versi baru.

#### Contoh Output:
Tabel di laporan (angka hanya contoh):

| Kecepatan | Galat lama | Waktu lama | Galat baru | Waktu baru |
|---|---|---|---|---|
| 0,5 m/s | 0,05 m | 6,0 s | 0,01 m | 6,8 s |
| 1,0 m/s | 0,10 m | 3,0 s | 0,02 m | 3,9 s |
| 2,5 m/s | 0,25 m | 1,2 s | 0,04 m | 2,3 s |

Note : Posisi akhir bisa dibaca dengan `ros2 topic echo --once /turtle1/pose`. Tidak ada tes bawaan untuk bagian ini. Hati-hati, perbaikanmu tidak boleh membuat bagian D yang lama gagal dites.

## Tips

- Bagian D dan E bisa diuji dengan `pytest` tanpa pasangan, jadi kerjakan fungsi di `motion.py` lebih dulu.
- `ros2 run rally_miru miru --ros-args --log-level debug` menampilkan perpindahan state Miru. Alurnya ada di komentar di atas kelas `MiruNode`.
- Miru bergerak 100 kali per detik dari timer `update`, jadi `drive_step` dan `turn_step` harus singkat dan tidak boleh menunggu.
- Kalau Miru berhenti di tengah lintasan, lihat `ros2 topic echo /miru/status`: `state: 3` berarti antrean kosong dan navigator belum mengirim instruksi berikutnya. Kalau navigator tidak ada sama sekali, Miru maju lurus terus.
- Kalau Miru melenceng ke kotak lain, hampir selalu karena target dihitung dari posisi nyata, bukan posisi rencana.
- Kalau Miru berputar ke arah yang salah, periksa tanda sudut: belok kiri menambah sudut (berlawanan jarum jam), belok kanan mengurangi.
