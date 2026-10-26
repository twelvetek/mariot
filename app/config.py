from configparser import ConfigParser
from pathlib import Path


class Config:

    def __init__(self):

        config_file = Path(__file__).parent.parent / "config.ini"

        parser = ConfigParser()
        parser.read(config_file)

        self.web_host = parser["WEB"]["HOST"]
        self.web_port = parser.getint("WEB", "PORT")
        self.debug = parser.getboolean("WEB", "DEBUG")

        self.db_file = parser["DATABASE"]["FILE"]

        self.log_level = parser["LOGGING"]["LEVEL"]
        self.log_file = config_file.parent / parser["LOGGING"]["FILE"]