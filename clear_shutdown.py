import logging
import os
import time

import epd7in5b_V2

logger = logging.getLogger(__name__)
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "conf/logging/main_error.log")
logging.basicConfig(
    filename=filename,
    encoding="utf-8",
    format="%(asctime)s %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)

try:
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
except Exception as e:
    logger.warning(f"Clear shutdown failded: {e}")
