import cv2
import easyocr
import re
from datetime import date
from KassenzettelFunctions import *
from KassenzettelItem import *

reader = easyocr.Reader(['de']) # this needs to run only once to load the model into memory


image = cv2.imread('Aldi2.jpg')



#resize image for faster reading

image = resize_image(image,1500)
result = reader.readtext(image)
print(result)

stores = ["Edeka", "REWE","Aldi","go asia","Wolf","Asia Markt","dm"]


sort_from_top(result)

dateOfKassenzettel= str(date.today())
recognisedStore = False
start = False
end = False
gridItems =[]


for item in result:
    text = item[1]

    # is date
    potentialDate = re.search("[0-9][0-9].[0-9][0-9].[0-9][0-9][0-9][0-9]", text)
    if potentialDate:
        dateOfKassenzettel = potentialDate.start()

    for possibleStore in stores:
        if item[1].lower().startswith(possibleStore.lower()):
            recognisedStore = possibleStore

    if not start:
        if text.lower() == "eur":
            start = item
            print(start)

    if not end:
        if text.lower().replace(" ", "") == "summe":
            end = item

    if start and not end:
        gridItems.append(item)


kassenzettelItems=[]

usedItemList = gridItems if gridItems else result

for item in result:
    index = result.index(item)
    text = item[1]
    print(text)
    if same_column(item,start):
        price = False
        #Price is recognised with A or B
        if re.search("^[0-9]*[,.][0-9][0-9] [abAB]W?$", text):
            price = re.sub(" [abAB]","",text)
        # Price is recognised without A or B
        elif re.search("^[0-9]*[,.][0-9][0-9]$", text):
                for other in other_items_within_range(result,item,5):
                    if re.search("^[abAB]W?$",other[1]) and get_x(item) < get_x(other):
                        price = text
                        break
        if price:
            potentialItemName = ""
            closestNameCandidate= (None,get_y(item))
            for other in other_items_within_range(result,item,5):
                distance = abs(get_y(item) - get_y(other))
                if distance < closestNameCandidate[1]:
                    closestNameCandidate = (other,distance)

            potentialNameParts = []
            for other in other_items_within_range(result, item, 5):
                if closestNameCandidate[0] and get_height(closestNameCandidate[0])/2 > abs(get_y(closestNameCandidate[0])-get_y(other)):
                    potentialNameParts.append(other)

            potentialNameParts.sort(key=lambda potential_name_part: abs(get_y(item) - get_y(potential_name_part)),reverse=True)
            for namePart in  potentialNameParts:
                if len(namePart[1]) > 3 and not namePart[1] == text:
                        for part in namePart[1].split():
                            if len(part) > 1 and not re.search("^[0-9]+$",part):
                                potentialItemName += " " +part
            potentialItemName = potentialItemName.strip()
            if not re.search("Pfand|Summe|Total",potentialItemName):
                kassenzettelItems.append(KassenzettelItem(price, potentialItemName, dateOfKassenzettel))


print("Du warst am",dateOfKassenzettel, "im",recognisedStore)
print("Und hast folgendes gekauft:")
for item in kassenzettelItems:
    print(item.name, item.price)
