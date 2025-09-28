class KassenzettelItem:
    price = False
    name = False
    date = False

    def __init__(self,price,name,date):
        self.price = price
        self.name = name
        self.date = date
