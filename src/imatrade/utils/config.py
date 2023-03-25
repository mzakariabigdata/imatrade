# utils/config.py
import os
import yaml


class Config:
    def __init__(self, config_file):
        self._config = self._load_config(config_file)

    def _load_config(self, config_file):
        with open(config_file, "r") as f:
            return yaml.safe_load(f)

    def get(self, key, default=None):
        return self._config.get(key, default)


# Chargement de la configuration des stratégies
strategies_config = Config(
    os.path.join(os.path.dirname(__file__), "..\\..", "config", "strategies.yaml")
)
