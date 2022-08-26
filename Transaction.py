class Transaction:

    def __init__(self, type: int, otherClientId: int, amount: float):
        self.type = type
        self.otherClientId = otherClientId
        self.amount = amount
