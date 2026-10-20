uint8 PREPARING=0     # menunggu miru available
uint8 COUNTDOWN=1
uint8 GO=2
uint8 FINISHED=3      # Miru sampai di kotak finish
uint8 FAILED=4        # keluar lintasan atau waktu habis

uint8 state
float32 elapsed       # waktu lomba sejak GO [s]
float32 penalty       # total penalti [s]
