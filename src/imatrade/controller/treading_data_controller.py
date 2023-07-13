"""Module pour le data controller"""
import os
import glob
from pathlib import Path
import pandas as pd
from src.imatrade import Singleton


class TreadingDataController(metaclass=Singleton):
    """Contrôleur des données"""

    def __init__(self, oanda_data_provider):
        self.data = pd.DataFrame()  # Stocker les données du marché
        self.file_name = None  # Stocker le nom du fichier
        self.oanda_data_provider = oanda_data_provider

    def get_data(self):
        """Récupérer les données du marché"""
        if self.data.empty:
            print("No data to return.")
            return None
        return self.data

    def set_data(self, data):
        """ReDéfinir les données du marché"""
        self.data = data

    def get_file_name(self, file_path):
        """Récupérer le nom du fichier"""
        return os.path.basename(file_path[0])

    def load_data(self, num_files=1):
        """Charger les données du marché"""

        script_path = Path(__file__).resolve()  # Chemin du script
        new_path = script_path.parent / "../../data/"  # Ajouter '../../data/'

        # Résoudre le chemin pour éliminer le '..'
        new_path = new_path.resolve()
        files = glob.glob(str(new_path) + "/" + str(num_files) + "*.xlsx")
        print("new_path", new_path)
        print("files", files)
        if not files:
            print("No files found that match the prefix.")
            return None
        dataframe = pd.read_excel(files[0])
        self.data = dataframe
        self.file_name = self.get_file_name(files)
        return dataframe

    def print_data(self):
        """Afficher les données du marché"""
        print(self.data)

    def save_data(self):
        """Sauvegarder les données du marché"""
        script_path = Path(__file__).resolve()  # Chemin du script
        save_directory = (
            script_path.parent / "../../data/saves"
        )  # Ajouter '../../data/'

        # Résoudre le chemin pour éliminer le '..'
        save_directory = save_directory.resolve()

        # Créer le répertoire s'il n'existe pas
        if not os.path.exists(save_directory):
            save_directory.mkdir(parents=True, exist_ok=True)

        save_file = save_directory / self.file_name
        suffix = 0

        # Vérifiez si le fichier existe déjà. Dans ce cas, ajoutez un suffixe.
        while save_file.exists():
            suffix += 1
            save_file = save_directory / f"{self.file_name}_{suffix}.xlsx"

        if self.data.empty:
            print("No data to save.")
            return None

        # Définir le format de date
        self.data["time"] = pd.to_datetime(self.data["time"]).dt.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.data.to_excel(save_file, index=False)
        print(f"Data saved to data/saves/{self.file_name}_{suffix}.xlsx")
        return save_file

    def get_historical_data(self):
        """Récupérer les données historiques du marché"""
        market_data = self.oanda_data_provider.get_historical_data(
            instrument="EUR_USD", start="2021-01-01", end="2021-12-31", granularity="D"
        )
        return market_data
