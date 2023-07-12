"""
Contient les classes de vue pour afficher les stratégies et les données
"""



class TradingStrategyView:
    """Classe de vue pour afficher les stratégies de trading"""

    @staticmethod
    def display_strategy(strategy):
        """Affiche une stratégie de trading"""
        print(f"Stratégie de trading : {strategy.display_name}")
        print(f"déscription: {strategy.description}")
        print("Paramètres :")
        for key, value in strategy.parameters.items():
            print(f"  {key}: {value}")
        print()

    @staticmethod
    def display_data(data):
        """Affiche les données du marché"""
        print("Données du marché :")
        for row in data:
            print(f"  {row}")
        print()

    @staticmethod
    def display_strategies_summary(strategy):
        """Affiche un résumé de la stratégie de trading"""
        print(f"Nom : {strategy.name}")
        print(f"Paramètres : {strategy.parameters}")
        print()

    @staticmethod
    def display_signals(signals):
        """Affiche les signaux de trading"""
        print("Signaux de trading :")
        for signal in signals:
            print(f"  {signal}")
        print()
