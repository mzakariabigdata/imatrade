"""Module pour le contrôleur des indicators de trading"""

import glob
from pathlib import Path
import pandas as pd
from src.imatrade.view.trading_indicator_view import TradingIndicatorView


class TradingIndicatorsController:
    """Contrôleur des indicators de trading"""

    def __init__(self, indicator_factory):
        self.indicator_factory = indicator_factory  # Factory d'indicators
        self.indicators = {}  # Stocker les indicators créés
        self.data = None  # Stocker les données du marché

    def load_data(self, num_files=1):
        """Charger les données du marché"""
        script_path = Path(__file__).resolve()
        # Ajouter '../data/' à script_path
        new_path = script_path.parent / "../../data/"

        # Résoudre le chemin pour éliminer le '..'
        new_path = new_path.resolve()
        files = glob.glob(str(new_path) + "/" + str(num_files) + "*.xlsx")
        print("new_path", new_path)
        print("files", files)
        if not files:
            print("No files found that match the prefix.")
            return None
        dataframe = pd.read_excel(files[0])
        return dataframe

    def load_indicators_builder(self):
        """Charger les constructeurs d'indicators"""
        self.indicator_factory.load_builder()

    def create_all_indicators(self):
        """Créer tous les indicators à partir du fichier indicators.yaml"""
        self.load_indicators_builder()  # Charger les constructeurs d'indicators
        for indicator_name in self.indicator_factory.get_registered_indicator_names():
            indicator = self.indicator_factory.create_indicator(indicator_name)
            self.add_indicator(indicator_name, indicator)
        return self.indicators

    def create_indicator(self, indicator_type):
        """Créer un indicator de trading"""
        indicator_name, indicator = self.indicator_factory.create_indicator(
            indicator_type
        )
        self.add_indicator(
            indicator_name, indicator
        )  # Ajouter l'indicator au dictionnaire
        return indicator

    def add_indicator(self, indicator_name, indicator):
        """Ajouter un indicator au dictionnaire"""
        self.indicators[indicator_name] = indicator

    def remove_indicator(self, indicator_name):
        """Supprimer un indicator"""
        if indicator_name in self.indicators:
            del self.indicators[indicator_name]

    def display_indicators_summary(self):
        """Afficher un résumé de tous les indicators"""
        print()
        print(
            f"Récapitulatif des indicators de trading, total {len(self.indicators)} :"
        )
        print()
        for _, indicator in self.indicators.items():
            TradingIndicatorView.display_indicator_summary(indicator)

    def display_all_indicators(self):
        """Afficher toutes les stratégies"""
        for indicator_name, indicator in self.indicators.items():
            print(f"\nStrategy name: {indicator_name}")
            TradingIndicatorView.display_indicator(indicator)

    def display_indicator(self, indicator_name):
        """Afficher un indicator"""
        if indicator_name in self.indicators:
            TradingIndicatorView.display_indicator(self.indicators[indicator_name])

    def perform_indicator(self, indicator_name):
        """Exécuter un indicator"""
        self.data = self.load_data()
        print("data", self.data)
        if indicator_name in self.indicators:
            # self.indicators[indicator_name].perform()
            print("perform_indicator", self.indicators[indicator_name])

    def get_indicator(self, indicator_name):
        """Récupérer un indicator"""
        if indicator_name in self.indicators:
            return self.indicators[indicator_name]
        return None

    def get_indicators(self):
        """Récupérer tous les indicators"""
        return self.indicators

    def get_indicator_names(self):
        """Récupérer les noms de tous les indicators"""
        return self.indicators.keys()

    def get_indicator_by_name(self, indicator_name):
        """Récupérer un indicator par son nom"""
        if indicator_name in self.indicators:
            return self.indicators[indicator_name]
        return None

    def get_indicator_by_type(self, indicator_type):
        """Récupérer un indicator par son type"""
        for indicator in self.indicators.values():
            if indicator.type == indicator_type:
                return indicator
        return None