import epd7in5b_V2
import time

print("Starting shut down")
epd = epd7in5b_V2.EPD()
epd.init()
time.sleep(1)
print("Clearing...")
epd.Clear()
time.sleep(2)
print("Exiting !")
epd7in5b_V2.epdconfig.module_exit(cleanup=True)
print("Bye")
exit()
