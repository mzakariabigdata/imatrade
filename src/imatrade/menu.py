"""Module to display and run a menu."""


class Menu:
    """Class to display and run a menu."""

    def __init__(self, commands):
        self.commands = commands

    def last_digit(self, number):
        """method to get the last digit of a number."""
        return int(str(number)[-1])

    def display(self):
        """method to display the menu."""
        print("\nOptions :")
        for key, command in self.commands.items():
            if isinstance(key, str):
                print(f"{command}")
                continue
            print(f"{self.last_digit(key)}. {command.description}")

    def run(self):
        """method to run the menu."""

        while True:
            self.display()
            choice = int(input("Choisissez une option : "))

            command = self.commands.get(choice)
            if command:
                command.execute()
            else:
                print("Option invalide. Veuillez réessayer.")
