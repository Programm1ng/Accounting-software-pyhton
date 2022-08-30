import glob
from Client import Client
from Transaction import Transaction
from ConsoleCodes import ConsoleCodes
from TransactionType import TransactionType
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np
import datetime

class Accounting:

    def __init__(self):
        self.clients = []

    # Load all clients from text files located in the folder clients
    def init(self):

        # Read all text files located in the clients folder
        clientFiles = glob.glob('./clients/*.txt')

        # Iterate over all text file paths
        for clientFile in clientFiles:
            with open(clientFile) as f:

                # Open text file for reading it
                f = open(clientFile, "r")

                # Get the content of the text file and split the string by semicolon
                data = f.read().split(';')

                # Make a new object of type client and initialize it with id, firstname, lastname and balance we just read from the text file
                if (len(data) >= 4):
                    client = Client(data[0], data[1], data[2], data[3])

                    #  Get transactions if there are ones
                    for i in range(4, len(data)):
                        transactionArr = data[i].split('/')
                        newTransaction = Transaction(
                            # Type, otherClientId, amount, newBalance, day, month, year
                            transactionArr[0], transactionArr[1], transactionArr[2], transactionArr[3], transactionArr[4], transactionArr[5], transactionArr[6])
                        client.addTransaction(newTransaction)

                    self.clients.append(client)

    # This method will save the data of the clients objects into there proper text file
    def updateClient(self, client):
        with open("./clients/" + str(client.id) + ".txt", 'wt') as f:
            clientString = self.getClientString(client)
            transactionString = self.getTransactionsString(client)

            if (transactionString != None):
                clientString += transactionString

            f.write(clientString)
            f.close()

    # This method creates the correct string for saving client data into the text file
    def getClientString(self, client):
        return str(client.id) + ";" + client.firstname + ";" + client.lastname + ";" + str(client.balance)

    def getTransactionsString(self, client):
        transactionStr = ""
        for transaction in client.transactions:
            transactionStr += ";" + str(transaction.type) + "/" + \
                str(transaction.otherClientId) + "/" + str(transaction.amount) + "/" + str(transaction.newBalance) + "/" + str(transaction.day) + "/" + str(transaction.month) + "/" + str(transaction.year)

        if len(client.transactions) > 0:
            return transactionStr
        else:
            return None

    # Make a transaction from one client to another client
    def makeTransaction(self, fromClientId, toClientId, amount):

        if (fromClientId == toClientId):
            print("Client cannot pay himself")
            return

        fromClient = self.getClientById(fromClientId)

        toClient = self.getClientById(toClientId)

        if (fromClient == None):
            print("Client who shall pay does not exist")
            return

        if (toClient == None):
            print("Client who shall receive does not exist")
            return

        if (float(fromClient.balance) - float(amount) < 0):
            print("Client who shall pay has not enough money")
            return

        # Current date time
        now = datetime.datetime.now()

        # New Balance for fromClient
        fromClient.balance = int(fromClient.balance) - int(amount)

        # Create new transaction for fromClient
        fromClientTransaction = Transaction(
            TransactionType.PAID.value, toClientId, amount, fromClient.balance, now.day, now.month, now.year)

        # Add the transaction to the fromClient object
        fromClient.addTransaction(fromClientTransaction)

        # New Balance for toClient
        toClient.balance = int(toClient.balance) + int(amount)

        # Create new transaction for toClient
        toClientTransaction = Transaction(
            TransactionType.RECEIVED.value, fromClientId, amount, toClient.balance, now.day, now.month, now.year)

        # Add the transaction to the toClient object
        toClient.addTransaction(toClientTransaction)

        # Update fromClient file
        self.updateClient(fromClient)

        # Update toClient file
        self.updateClient(toClient)

    def displayClients(self):
      headers = ["ID", "Firstname", "Lastname", "Balance"]
      data = []
      for client in self.clients:
        data.append(client.id, client.firstname, client.lastname, client.balance);

      print(tabulate(data, headers, tablefmt="grid"))

    def displayTransactions(self, clientId):

      client = self.getClientById(clientId)

      if (client == None):
            print("Client not found")
            return

      headers = ["Date", "Type", "Amount", "from/to", "Other Client", "New Balance"]

      data = []

      print("Client: ", client.firstname, client.lastname)

      for transaction in client.transactions:
        
        transactionType, relation = ("Paid", "to") if int(transaction.type) == int(TransactionType.PAID.value) else ("Received", "from");
        
        otherClient = self.getClientById(transaction.otherClientId);
        
        otherClientName = otherClient.firstname + " " + otherClient.lastname if otherClient != None else "Unknown"

        transactionAmountStr = "{:.2f}".format(float(transaction.amount)) + '€'

        newBalanceStr = "{:.2f}".format(float(transaction.newBalance)) + '€'
        
        data.append([transaction.date(), transactionType, transactionAmountStr, relation, otherClientName, newBalanceStr]);

      print(tabulate(data, headers, tablefmt="grid"))

    def getClientById(self, clientId):
        for client in self.clients:
            if int(client.id) == int(clientId):
                return client

        return None

    def newClient(self, firstname, lastname, balance):
        clientId = self.getNewClientId()
        client = Client(clientId, firstname, lastname, balance)
        self.clients.append(client)
        self.updateClient(client)

    def getNewClientId(self):
        clientId = 0
        for client in self.clients:
            if client.id >= clientId:
                clientId = client.id + 1
        return clientId

    def displayCashflowGraph(self, clientId):
      client = self.getClientById(clientId)

      if (client == None):
            print("Client not found")
            return
      
      dates = list(map(lambda transaction : transaction.date(), client.transactions))

      balances = list(map(lambda transaction : float(transaction.newBalance), client.transactions))

      fig, ax = plt.subplots()
      ax.plot(dates, balances)

      ax.set(xlabel='Date', ylabel='Balance (€)',
             title="Client: " + client.firstname + " " + client.lastname)
      ax.grid()

      plt.show()