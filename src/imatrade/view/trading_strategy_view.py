"""
Contient les classes de vue pour afficher les stratégies et les données
"""

# view/trading_strategy_view.py


class TradingStrategyView:
    @staticmethod
    def display_strategy(strategy):
        print(f"Stratégie de trading : {strategy.name}")
        print("Paramètres :")
        for key, value in strategy.parameters.items():
            print(f"  {key}: {value}")
        print()

    @staticmethod
    def display_data(data):
        print("Données du marché :")
        for row in data:
            print(f"  {row}")
        print()

    @staticmethod
    def display_strategy_summary(strategy):
        print(f"Nom : {strategy.name}")
        print(f"Paramètres : {strategy.parameters}")
        print()

    @staticmethod
    def display_signals(signals):
        print("Signaux de trading :")
        for signal in signals:
            print(f"  {signal}")
        print()
