from battery import get_battery
from gui import BatteryApp


def main():

    battery = get_battery()

    if battery is None:
        return

    app = BatteryApp(battery)

    app.run()


if __name__ == "__main__":
    main()
