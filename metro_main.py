from serial import Serial, SEVENBITS, STOPBITS_ONE, PARITY_EVEN
from time import sleep

ser = Serial("/dev/ttyUSB0", 600, SEVENBITS, PARITY_EVEN, STOPBITS_ONE)
#ser = Serial("/dev/cu.UC-232AC", 600, SEVENBITS, PARITY_EVEN, STOPBITS_ONE)
STX = chr(2)
ETX = chr(3)
EOT = chr(4)
ENQ = chr(5)
NL = chr(10)
PAD = chr(127)
NULL = chr(0)

addr = "01" # low bit says write
def wr(x):
  ser.write(PAD + PAD + x + PAD + PAD)

slp = 1 # sometimes even smaller works, sometimes need to retry with this

col = "B" # magic numbers
ver = "004"
mempos = "01"
col2 = "D"

wr(EOT)
sleep(slp)
wr(addr + ENQ)
sleep(slp)

row = "1"
rivi1 = "raspberry"
wr(STX + row + col + ver + mempos + col2 + rivi1 + ETX + "p")
sleep(slp)
wr(EOT)

wr(EOT)
sleep(slp)
wr(addr + ENQ)
sleep(slp)

row = "2"
rivi2 = "error"
wr(STX + row + col + ver + mempos + col2 + rivi2 + ETX + "p")
sleep(slp)
wr(EOT)
