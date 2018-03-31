import os

os.system("sudo apt-get update")
os.system("sudo apt-get upgrade")

os.system("sudo apt-get install python-setuptools")
os.system("sudo easy_install pip")

os.system("sudo pip install -U ubidots==1.6.6")
os.system("sudo pip install paho-mqtt")

print ("Instalation finished")
