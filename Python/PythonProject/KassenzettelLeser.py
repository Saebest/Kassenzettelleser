import cv2
import easyocr
from KassenzettelFunctions import *
reader = easyocr.Reader(['de']) # this needs to run only once to load the model into memory


image = cv2.imread('20250927_115336.jpg')
result = reader.readtext(image)

stores = ["Edeka", "REWE","Aldi","go asia","Wolf","Asia Markt","dm"]
recognisedStore = False

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

for item in result:
    text = item[1]
    if same_column(item,start):
        print(text)

print("Du warst im",recognisedStore)


