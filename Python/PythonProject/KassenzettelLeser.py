import easyocr
reader = easyocr.Reader(['de']) # this needs to run only once to load the model into memory



result = reader.readtext('Test.jpg')

for item in result:
    print(item,type(item))