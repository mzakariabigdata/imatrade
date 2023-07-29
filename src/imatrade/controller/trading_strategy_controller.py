"""Module pour le contrôleur des stratégies de trading""" ""

from src.imatrade.view.trading_strategy_view import TradingStrategyView
from src.imatrade import Singleton
from src.imatrade.processor.market_data_processor import MarketDataProcessor


class TradingStrategyController(metaclass=Singleton):
    """Contrôleur des stratégies de trading"""

    def __init__(self, strategy_factory, data_controller, report_generator):
        self.report_generator = report_generator
        self.strategy_factory = strategy_factory
        self.strategies = {}  # Stocker les stratégies créées
        self.data_controller = data_controller  # Contrôleur des données
        self.data = None  # Stocker les données du marché

    def load_strategies_builder(self):
        """Charger les constructeurs de stratégies"""
        self.strategy_factory.load_builder()

    def get_strategies(self):
        """Récupérer les stratégies"""
        return self.strategies

    def prepare_strategy_data(self, strategy_name, num_files=1):
        """Préparer les données pour les stratégies"""
        _, _ = self.data_controller.load_data(num_files)
        data = self.data_controller.get_data()
        if data is None:
            print("No data to prepare for strategies !")
            return None
        if strategy_name in self.strategies:
            strategy = self.get_strategy(strategy_name)
            print("strategy", strategy)
            print("indicator", strategy.indicators)
            for indicator in strategy.indicators:
                data = indicator.prepare_data(data)
            print(data)
        self.data_controller.set_data(data)
        return data

    def prepare_strategy_data_for_bar(self, window_data):
        """Préparer les données pour bar"""
        data = window_data
        if data is None:
            print("No data to prepare for strategies !")
            return None
        for _, strategy in self.strategies.items():
            # print("strategy", strategy)
            # print("indicator", strategy.indicators)
            for indicator in strategy.indicators:
                indicator_for_bar = indicator.prepare_data_for_bar(data)
                return indicator_for_bar
            # print("data", data)
        return data

    def create_all_strategies(self):
        """Créer toutes les stratégies à partir du fichier strategies.yaml"""
        self.load_strategies_builder()  # Charger les constructeurs de stratégies
        for strategy_name in self.strategy_factory.get_registered_strategy_names():
            strategy = self.strategy_factory.create_strategy(strategy_name)
            self.add_strategy(strategy_name, strategy)
        return self.strategies

    def create_strategy(self, strategy_type):
        """Créer une stratégie de trading"""
        strategy_name, strategy = self.strategy_factory.create_strategy(strategy_type)
        self.add_strategy(
            strategy_name, strategy
        )  # Ajouter la stratégie au dictionnaire
        return strategy

    def add_strategy(self, strategy_name, strategy):
        """Ajouter une stratégie au dictionnaire"""
        self.strategies[strategy_name] = strategy

    def remove_strategy(self, strategy_name):
        """Supprimer une stratégie"""
        if strategy_name in self.strategies:
            del self.strategies[strategy_name]

    def display_strategies_summary(self):
        """Afficher un résumé de toutes les stratégies"""
        print()
        print(
            f"Récapitulatif des stratégies de trading, total {len(self.strategies)} :"
        )
        print()
        for _, strategy in self.strategies.items():
            TradingStrategyView.display_strategies_summary(strategy)

    def process_market_data(self, strategy_name, num_files=1):
        """Préparer les données du marché"""
        _, file_name = self.data_controller.load_data(num_files)
        strategy = self.get_strategy(strategy_name)
        market_data_processor = MarketDataProcessor(
            self.data_controller.get_data(), strategy
        )
        market_data_processor.file_name = file_name
        market_data_processor.process_market_data()

        data_frame_processed = market_data_processor.get_data_frame_processed()
        self.data_controller.set_data(data_frame_processed)
        self.data_controller.save_data()

        self.report_generator.generate_close_report(market_data_processor)

    def run_strategy(self, strategy_name):
        """Exécuter une stratégie de trading"""
        self.process_market_data(strategy_name)

    def get_strategy(self, strategy_name):
        """Récupérer une stratégie"""
        return self.strategies.get(strategy_name)

    def display_all_strategies(self):
        """Afficher toutes les stratégies"""
        TradingStrategyView.display_all_strategies(self.strategies)

    def display_strategy(self, strategy_name):
        """Afficher une stratégie"""
        strategy = self.get_strategy(strategy_name)
        TradingStrategyView.display_strategy(strategy)

    # def display_data(self, data):
    #     """Afficher les données du marché"""
    #     TradingStrategyView.display_data(data)

    # def display_signals(self, signals):
    #     """Afficher les signaux de trading"""
    #     TradingStrategyView.display_signals(signals)

    def execute_strategy(self, strategy_name, market_data):
        """Exécuter une stratégie de trading"""
        strategy = self.get_strategy(strategy_name)
        strategy.prepare_data(market_data)
        signals = strategy.generate_signals()
        # self.display_signals(signals)
        return signals

    def __enter__(self):
        """Méthode pour le context manager"""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Méthode pour le context manager"""
