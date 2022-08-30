class Transaction:

    def __init__(self, type: int, otherClientId: int, amount: float, newBalance: float, day: int, month: int, year: int):
        self.type = type
        self.otherClientId = otherClientId
        self.amount = amount
        self.newBalance = newBalance
        self.day = day
        self.month = month
        self.year = year

    def date(self):
      return str(self.day) + "." + str(self.month) + "." + str(self.year)
