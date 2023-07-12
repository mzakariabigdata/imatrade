"""Module pour le data controller"""
import os
import glob
from pathlib import Path
import pandas as pd


class TreadingDataController:
    """Contrôleur des données"""

    def __init__(self, data_factory):
        self.data_factory = data_factory  # Factory de données
        self.data = pd.DataFrame()  # Stocker les données du marché

    def load_data(self, num_files=1):
        """Charger les données du marché"""

        script_path = Path(__file__).resolve() # Chemin du script
        new_path = script_path.parent / "../../data/" # Ajouter '../../data/' 

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
        return dataframe

    def print_data(self):
        """Afficher les données du marché"""
        print(self.data)

    def save_data(self):
        """Sauvegarder les données du marché"""
        script_path = Path(__file__).resolve() # Chemin du script
        save_directory = script_path.parent / "../../data/saves" # Ajouter '../../data/' 

        # Résoudre le chemin pour éliminer le '..'
        save_directory = save_directory.resolve()

        # Créer le répertoire s'il n'existe pas
        if not os.path.exists(save_directory):
            save_directory.mkdir(parents=True, exist_ok=True)

        save_file = save_directory / "data.xlsx"
        suffix = 0

        # Vérifiez si le fichier existe déjà. Dans ce cas, ajoutez un suffixe.
        while save_file.exists():
            suffix += 1
            save_file = save_directory / f"data_{suffix}.xlsx"

        if self.data.empty:
            print("No data to save.")
            return None
        
        # Définir le format de date
        self.data['time'] = pd.to_datetime(self.data['time']).dt.strftime('%Y-%m-%d %H:%M:%S')


        self.data.to_excel(save_file, index=False)
        print("Data saved to data/saves/data.xlsx")
