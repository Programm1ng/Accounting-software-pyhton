from Accounting import Accounting

# Make an object
accounting = Accounting()

# Load all clients from text files
clients = accounting.init()


# Prints out the menu
def displayMenu():
    print("Please select an action by typing in the number and press enter")
    print("1 Show all clients")
    print("2 Create a new client")
    print("3 Show transactions of a client")
    print("4 New transaction")
    print("5 Show cashflow graph for user")
    userInput = input()

    if userInput == "1":
        # Print all clients
        accounting.displayClients()
    elif userInput == "2":
        print("Please enter the firstname")
        firstname = input()

        print("Please enter the lastname")
        lastname = input()

        print("Please enter the initial balance")
        balance = input()
        if not balance.isnumeric():
            print("Not a number!")
            return

        accounting.newClient(firstname, lastname, balance)
    elif userInput == "3":
        print("Please enter a client id")
        clientId = input()
        if clientId.isnumeric():
            accounting.displayTransactions(clientId)
    elif userInput == "4":
        print("Pleae enter the id of the client who shall pay")
        fromClientId = input()
        if not fromClientId.isnumeric():
            print("Not a number!")
            return

        print("Pleae enter the id of the client who shall receive")
        toClientId = input()
        if not toClientId.isnumeric():
            print("Not a number!")
            return

        print("Please enter the amount of money")
        amount = input()
        if not amount.isnumeric():
            print("Not a number!")
            return

        accounting.makeTransaction(fromClientId, toClientId, amount)
    elif userInput == "5":
      print("Pleae enter the id of the client who shall pay")
      fromClientId = input()
      if not fromClientId.isnumeric():
        print("Not a number!")
        return
      accounting.displayCashflowGraph(fromClientId)


while True:
    displayMenu()