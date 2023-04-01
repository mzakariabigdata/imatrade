# utils/config.py
import os
import yaml
from imobject import ObjDict

global APPLICATION

APPLICATION = ObjDict()


class Config:
    def __init__(self, config_file):
        self._config_file = config_file

    def _load_config(self):
        with open(self._config_file, "r") as f:
            return yaml.safe_load(f)


# Chargement de la configuration des stratégies
APPLICATION.strategies_config = Config(
    os.path.join(os.path.dirname(__file__), "..\\..", "config", "strategies.yaml")
)._load_config()

# strategies_config =

# print("0000", strategies_config)
