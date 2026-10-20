uint8 TURN_NONE=0     # tidak belok, ini instruksi terakhir
uint8 TURN_LEFT=1     # belok kiri 90 derajat
uint8 TURN_RIGHT=2    # belok kanan 90 derajat

uint32 id             # mulai dari 1, naik satu per instruksi
uint8 distance        # maju sejauh ini terlebih dahulu, nilai boleh 0
uint8 turn            # lalu belok 90 derajat, atau TURN_NONE di akhir
