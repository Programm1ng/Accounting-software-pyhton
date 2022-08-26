import glob
from Client import Client
from Transaction import Transaction
from ConsoleCodes import ConsoleCodes
from TransactionType import TransactionType


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
                            transactionArr[0], transactionArr[1], transactionArr[2])
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
                str(transaction.otherClientId) + "/" + str(transaction.amount)

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

        fromClient.balance = int(fromClient.balance) - int(amount)

        fromClientTransaction = Transaction(
            TransactionType.PAID.value, toClientId, amount)

        fromClient.addTransaction(fromClientTransaction)

        toClient.balance = int(toClient.balance) + int(amount)

        toClientTransaction = Transaction(
            TransactionType.RECEIVED.value, fromClientId, amount)

        toClient.addTransaction(toClientTransaction)

        self.updateClient(fromClient)

        self.updateClient(toClient)

    def displayClients(self):
        print("---------------------------------------")
        print("Clients\n")
        for client in self.clients:
            print(client, "\n")
        print("---------------------------------------")

    def displayTransactions(self, clientId):

        client = self.getClientById(clientId)

        if (client == None):
            print("Client not found")
            return

        print("---------------------------------------")
        print("Transactions of", client.firstname, client.lastname)

        for transaction in client.transactions:

            transactionTypeStr = ""
            if int(transaction.type) == int(TransactionType.PAID.value):
                transactionTypeStr = "Paid"
                transactionTypeStr += ConsoleCodes.WARNING
            else:
                transactionTypeStr = "Received"
                transactionTypeStr += ConsoleCodes.OKGREEN

            amountStr = "{:.2f}".format(float(transaction.amount)) + '€'

            amountStr += ConsoleCodes.ENDC

            otherClient = self.getClientById(transaction.otherClientId)

            otherClientStr = "to " if int(transaction.type) == int(
                TransactionType.PAID.value) else "from "

            otherClientStr += (otherClient.firstname + " " +
                               otherClient.lastname) if otherClient != None else "Not found"

            print(transactionTypeStr, amountStr, otherClientStr)

        print("---------------------------------------")

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
