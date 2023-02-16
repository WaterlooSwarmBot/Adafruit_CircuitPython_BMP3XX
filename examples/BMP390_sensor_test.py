import time
import board
import adafruit_bmp3xx
from adafruit_bmp3xx import PowerMode, ODRMode
import digitalio
import enum
spi = board.SPI()
cs = digitalio.DigitalInOut(board.D5)
bmp = adafruit_bmp3xx.BMP3XX_SPI(spi, cs)
bmp.sea_level_pressure = 1013.25

bmp.pressure_oversampling = 8
bmp.temperature_oversampling = 4
bmp.filter_coefficient = 2


print(bmp.power_mode)

ODR = ODRMode.ODR_25
bmp.output_data_rate = ODR
print(bmp.output_data_rate)
sample_wait = 1/ODR - 0.002
samples = 1000

n = 0

while n < samples:    
    print("Pressure: {:6.2f}".format(bmp.pressure))
    print("Temperature: {:6.2f}".format(bmp.temperature))
    n += 1
    time.sleep(0.1)
