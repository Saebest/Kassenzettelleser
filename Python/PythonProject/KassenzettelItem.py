from datetime import date
class KassenzettelItem:
    price = False
    name = False

    def __init__(self,price,name):
        self.price = price
        self.name = name


class KassenzettelResult:
    items = []
    laden = ""
    datum = str(date.today())

    def __init__(self,laden,datum):
        self.laden = laden
        self.datum = datum

    def add_item(self, item):
        self.items.append(item)