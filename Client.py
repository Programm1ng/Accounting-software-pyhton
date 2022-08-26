from ConsoleCodes import ConsoleCodes
from TransactionType import TransactionType


class Client:

    def __init__(self, id: int, firstname: str, lastname: str, balance: float):
        self.id = int(id)
        self.firstname = str(firstname)
        self.lastname = str(lastname)
        self.balance = float(balance)
        self.transactions = []

    def __str__(self) -> str:

        # If the balance is greater or equal to zero, display the balance in green, otherwise in red
        balanceStr = ConsoleCodes.OKGREEN if int(
            self.balance) >= 0 else ConsoleCodes.WARNING

        # Add the balance to the string with two decimal places and the euro symbol
        balanceStr += "{:.2f}".format(self.balance) + '€'

        # Reset the color to the normal terminal color
        balanceStr = balanceStr + ConsoleCodes.ENDC

        # Return the object description
        return(
            "ID: " + str(self.id) + "\n"
            "Firstname: " + self.firstname + "\n"
            "Lastname: " + self.lastname + "\n"
            "Balance: " + balanceStr
        )

    def addTransaction(self, transaction):
        self.transactions.append(transaction)
