import subprocess
import shutil


class Battery:

    def __init__(self, info):

        self.vendor = info.get("vendor")
        self.model = info.get("model")
        self.serial = info.get("serial")

        self.state = info.get("state")
        self.percentage = info.get("percentage")

        self.energy = info.get("energy")
        self.energy_full = info.get("energy-full")
        self.energy_full_design = info.get("energy-full-design")
        self.energy_rate = info.get("energy-rate")

        self.voltage = info.get("voltage")
        self.charge_cycles = info.get("charge-cycles")

        self.health = info.get("capacity")
        self.technology = info.get("technology")

        self.time_to_full = info.get("time to full")
        self.time_to_empty = info.get("time to empty")

        if self.health is None:
            if self.energy_full and self.energy_full_design:
                self.health = (
                    self.energy_full /
                    self.energy_full_design
                ) * 100


def is_upower_installed():

    return shutil.which("upower") is not None


def install_upower():

    print("UPower is not installed.")
    print("Installing UPower...")

    try:

        subprocess.run(
            ["sudo", "apt", "update"],
            check=True
        )

        subprocess.run(
            ["sudo", "apt", "install", "-y", "upower"],
            check=True
        )

        print("UPower installed successfully.")

        return True

    except subprocess.CalledProcessError:

        print("Failed to install UPower. Please install it manually.")

        return False


def find_battery():

    result = subprocess.run(
        ["upower", "-e"],
        capture_output=True,
        text=True,
        check=True
    )

    devices = result.stdout.splitlines()

    for device in devices:

        if "/battery_" in device.lower():

            return device

    return None


def get_battery_info(battery):

    result = subprocess.run(
        ["upower", "-i", battery],
        capture_output=True,
        text=True,
        check=True
    )

    return result.stdout


def clean_value(value):

    value = value.strip()

    try:

        if value.endswith("%"):
            return float(value[:-1])

        if value.endswith(" Wh"):
            return float(value[:-3])

        if value.endswith(" W"):
            return float(value[:-2])

        if value.endswith(" V"):
            return float(value[:-2])

        if value.endswith(" hours"):
            return float(value[:-6])

        if value.isdigit():
            return int(value)

    except ValueError:

        pass

    return value


def parse_battery_info(output):

    battery_info = {}

    for line in output.splitlines():

        if ":" not in line:
            continue

        key, value = line.split(":", 1)

        key = key.strip()
        value = value.strip()

        battery_info[key] = clean_value(value)

    return battery_info


def get_battery():

    if not is_upower_installed():

        print("UPower was not detected.")

        answer = input(
            "Do you want BAT to install UPower [y/n]: "
        ).strip().lower()

        if answer != "y":

            print("UPower is required for BAT.")

            return None

        if not install_upower():

            return None

    else:

        print("UPower is installed.")

    battery_path = find_battery()

    if not battery_path:

        print("\nNo battery found on this system.")

        return None

    print("Battery found:", battery_path)

    info = get_battery_info(battery_path)

    battery_data = parse_battery_info(info)

    return Battery(battery_data)

def refresh_battery_data(battery):
    if not battery:
        return None

    try:
        info = get_battery_info(find_battery())
        battery_data = parse_battery_info(info)
        return Battery(battery_data)
    except (subprocess.CalledProcessError, TypeError):
        return None
