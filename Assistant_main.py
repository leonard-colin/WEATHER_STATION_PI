# -*- coding:utf-8 -*-
import argparse
import logging
import os
from datetime import time

import colorama
from colorama import Fore, Style
from dotenv import load_dotenv

from display import *
from news import *
from tools import graph
from weather import *

logger = logging.getLogger(__name__)
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "conf/logging/main_error.log")
logging.basicConfig(
    filename=filename,
    filemode="a",
    encoding="utf-8",
    format="%(asctime)s %(levelname)s %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)
load_dotenv()
colorama.init(autoreset=True)

# Paris
lat = "48.864716"
lon = "2.349014"
api_key_weather = os.environ.get("WEATHER_API_KEY")
api_key_news = os.environ.get("NEWS_API_KEY")
debug = 0
if debug == 0:
    import epd7in5b_V2


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--show-graph", help="Display bottom graphs", action="store_true"
    )
    parser.add_argument("--debug", help="debug mode", action="store_true")
    args = parser.parse_args()
    return args


def check_for_shutdown():
    args = parse_arguments()
    if not args.debug:
        current_time = time.strftime("%H:%M", time.localtime())
        if "00:00" <= current_time <= "06:00":
            try:
                epd7in5b_V2.epdconfig.module_exit(cleanup=True)
                exit()
            except Exception as e:
                logger.warning(f"Could not shutdown: {e}")


def main():
    args = parse_arguments()

    ##################################################################################################################
    # FRAME
    display.draw_black.rectangle(
        (5, 5, 795, 475), fill=255, outline=0, width=2
    )  # INNER FRAME
    # display.draw_black.line((540, 5, 540, 350), fill=0, width=1)  # VERTICAL SEPARATION
    display.draw_black.line(
        (350, 5, 350, 350), fill=0, width=1
    )  # VERTICAL SEPARATION slim
    display.draw_black.line(
        (5, 350, 795, 350), fill=0, width=1
    )  # HORIZONTAL SEPARATION

    # UPDATED AT
    display.draw_black.text(
        (10, 8), f"Mis à jour le {weather.current_time()}", fill=0, font=font8
    )

    ###################################################################################################################
    # CURRENT WEATHER
    display.draw_black.text((225, 150), "PARIS", fill=0, font=font16)
    display.draw_icon(
        20, 55, "r", 75, 75, weather.weather_description(weather.current_weather())[0]
    )  # CURRENT WEATHER ICON
    display.draw_black.text(
        (120, 15), weather.current_temp(), fill=0, font=font48
    )  # CURRENT TEMP
    display.draw_black.text(
        (230, 15), weather.current_hum(), fill=0, font=font48
    )  # CURRENT HUM
    display.draw_black.text(
        (245, 65), "Humidité", fill=0, font=font12
    )  # LABEL "HUMIDITY"
    display.draw_black.text(
        (120, 75),
        f"{weather.current_wind()[0]} {weather.current_wind()[1]}",
        fill=0,
        font=font24,
    )

    display.draw_icon(120, 105, "b", 35, 35, "sunrise")  # SUNRISE ICON
    display.draw_black.text(
        (160, 110), weather.current_sunrise(), fill=0, font=font16
    )  # SUNRISE TIME
    display.draw_icon(220, 105, "b", 35, 35, "sunset")  # SUNSET ICON
    display.draw_black.text(
        (260, 110), weather.current_sunset(), fill=0, font=font16
    )  # SUNSET TIME

    ###################################################################################################################
    # NEXT HOUR RAIN
    try:
        data_rain = weather.rain_next_hour()

        # FRAME
        display.draw_black.text(
            (20, 150),
            "Pluie dans l'heure - " + time.strftime("%H:%M", time.localtime()),
            fill=0,
            font=font16,
        )  # NEXT HOUR RAIN LABEL
        display.draw_black.rectangle(
            (20, 175, 320, 195), fill=255, outline=0, width=1
        )  # Red rectangle = rain

        # LABEL
        for i in range(len(data_rain)):
            display.draw_black.line(
                (20 + i * 50, 175, 20 + i * 50, 195), fill=0, width=1
            )
            display.draw_black.text(
                (20 + i * 50, 195), data_rain[i][0], fill=0, font=font16
            )
            if data_rain[i][1] != 0:
                display.draw_red.rectangle(
                    (20 + i * 50, 175, 20 + (i + 1) * 50, 195), fill=0
                )
    except Exception:
        pass

    ###################################################################################################################
    # HOURLY FORECAST
    hourly_min_left = 30
    hourly_min_up = 227

    # Define the horizontal spacing between hourly forecast periods
    horizontal_spacing = 120

    # Iterate over hourly forecast periods
    for i, forecast_period in enumerate(["+3h", "+6h", "+12h"]):
        # Calculate position based on index
        current_left = hourly_min_left + i * horizontal_spacing

        # Draw label
        display.draw_black.text(
            (current_left, hourly_min_up), forecast_period, fill=0, font=font16
        )

        # Draw weather icon
        display.draw_icon(
            current_left - 5,
            hourly_min_up + 20,
            "r",
            50,
            50,
            weather.weather_description(
                weather.hourly_forecast()[forecast_period]["id"]
            )[0],
        )

        # Draw weather description
        display.draw_black.text(
            (current_left, hourly_min_up + 70),
            weather.weather_description(
                weather.hourly_forecast()[forecast_period]["id"]
            )[1],
            fill=0,
            font=font12,
        )

        # Draw temperature
        display.draw_black.text(
            (current_left, hourly_min_up + 85),
            weather.hourly_forecast()[forecast_period]["temp"],
            fill=0,
            font=font16,
        )

        # Draw rain probability
        display.draw_black.text(
            (current_left, hourly_min_up + 100),
            weather.hourly_forecast()[forecast_period]["pop"],
            fill=0,
            font=font16,
        )

    ###################################################################################################################
    # DAILY FORECAST
    min_left = 20
    min_up = 355

    # Define the horizontal spacing between days
    horizontal_spacing = 200

    # Iterate over forecast periods
    for i, forecast_period in enumerate(["+24h", "+48h", "+72h", "+96h"]):
        # Calculate position based on index
        current_left = min_left + i * horizontal_spacing

        # Draw day
        display.draw_black.text(
            (current_left, min_up),
            weather.daily_forecast()[forecast_period]["date"],
            fill=0,
            font=font16,
        )

        # Draw weather icon
        display.draw_icon(
            current_left,
            min_up + 40,
            "r",
            50,
            50,
            weather.weather_description(
                weather.daily_forecast()[forecast_period]["id"]
            )[0],
        )

        # Draw min temperature
        display.draw_black.text(
            (current_left + 60, min_up + 40),
            weather.daily_forecast()[forecast_period]["min"],
            fill=0,
            font=font14,
        )
        display.draw_black.text(
            (current_left + 60, min_up + 60),
            weather.daily_forecast()[forecast_period]["max"],
            fill=0,
            font=font14,
        )
        display.draw_black.text(
            (current_left + 60, min_up + 80),
            weather.daily_forecast()[forecast_period]["pop"],
            fill=0,
            font=font14,
        )

        # Draw labels for temperature and rain probability
        display.draw_black.text(
            (current_left + 100, min_up + 40), "min", fill=0, font=font14
        )
        display.draw_black.text(
            (current_left + 100, min_up + 60), "max", fill=0, font=font14
        )
        display.draw_black.text(
            (current_left + 100, min_up + 80), "pluie", fill=0, font=font14
        )

    ###################################################################################################################
    # GRAPHS
    # PRESSURE & TEMPERATURE
    if args.show_graph:
        graph.init_graph(weather, display)

    ###################################################################################################################
    # ALERT AND POLLUTION

    ###################################################################################################################
    # NEWS UPDATE
    news_selected = news.selected_title()
    display.draw_black.text((360, 10), "NEWS", fill=0, font=font24)
    for i in range(5):
        if len(news_selected) == 1:
            display.draw_black.text((360, 45), news_selected[0], fill=0, font=font14)
            break
        else:
            if len(news_selected[i]) <= 3:
                for j in range(len(news_selected[i])):
                    display.draw_black.text(
                        (360, 45 + j * 15 + i * 60),
                        news_selected[i][j],
                        fill=0,
                        font=font14,
                    )
            else:
                for j in range(2):
                    display.draw_black.text(
                        (360, 45 + j * 15 + i * 60),
                        news_selected[i][j],
                        fill=0,
                        font=font14,
                    )
                display.draw_black.text(
                    (360, 45 + 2 * 15 + i * 60),
                    f"{news_selected[i][2]}[...]",
                    fill=0,
                    font=font14,
                )

    ###################################################################################################################
    print(Fore.GREEN + "Updating screen...")
    # display.im_black.show()
    # display.im_red.show()
    print(Fore.GREEN + "\tPrinting...")

    time.sleep(2)
    epd.display(epd.getbuffer(display.im_black), epd.getbuffer(display.im_red))
    time.sleep(2)
    return True


