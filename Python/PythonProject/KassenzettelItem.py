from datetime import date
import json

class KassenzettelItem:
    price = False
    name = False

    def __init__(self,price,name):
        self.price = price
        self.name = name


    def to_dict(self):
        return {"name": self.name, "price": self.price}



class KassenzettelResult:
    items = []
    laden = ""
    datum = str(date.today())

    def __init__(self,laden,datum):
        self.laden = laden
        self.datum = datum
        print(datum)

    def add_item(self, item):
        self.items.append(item)

    def to_dict(self):
        # wandelt die komplette Klasse in dict um, inkl. Liste von Items
        return {
            "laden": self.laden,
            "datum": self.datum,
            "items": [item.to_dict() for item in self.items]
        }

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)