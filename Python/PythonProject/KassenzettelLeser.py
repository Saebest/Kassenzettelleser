import cv2
import easyocr
import re
from KassenzettelFunctions import *
from KassenzettelItem import *

reader = easyocr.Reader(['de']) # this needs to run only once to load the model into memory


image = cv2.imread('20250927_115312.jpg')



#resize image for faster reading
# new_width = min(1000,image.shape[1])
# ratio = new_width / image.shape[1]
# new_height = int(image.shape[0] * ratio)
#resized = cv2.resize(image, (new_width, new_height))
result = reader.readtext(image)
stores = ["Edeka", "REWE","Aldi","go asia","Wolf","Asia Markt","dm"]
recognisedStore = False
print(result)
sort_from_top(result)


for item in result:
    for possibleStore in stores:
        if item[1].lower().startswith(possibleStore.lower()):
            recognisedStore = possibleStore
            break

start = False


for item in result:
    text = item[1]
    if not start:
        if text.lower() == "eur":
            start = item
            break

kassenzettelItems=[]
for item in result:
    text = item[1]
    #print(text)
    if same_column(item,start):
        price = False
        #Price is recognised with A or B
        if re.search("^[0-9]*[,.][0-9][0-9] [abAB]$", text):
            print("Good",text)
            price = re.sub(" [abAB]","",text)
        # Price is recognised without A or B
        elif re.search("^[0-9]*[,.][0-9][0-9]$", text):
                print(text)
                for other in result:
                    if same_row(item,other) and re.search(other[1],"^[abAB]$") and get_x(item) < get_x(other):
                        price = text
                        break
        if price:
            potentialItemNames = []
            for other in result:
                if same_row(item,other) and len(other[1]) > 3 and not other[1] == text:
                    for part in other[1].split():
                        if len(part) > 1 and not re.search("^[0-9]+$",part):
                            potentialItemNames.append(part)

            name = max(potentialItemNames, key=len)
            if not name == "Pfand":
                kassenzettelItems.append(KassenzettelItem(price, name))


kassenzettelItems

print("Du warst im",recognisedStore)
print("Und hast folgendes gekauft:")
for item in kassenzettelItems:
    print(item.name, item.price)
