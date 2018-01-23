import csv
import sys
import json
import string
import os
import datetime
import base64
from pub import *
    
def func_take_photo(building_id, server_address, command_parameter1, command_parameter2):
        
    #take photo and upload
    print('Taking photo with parameters: \"' + str(command_parameter1) + "," + str(command_parameter2) +"\"")
    
    #test picture
    with open('./pictures/test.jpg', 'rb') as f:
        picture = base64.b64encode(f.read())
    str_pic = picture.decode()
    packet = {'buildingId': building_id, 'time' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'picture' : str_pic}
    json_dic = json.dumps(packet, sort_keys = True, indent = 4, separators = (',',':'))
    print(json_dic)
    asyncio.get_event_loop().run_until_complete(pub_picture(json_dic, server_address))
    return 1
    
def func_function2(command_parameter1, command_parameter2):
        
    #do something
    print("Executing funtion 2 with parameters: \"" + str(command_parameter1) + "," + str(command_parameter2) +"\"")
    
    return 1

class COM_Controller:
    
    #establish record file
    def __init__(self) :
        
        #record file exists, return
        if os.path.exists('./COM_Record/Command(COM) Data.csv'):
            print ("File:\"COM_Record/Command(COM) Data.csv\"exsits. If you want to rewrite this file, please delete the file and restart the program.")
            return
        
        #Write file header
        unit_row = ['Time', 'Integer', 'Integer', 'Float', 'Float', 'Time', 'Integet']
        dataID_row = ['Command Time','Command ID', 'Command Type', 'Command Parameter 1', 'Command parameter 2', 'Action TIme', 'Action status']
        
        try:
            f = open('./COM_Record/Command(COM) Data.csv','w')
            writer = csv.writer(f)
            writer.writerows([unit_row, dataID_row])
            print ('Write header succeed: COM_Record/Command(COM) Data.csv')
            f.close()
        except IOError:
            print ("Could not write to file: COM_Record/Command(COM) Data.csv")
        finally:
            f.close()

    
    #command finished, record the action time and chan the action status of command record
    def com_set_status(self, server_address, building_id, com_id, status):
        
        
        print("******")
        #read last line
        with open('./COM_Record/Command(COM) Data.csv','r') as f:
            lines = f.readlines()
         
        #empty file
        if len(lines) <= 2 :
            print ("There is no record in file: \"COM_Record/Command(COM) Data.csv\"")
            return False
        
        data = []
        for i in range(len(lines)):
            lines[i] = lines[i].replace('\r\n','')
            temp = lines[i].split(',')
            data.append(temp)
        
        #find the target record according to com_id
        l = len(data)
        for i in range(len(data)):
            print(com_id + " " + str(data[l-i-1][1]))
            if data[l-i-1][1] == com_id :
                data[l-i-1][5] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data[l-i-1][6] = status
                
                packet = {'buildingId' : building_id, 'commmandId' : com_id, 'actionTime' : data[l-i-1][5], 'actionStatus' : status}
                json_dic = json.dumps(packet, sort_keys = True, indent = 4, separators = (',',':'), ensure_ascii = True)
                print (json_dic)
                #send packet to server to response commands
                asyncio.get_event_loop().run_until_complete(pub_comRes(json_dic, server_address, building_id))
                print(building_id)
                try:
                    f = open('./COM_Record/Command(COM) Data.csv','w')
                    writer = csv.writer(f)
                    writer.writerows(data)
                    print ('Write row succeed: COM_Record/Command(COM) Data.csv')
                    f.close()
                except IOError:
                    print ("Could not write to file: COM_Record/Command(COM) Data.csv")
                finally:
                    f.close()

                return True
        
        print ("There is no command record which has the com_id: \"" + str(com_id) +"\"")
        
        return False
    
    #execute the command
    def execute_command(self, server_address, building_id, com_id, command_type, command_parameter1, command_parameter2):
        
        print (command_type)
        
        if command_type == 1 :    #take photo
            out = func_take_photo(building_id, server_address, command_parameter1, command_parameter2)
            self.com_set_status(server_address, building_id, com_id, out)
            return out
        elif command_type == 2 :    #funcion 2
            out = func_function2(command_parameter1, command_parameter2)
            self.com_set_status(server_address, building_id, com_id, out)
            return out
        else:
            return -1
    
    #insert a new command record in the end of COM data file and execute the command
    def new_command(self, server_address, building_id, time, com_id, command_type, command_parameter1, command_parameter2):

        entry = [time, com_id, command_type, command_parameter1, command_parameter2, None, 0]
        
        print (entry)
        
        try:
            f = open('./COM_Record/Command(COM) Data.csv','a')
            writer = csv.writer(f)
            writer.writerow(entry)
            print ('Write row succeed: COM_Record/Command(COM) Data.csv')
            f.close()
        except IOError:
            print ("Could not write to file: COM_Record/Command(COM) Data.csv")
        finally:
            f.close()
        
        return self.execute_command(server_address, building_id, com_id, command_type, command_parameter1, command_parameter2)

    
    