-------------initialization and installation---------------

1. Please run the file: "install.py" in the "install" folder with python3.
2. Please run the file: "init.py" in the "init" folder with python3.

----------------------Configuration------------------------

You should edit the Configuration file before you launch the program for the first time.
There is a "Config_data.txt" file in the "Configuration_data" folder.
This file records information about this controller listed as below:
	1. "buildingid = xxxx" : it stands for the buildingid of the building that this controller controls.
	2. "address = xxxx" : it stands for the address of MQTT server.
	3. "port = xxxx" : it stands for the port the server open to this Raspberry Pi controller.
	4. "timeInterval = xxxx" : it stands for the time interval between the collection of SOS data.
	5. "temperature = temp1, temp2, temp3" 
		"pressure = p1, p2, p3" : it stands for the number and the display names of the sensors.
		For an example, in this case there are 3 temperature sensors whose dataID and names are : "temperature 1 --- temp1", "temperature 2 --- temp2", "temperature 3 --- temp3"

Be careful! There are rules for editing the "Config_data.txt" file:
	1. All the strings before "=" can not be changed!
	2. The "buildingid" row has to be the first row, and the "address" row has to be the second row!
	3. The unit of time interval is second(s).
	4. Display names of sensors which have the same type should be in the same row and seperated by comma.
	5. Please make sure the program is no running when you editing the file.

---------------------------Launch--------------------------

1. Please run the "main.py" with python3. This program would collect and send SOS data to sever.
2. Please run the "listener.py" with python3. This program subscribes infomation from MQTT server.

-------------------------Data files------------------------

SOS_data folder:
It has two kind of files. "data_property" records the display names, unit infomation and data ID of sensors.
The SOS data files are named by the date of the records. For example:"2018-01-18".

COM_Record folder:
It has only one file: "Command(COM) Data.csv". This file records all command that has been send to this controller.

OPI_Record folder:
It has only one file: "Optimization inpu(OPI) Data.csv" This file records all OPI updates of this controller.