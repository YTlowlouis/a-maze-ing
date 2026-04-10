from typing import Union
import random


class ConfigError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return f"{self.message}"


class MazeGenerator():
    def get_conf(self, config_file: str) -> dict[str, str]:
        dct = {}
        try:
            with open(config_file, "r") as f:
                for i in f:
                    line = i.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        raise ConfigError(f"Invalid line: {line}")
                    key, value = map(str.strip, line.split("=", 1))
                    if key in dct:
                        raise ConfigError(f"Duplicate key: {key}")
                    dct[key] = value
        except FileNotFoundError:
            raise ConfigError(f"File {config_file} doesn't exist!")
        except Exception as e:
            raise ConfigError(f"Unexpected error reading config: {e}")

        return dct

    def validate_conf(self,
                      conf_dict: dict) -> dict:
        if not isinstance(conf_dict, dict):
            raise ConfigError("Config is not a dict")

        conf: dict[str, Union[int, bool, str, tuple[int, int] | None]] = {}
        rules = {
            "WIDTH": int,
            "HEIGHT": int,
            "PERFECT": bool,
            "ENTRY": str,
            "EXIT": str,
            "OUTPUT_FILE": str
        }

        for key in rules.keys():
            if key not in conf_dict:
                raise ConfigError(f"Missing key: {key}")

        for key, expected_type in rules.items():
            try:
                if key == "ENTRY" or key == "EXIT":
                    if "," not in conf_dict[key]:
                        raise ConfigError(f"{key} must have ','"
                                          " beetween numbers")
                    if len(conf_dict[key].split(',')) != 2:
                        raise ConfigError(f"{key} must have only two values"
                                          " as coordinates")
                    if (
                        int(conf_dict[key].split(',')[0]) >=
                        int(conf_dict["HEIGHT"])
                        or int(conf_dict[key].split(',')[1]) >=
                        int(conf_dict["WIDTH"])
                    ):
                        raise ConfigError(f"{key} must be"
                                          " inside the maze")
                    if int(conf_dict[key].split(',')[0]) < 0 or \
                       int(conf_dict[key].split(',')[1]) < 0:
                        raise ConfigError("Error, ENTRY and EXIT"
                                          " must be positive !")
                    conf[key] = (int(conf_dict[key].split(",")[0]),
                                 int(conf_dict[key].split(",")[1]))
                elif key == "WIDTH" or key == "HEIGHT":
                    # conf[key] = expected_type(conf_dict[key])
                    value = expected_type(conf_dict[key])
                    if value < 3:
                        raise ConfigError(f"Parameter: {key} too short")
                    if value > 80:
                        raise ConfigError(f"Parameter: {key} too big")
                    conf[key] = value
                elif key == "PERFECT":
                    if conf_dict["PERFECT"].lower() not in ["true", "false"]:
                        raise ConfigError("PERFECT must be True or False")
                    else:
                        temp = conf_dict["PERFECT"].lower()
                        conf[key] = True if temp == "true" else False
                elif key == "OUTPUT_FILE":
                    if not conf_dict["OUTPUT_FILE"].endswith(".txt"):
                        raise ConfigError("Output file must be format '.txt'")
                    else:
                        conf[key] = str(conf_dict["OUTPUT_FILE"])
                else:
                    conf[key] = expected_type(conf_dict[key])

            except ValueError:
                raise ConfigError(f"Key: {key} must be of type: int")
        if conf["ENTRY"] == conf["EXIT"]:
            raise ConfigError("Entry point and Exit point"
                              " cannot be the same")
        if "SEED" in conf_dict:
            try:
                conf["SEED"] = int(conf_dict["SEED"])
            except ValueError:
                raise ConfigError("Seed must be an integer")
        else:
            conf["SEED"] = random.randint(0, 10000000)
        return conf
