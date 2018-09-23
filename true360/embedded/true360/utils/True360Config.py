import configparser


class True360Configs:

    def __init__(self):
        self._config = configparser.ConfigParser()
        self._environments = './true360/config/env.ini'
        self._config.read(self._environments)

    def getint(self, section, option):
        try:
            value = self._config.getint(section, option)
            if value == "None":
                return None
            return value
        except ValueError:
            return None

    def getstr(self, section, option):
        value = self._config.get(section, option)
        if len(value) == 0 or value == "None":
            return None
        return str(value)

    def set(self, section, option, value):
        self._config.set(section, option, value)

    def save(self):
        with open(self._environments, "w") as configfile:
            self._config.write(configfile)
