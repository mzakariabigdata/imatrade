class Menu:
    def __init__(self, commands):
        self.commands = commands

    def display(self):
        print("\nOptions :")
        for key, command in self.commands.items():
            print(f"{key}. {command.description}")
    
    def run(self):
        while True:
            self.display()
            choice = int(input("Choisissez une option : "))

            command = self.commands.get(choice)
            if command:
                command.execute()
            else:
                print("Option invalide. Veuillez réessayer.")
