import base64

file = open('./test.jpg', 'rb')
pic = base64.b64encode(file.read())
print(type(pic))
strp = str(pic)
print(type(strp))