if __name__ == "__main__":
    global been_reboot
    been_reboot = 1
    while True:
        try:
            weather = Weather(lat, lon, api_key_weather)
            # pollution = Pollution()
            news = News()
            break
        except Exception as e:
            current_time = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
            print(Fore.RED + "INITIALIZATION PROBLEM- @" + current_time)
            print(e)
            logger.warning(Fore.RED + "INITIALIZATION PROBLEM- @" + current_time)
            logger.warning(e)
            time.sleep(2)

    epd = epd7in5b_V2.EPD()
    while True:
        try:
            # Defining objects
            current_time = time.strftime("%d/%m/%Y %H:%M", time.localtime())
            print(Fore.YELLOW + "Begin update at" + current_time)
            print(Fore.YELLOW + "Creating display")
            display = Display()
            # Update values
            weather.update()
            print(Fore.GREEN + "Weather Updated")
            # pollution.update(lat, lon, api_key_weather)
            news.update(api_key_news)
            print(Fore.GREEN + "News Updated")

            print(Fore.GREEN + Style.BRIGHT + "Main program running...")
            epd.init()
            epd.Clear()
            check_for_shutdown()
            main()
            print(Fore.YELLOW + Style.BRIGHT + "Going to sleep...")
            epd.init()
            epd.sleep()
            print(Fore.CYAN + "Sleeping ZZZzzzzZZZzzz")
            print(Fore.CYAN + "Done")
            print("------------")
            time.sleep(1800)
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            print(Fore.RED + f"Error: {e}")
            time.sleep(5)  # Avoid CPU overload if it keeps failing
