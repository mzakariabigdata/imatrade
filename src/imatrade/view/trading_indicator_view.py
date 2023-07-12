"""
Contient les classes de vue pour afficher les indicators et les données
"""


class TradingIndicatorView:
    """Classe de vue pour afficher les indicators de trading"""

    @staticmethod
    def display_indicator(indicator):
        """Affiche un indicator de trading"""
        print(f"Indicator de trading : {indicator.display_name}")
        print(f"déscription: {indicator.description}")
        print("Paramètres :")
        for key, value in indicator.parameters.items():
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
    def display_indicator_summary(indicator):
        """Affiche un résumé de l'indicator de trading"""
        print(f"Nom : {indicator.name}")
        print(f"Paramètres : {indicator.parameters}")
        print()

    @staticmethod
    def display_signals(signals):
        """Affiche les signaux de trading"""
        print("Signaux de trading :")
        for signal in signals:
            print(f"  {signal}")
        print()
