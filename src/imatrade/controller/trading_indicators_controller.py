"""Module pour le contrôleur des indicators de trading"""

from src.imatrade.view.trading_indicator_view import TradingIndicatorView
from src.imatrade import Singleton


class TradingIndicatorsController(metaclass=Singleton):
    """Contrôleur des indicators de trading"""

    def __init__(self, indicator_factory, data_controller):
        self.indicator_factory = indicator_factory  # Factory d'indicators
        self.indicators = {}  # Stocker les indicators créés
        self.data = None  # Stocker les données du marché
        self.data_controller = data_controller  # Contrôleur des données

    def load_indicators_builder(self):
        """Charger les constructeurs d'indicators"""
        self.indicator_factory.load_builder()  # Charger les constructeurs d'indicators

    def create_all_indicators(self):
        """Créer tous les indicators à partir du fichier indicators.yaml"""
        self.load_indicators_builder()  # Charger les constructeurs d'indicators
        for (
            indicator_name
        ) in (
            self.indicator_factory.get_registered_indicator_names()
        ):  # Créer tous les indicators
            indicator = self.indicator_factory.create_indicator(
                indicator_name
            )  # Créer un indicator
            self.add_indicator(
                indicator_name, indicator
            )  # Ajouter l'indicator au dictionnaire
        return self.indicators  # Retourner les indicators

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
        TradingIndicatorView.display_all_indicators(self.indicators)

    def display_indicator(self, indicator_name):
        """Afficher un indicator"""
        if indicator_name in self.indicators:
            TradingIndicatorView.display_indicator(self.indicators[indicator_name])

    def prepare_indicator_data(self, indicator_name, num_files=1):
        """Préparer les données pour les indicators"""
        _, _ = self.data_controller.load_data(num_files)
        data = self.data_controller.get_data()
        if data is None:
            print("No data to prepare for indicators !")
            return None
        if indicator_name in self.indicators:
            prepared_date = self.indicators.get(indicator_name).prepare_data(data)
            self.data_controller.set_data(prepared_date)
        self.data = prepared_date
        return True

    def prepare_indicator_data_for_bar(self, indicator_name, window_data):
        """Préparer les données pour bar"""
        data = window_data
        if data is None:
            print("No data to prepare for indicators !")
            return None
        if indicator_name in self.indicators:
            indicator_for_bar = self.indicators.get(
                indicator_name
            ).prepare_data_for_bar(data)
            return indicator_for_bar
        return data

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
