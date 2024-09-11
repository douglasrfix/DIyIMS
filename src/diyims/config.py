import configparser


def list_config():
    config = configparser.ConfigParser()

    try:
        with open("example.ini", "r") as configfile:
            config.read_file(configfile)

    except FileNotFoundError as e:
        print(f"The error '{e}' occurred.")
        return

    with open("example.ini", "w") as configfile:
        config.write(configfile)
