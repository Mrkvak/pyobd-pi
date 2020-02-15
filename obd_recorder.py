#!/usr/bin/env python2

import obd_io
import serial
import platform
import obd_sensors
from datetime import datetime
import time
import getpass
import sys

from obd_utils import scanSerial

class OBD_Recorder():
    def __init__(self, path, log_items):
        self.port = None
        self.sensorlist = []
        localtime = time.localtime(time.time())
        filename = path+"car-"+str(localtime[0])+"-"+str(localtime[1])+"-"+str(localtime[2])+"-"+str(localtime[3])+"-"+str(localtime[4])+"-"+str(localtime[5])+".log"
        self.log_file = open(filename, "w", 128)
#        self.log_file.write("Time,RPM,km/h,Throttle,Load,S-T fuel trim,L-T fuel trim,Coolant temp,Intake manifold pressure,Timing advance,Intake air temp,Air flow rate (MAF),O2 sensor 1-2 percent,O2 sensor 1-2 volts,Fuel Status\n");
#        self.log_file.write("Time,Throttle,O2 sensor 1-1 current, O2 sensor 1-2 volts\n");
        self.log_file.write("Time,O2 sensor 1-1 current, O2 sensor 1-2 volts\n");

        print("Time,O2 sensor 1-1 current, O2 sensor 1-2 volts\n");


        for item in log_items:
            self.add_log_item(item)

        self.gear_ratios = [34/13, 39/21, 36/23, 27/20, 26/21, 25/22]
        #log_formatter = logging.Formatter('%(asctime)s.%(msecs).03d,%(message)s', "%H:%M:%S")

    def connect(self):
        portnames = scanSerial()
        #portnames = ['COM10']
        print portnames
        for port in portnames:
            self.port = obd_io.OBDPort(port, None, 2, 2)
            if(self.port.State == 0):
                self.port.close()
                self.port = None
            else:
                break

        if(self.port):
            print "Connected to "+self.port.port.name
            
    def is_connected(self):
        return self.port
        
    def add_log_item(self, item):
        for index, e in enumerate(obd_sensors.SENSORS):
            if(item == e.shortname):
                self.sensorlist.append(index)
                print "Logging item: "+e.name
                break
            
            
    def record_data(self):
        if(self.port is None):
            return None
        
        print "Logging started"
        
        while 1:
            localtime = datetime.now()
            current_time = str(localtime.hour)+"-"+str(localtime.minute)+"-"+str(localtime.second)+"."+str(localtime.microsecond/1000)
            log_string = current_time
            results = {}
            for index in self.sensorlist:
                (name, value, unit) = self.port.sensor(index)
                log_string = log_string + ","+str(value)
                results[obd_sensors.SENSORS[index].shortname] = value;

            #gear = self.calculate_gear(results["rpm"], results["speed"])
            log_string = log_string #+ "," + str(gear)
            self.log_file.write(log_string+"\n")
            print(log_string)
            sys.stdout.flush()

            
    def calculate_gear(self, rpm, speed):
        if speed == "" or speed == 0:
            return 0
        if rpm == "" or rpm == 0:
            return 0

        rps = rpm/60
        mps = (speed*1.609*1000)/3600
        
        primary_gear = 85/46 #street triple
        final_drive  = 47/16
        
        tyre_circumference = 1.978 #meters

        current_gear_ratio = (rps*tyre_circumference)/(mps*primary_gear*final_drive)
        
        #print current_gear_ratio
        gear = min((abs(current_gear_ratio - i), i) for i in self.gear_ratios)[1] 
        return gear
        
username = getpass.getuser()  
#time,RPM,km/h,Throttle,Load,S-T fuel trim,L-T fuel trim,Coolant temp,Intake manifold pressure,Timing advance,Intake air temp,Air flow rate (MAF),O2 sensor 1-2 percent,O2 sensor 1-2 volts,Fuel Status\n");
#Time,RPM,Throttle,S-T fuel trim,L-T fuel trim,O2 sensor 1-1 current, O2 sensor 1-2 volts
logitems = ["o211-a", "o212-v"]
#o = OBD_Recorder('/home/'+username+'/pyobd-pi/log/', logitems)
o = OBD_Recorder('./log/', logitems)

o.connect()

if not o.is_connected():
    print "Not connected"
o.record_data()
