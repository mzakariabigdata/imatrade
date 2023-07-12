"""Module pour le contrôleur des stratégies de trading""" ""

from src.imatrade.view.trading_strategy_view import TradingStrategyView


class TradingStrategyController:
    """Contrôleur des stratégies de trading"""

    def __init__(self, strategy_factory):
        self.strategy_factory = strategy_factory
        self.strategies = {}  # Stocker les stratégies créées

    def load_strategies_builder(self):
        """Charger les constructeurs de stratégies"""
        self.strategy_factory.load_builder()

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

    def get_strategy(self, strategy_name):
        """Récupérer une stratégie"""
        return self.strategies.get(strategy_name)

    def display_all_strategies(self):
        """Afficher toutes les stratégies"""
        for strategy_name, strategy in self.strategies.items():
            print(f"\nStrategy name: {strategy_name}")
            TradingStrategyView.display_strategy(strategy)

    def display_strategy(self, strategy_name):
        """Afficher une stratégie"""
        strategy = self.get_strategy(strategy_name)
        TradingStrategyView.display_strategy(strategy)

    def display_data(self, data):
        """Afficher les données du marché"""
        TradingStrategyView.display_data(data)

    def display_signals(self, signals):
        """Afficher les signaux de trading"""
        TradingStrategyView.display_signals(signals)

    def execute_strategy(self, strategy_name, market_data):
        """Exécuter une stratégie de trading"""
        strategy = self.get_strategy(strategy_name)
        strategy.prepare_data(market_data)
        signals = strategy.generate_signals()
        self.display_signals(signals)
        return signals

    def __enter__(self):
        """Méthode pour le context manager"""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Méthode pour le context manager"""
