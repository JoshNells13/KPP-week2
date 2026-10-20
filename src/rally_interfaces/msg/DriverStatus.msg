uint8 WAITING_START=0         # menunggu aba-aba mulai
uint8 DRIVING=1               # sedang maju
uint8 TURNING=2               # sedang belok
uint8 WAITING_INSTRUCTION=3   # antrean kosong, maju lurus menunggu instruksi
uint8 FINISHED=4              # instruksi terakhir selesai atau lomba berakhir

uint8 state
float32 x                     # posisi [m]
float32 y
float32 theta                 # arah [rad]
uint32 current_id             # instruksi yang sedang dijalankan, 0 jika tidak ada
uint32 done_id                # instruksi terakhir yang sudah selesai, 0 jika belum ada
uint8 queued                  # jumlah instruksi yang menunggu di antrean
