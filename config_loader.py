from typing import Union
import random


class ConfigError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return f"{self.message}"


class MazeGenerator():
    def get_conf(self, config_file: str) -> Union[dict, str]:
        dct = {}
        try:
            with open(config_file, "r") as f:
                for i in f.readlines():
                    if i[0] != "#":
                        line = i.strip().split("=")
                        dct[line[0]] = line[1]
            return dct

        except FileNotFoundError:
            raise ConfigError(f"File {config_file} doesn't exist!")
        except Exception as e:
            return f"Error: {e}"

    def validate_conf(self, conf_dict: dict) -> dict:
        if not isinstance(conf_dict, dict):
            raise ConfigError("Config is not a dict")

        conf = {}
        rules = {
            "WIDTH": int,
            "HEIGHT": int,
            "PERFECT": bool,
            "ENTRY": str,
            "EXIT": str,
            "OUTPUT_FILE": str
        }

        optional_keys = {
            "SEED": int
        }

        for key in rules.keys():
            if key not in conf_dict:
                raise ConfigError(f"Missing key: {key}")

        for key, expected_type in rules.items():
            try:
                expected_type(conf_dict[key])
                if key == "ENTRY" or key == "EXIT":
                    if "," not in conf_dict[key]:
                        raise ConfigError("f{key} must have ',' beetween numbers")
                    expected_type(conf_dict[key])
                    conf[key] = [int(conf_dict[key].split(",")[0]), int(conf_dict[key].split(",")[1])]
                elif key == "WIDTH" or key == "HEIGHT":
                    conf[key] = expected_type(conf_dict[key])
                    if conf[key] < 3:
                        raise ConfigError(f"Parameter: {key} cannot be less than 3")
                elif key == "PERFECT":
                    conf["PERFECT"] = conf_dict["PERFECT"].lower() == "true"
                else:
                    conf[key] = expected_type(conf_dict[key])
            except ValueError:
                raise ConfigError(f"Key: {key} must be of type: {expected_type.__name__}")

        if "SEED" in conf_dict:
            try:
                conf["SEED"] = int(conf_dict["SEED"])
            except ValueError:
                raise ConfigError("Seed must be an integer")
        else:
            conf["SEED"] = random.randint(0, 10000000)

        return conf
