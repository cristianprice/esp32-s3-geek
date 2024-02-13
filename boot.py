import machine
import sdcard
import uos

# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(34, machine.Pin.OUT)

# Intialize SPI peripheral (start with 1 MHz)
spi = machine.SoftSPI(
                  baudrate=10000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(36),
                  mosi=machine.Pin(35),
                  miso=machine.Pin(37))

# Initialize SD card
sd = sdcard.SDCard(spi=spi, cs=cs,baudrate=5_000_000)

# Mount filesystem
uos.mount(sd, '/sd')

