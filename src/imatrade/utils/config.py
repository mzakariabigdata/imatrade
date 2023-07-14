"""Module de configuration de l'application"""

# utils/config.py
import os
import yaml
from imobject import ObjDict


APPLICATION = ObjDict()


class Config:  # pylint: disable=too-few-public-methods
    """Classe de configuration"""

    def __init__(self, config_file):
        self._config_file = config_file

    def load_config(self):
        """Chargement de la configuration"""
        with open(self._config_file, "r", encoding="UTF-8") as file:
            return yaml.safe_load(file)

    def save_config(self, config):
        """Sauvegarde de la configuration"""
        with open(self._config_file, "w", encoding="UTF-8") as file:
            yaml.dump(config, file)


# Chargement de la configuration des stratégies
APPLICATION.strategies_config = Config(
    os.path.join(os.path.dirname(__file__), "../..", "config", "strategies.yml")
).load_config()

# chargement de la configuration des indicateurs
APPLICATION.indicators_config = Config(
    os.path.join(os.path.dirname(__file__), "../..", "config", "indicators.yml")
).load_config()

APPLICATION.backtests_config = Config(
    os.path.join(os.path.dirname(__file__), "../..", "config", "backtests.yml")
).load_config()
