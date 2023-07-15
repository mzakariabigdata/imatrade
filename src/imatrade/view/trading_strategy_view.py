"""
Contient les classes de vue pour afficher les stratégies et les données
"""


class TradingStrategyView:
    """Classe de vue pour afficher les stratégies de trading"""

    @staticmethod
    def display_a_strategy(strategy):
        """Affiche une stratégie de trading"""
        print(f"Stratégie de trading : {strategy.name}")
        print(f"déscription: {strategy.description}")
        for indicator in strategy.indicators:
            print(f"  indicator: {indicator.name}")
            print(f"     Object: {indicator}")
            print("     Paramètres :")
            for key, value in indicator.parameters.items():
                print(f"        {key}: {value}")

    @staticmethod
    def display_strategy(strategy):
        """Affiche une stratégie de trading"""
        TradingStrategyView.display_a_strategy(strategy)
        TradingStrategyView.display_rules(strategy)

    @staticmethod
    def display_all_strategies(strategies, num_spaces=0):
        """Affiche toutes les stratégies de trading"""
        spaces = " " * num_spaces
        print(f"{spaces}Stratégies de trading :")
        for strategy_name, strategy in strategies.items():
            print(f"{spaces}Strategy name: {strategy_name}")
            TradingStrategyView.display_strategy(strategy)
            print()

    # @staticmethod
    # def display_data(data):
    #     """Affiche les données du marché"""
    #     print("Données du marché :")
    #     for row in data:
    #         print(f"  {row}")
    #     print()

    @staticmethod
    def display_strategies_summary(strategy):
        """Affiche un résumé de la stratégie de trading"""
        print(f"Nom : {strategy.name}")
        print(f"Description : {strategy.description}")
        for indicator in strategy.indicators:
            print(f"  indicator: {indicator.name}")
            print(f"    Paramètres : {indicator.parameters}")
        TradingStrategyView.display_rules(strategy)

    @staticmethod
    def display_rules(strategy):
        """Affiche les règles de trading"""
        print(" Règles de trading :")
        print(f"  Entry: {strategy.entry_rule.action}")
        for condition in strategy.entry_rule.conditions:
            print(f"    name: {condition.name}")
            print(f"    condition: {condition.condition}")
        print(f"  Exit: {strategy.exit_rule.action}")
        for condition in strategy.exit_rule.conditions:
            print(f"    name: {condition.name}")
            print(f"    condition: {condition.condition}")
        print()

    # @staticmethod
    # def display_signals(signals):
    #     """Affiche les signaux de trading"""
    #     print("Signaux de trading :")
    #     for signal in signals:
    #         print(f"  {signal}")
    #     print()
