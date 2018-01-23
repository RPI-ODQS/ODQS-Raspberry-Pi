import csv
import sys
import string
import os

class OPI_Record:
    
    #establish record file
    def __init__(self) :
        
        #record file exists, return
        if os.path.exists('./OPI_Record/Optimization Input(OPI) Data.csv'):
            print ("File:\"OPI_Record/Optimization Input(OPI) Data.csv\"exsits. If you want to rewrite this file, please delete the file and restart the program")
            return
        
        #Write file header
        unit_row = ['Time', 'Integer']
        dataID_row = ['Data ID', 'Optimization Type']
        
        for i in range(2):
            unit_row.append('Float')
            dataID_row.append('Optimization Parameter ' + str(i+1))
        for i in range(24):
            unit_row.append('Float')
            dataID_row.append('Hot Water Demand ' + str(i+1))
        for i in range(24):
            unit_row.append('Float')
            dataID_row.append('Electricity Price ' + str(i+1))
        for i in range(24):
            unit_row.append('Float')
            dataID_row.append('Ambient Temperature ' + str(i+1))
        for i in range(24):
            unit_row.append('Float')
            dataID_row.append('Solar Generation ' + str(i+1))
        for i in range(24):
            unit_row.append('Float')
            dataID_row.append('Demand Response ' + str(i+1))
        
        
        try:
            f = open('./OPI_Record/Optimization Input(OPI) Data.csv','w')
            writer = csv.writer(f)
            writer.writerows([unit_row, dataID_row])
            print ('Write header succeed: OPI_Record/Optimization Input(OPI) Data.csv')
            f.close()
        except IOError:
            print ("Could not write to file: OPI_Record/Optimization Input(OPI) Data.csv")
        finally:
            f.close()
    
    #add a new record in the end of the OPI data file
    def new_record(self, time, optimization_type, optimization_parameter, hot_water_demand, electricity_price, ambient_temperature, solar_generation, demand_response):
        
        self.time = time
        self.optimization_type = optimization_type
        self.optimization_parameter = optimization_parameter
        self.hot_water_demand = hot_water_demand
        self.electricity_price = electricity_price
        self.ambient_temperature = ambient_temperature
        self.solar_generation = solar_generation
        self.demand_response = demand_response
        
        print(optimization_parameter)
        print(hot_water_demand)
        
        entry = [time]
        entry.append(optimization_type)
        entry.extend(optimization_parameter)
        entry.extend(hot_water_demand)
        entry.extend(electricity_price)
        entry.extend(ambient_temperature)
        entry.extend(solar_generation)
        entry.extend(demand_response)
        
        try:
            f = open('./OPI_Record/Optimization Input(OPI) Data.csv','a')
            writer = csv.writer(f)
            writer.writerow(entry)
            print ('Write row succeed: OPI_Record/Optimization Input(OPI) Data.csv')
            f.close()
        except IOError:
            print ("Could not write to file: OPI_Record/Optimization Input(OPI) Data.csv")
        finally:
            f.close()

    #get the latest record of OPI data
    def get_latest(self):
        
        #if there is no record in memory, read file to get the last line.
        if not "self.optimization_type" in dir():
            
            #read last line
            with open('./OPI_Record/Optimization Input(OPI) Data.csv','r') as f:
                off = -100
                while True:
                    f.seek(off, 2)
                    lines = f.readlines()
                    if len(lines) >= 2 :
                        last_line_str = lines[-1]
                        break
                    off *= 2
            
            last_line_str = last_line_str.replace('\r\n', '')
            last_line = last_line_str.split(',')
            last_line[1] = int(last_line[1])
            
            i = 2
            while i < len(last_line):
                if last_line[i] != '':
                    last_line[i] = float(last_line[i])
                i += 1
            
            #if file is empty
            self.time = last_line[0]
            if self.time == 'Data ID':
                print ('Has no OPI_RECORD yet!')
                return
            
            self.optimization_type = last_line[1]
            self.optimization_parameter = last_line[2:4]
            self.hot_water_demand = last_line[4:28]
            self.electricity_price = last_line[28:52]
            self.ambient_temperature = last_line[52:76]
            self.solar_generation = last_line[76:100]
            self.demand_response = last_line[100:]
            
        data = {}
        data['time'] = self.time
        data['optimization_type'] = self.optimization_type
        data['optimization_parameter'] = self.optimization_parameter
        data['hot_water_demand'] = self.hot_water_demand
        data['electricty_price'] = self.electricity_price
        data['ambient_temperature'] = self.ambient_temperature
        data['solar_generation'] = self.solar_generation
        data['demand_response'] = self.demand_response
        
        return data