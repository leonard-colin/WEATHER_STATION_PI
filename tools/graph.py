import json
from display import font12


def _map_resize(val, in_mini, in_maxi, out_mini, out_maxi):
    return (
        (val - in_mini) * (out_maxi - out_mini) // (in_maxi - in_mini) + out_mini
        if in_maxi - in_mini != 0
        else out_mini
    )

def init_graph(weather, display):
    pression = []
    temperature = []
    maxi = 440  # MAX VERT. PIXEL OF THE GRAPH
    mini = 360  # MIN VERT PIXEL OF THE GRAPH
    x = [55, 105, 155, 205, 255, 305, 355]  # X value of the points
    j = ["J-6", "J-5", "J-4", "J-3", "J-2", "J-1", "J"]  # LABELS

    weather.graph_p_t()
    data = weather.prevision[1]
    global been_reboot
    if been_reboot == 1:
        try:
            with open("saved.txt", "r") as file:
                weather.prevision[1] = json.loads(file.read())
                data = weather.prevision[1]
                been_reboot = 0
        except:
            pass

    with open("saved.txt", "w") as file:
        file.write(str(data))
    for i in range(len(data)):
        pression.append(data[i][0])
        temperature.append(data[i][1])

    # PRESSURE
    display.draw_black.line(
        (40, mini, 40, maxi + 20), fill=0, width=1
    )  # GRAPH AXIS
    display.draw_black.text(
        (10, mini), str(max(pression)), fill=0, font=font12
    )  # MAX AXIS GRAPH LABEL
    display.draw_black.text(
        (10, maxi), str(min(pression)), fill=0, font=font12
    )  # MIN AXIS GRAPH LABEL
    display.draw_black.text(
        (10, mini + (maxi - mini) // 2),
        str((max(pression) + min(pression)) // 2),
        fill=0,
        font=font12,
    )  # MID VALUE LABEL
    for i in range(len(x)):  # UPDATE CIRCLE POINTS
        display.draw_black.text((x[i], 455), j[i], fill=0, font=font12)
        display.draw_circle(
            x[i],
            _map_resize(pression[i], min(pression), max(pression), maxi, mini),
            3,
            "r",
        )
    for i in range(len(x) - 1):  # UPDATE LINE
        display.draw_red.line(
            (
                x[i],
                _map_resize(pression[i], min(pression), max(pression), maxi, mini),
                x[i + 1],
                _map_resize(
                    pression[i + 1], min(pression), max(pression), maxi, mini
                ),
            ),
            fill=0,
            width=2,
        )
    # TEMPERATURE
    display.draw_black.line(
        (430, mini, 430, maxi + 20), fill=0, width=1
    )  # GRAPH AXIS
    display.draw_black.text(
        (410, mini), str(max(temperature)), fill=0, font=font12
    )  # MAX AXIS GRAPH LABEL
    display.draw_black.text(
        (410, maxi), str(min(temperature)), fill=0, font=font12
    )  # MIN AXIS GRAPH LABEL
    display.draw_black.text(
        (410, mini + (maxi - mini) // 2),
        str((max(temperature) + min(temperature)) // 2),
        fill=0,
        font=font12,
    )  # MID VALUE LABEL
    for i in range(len(x)):  # UPDATE CIRCLE POINTS
        display.draw_black.text((x[i] + 400, 455), j[i], fill=0, font=font12)
        display.draw_circle(
            x[i] + 400,
            _map_resize(
                temperature[i], min(temperature), max(temperature), maxi, mini
            ),
            3,
            "r",
        )
    for i in range(len(x) - 1):  # UPDATE LINE
        display.draw_red.line(
            (
                x[i] + 400,
                _map_resize(
                    temperature[i], min(temperature), max(temperature), maxi, mini
                ),
                x[i + 1] + 400,
                _map_resize(
                    temperature[i + 1],
                    min(temperature),
                    max(temperature),
                    maxi,
                    mini,
                ),
            ),
            fill=0,
            width=2,
        )