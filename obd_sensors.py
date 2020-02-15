#!/usr/bin/env python
###########################################################################
# obd_sensors.py
#
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)
# Copyright 2009 Secons Ltd. (www.obdtester.com)
#
# This file is part of pyOBD.
#
# pyOBD is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# pyOBD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyOBD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###########################################################################

def hex_to_int(str):
    i = eval("0x" + str, {}, {})
    return i

def maf(code):
    code = hex_to_int(code)
    return code / 100

def throttle_pos(code):
    code = hex_to_int(code)
    return code * 100.0 / 255.0

def intake_m_pres(code): # in kPa
    code = hex_to_int(code)
    return code
  
def rpm(code):
    code = hex_to_int(code)
    return code / 4

def speed(code):
    code = hex_to_int(code)
    return code

def percent_scale(code):
    code = hex_to_int(code)
    return code * 100.0 / 255.0

def timing_advance(code):
    code = hex_to_int(code)
    return (code - 128) / 2.0

def sec_to_min(code):
    code = hex_to_int(code)
    return code / 60

def temp(code):
    code = hex_to_int(code)
    return code - 40 

def ctemp(code):
    code = hex_to_int(code)
    return code/10.0 - 40 


def cpass(code):
    #fixme
    return code

def fuel_trim_percent(code):
    code = hex_to_int(code)
    #return (code - 128.0) * 100.0 / 128
    return (code - 128) * 100 / 128

def oxygen_sensor_percent(code):
    code = hex_to_int(code)
    code = (code << 2) & 0xff;
    return (code - 128.0) * 100.0 / 128.0

def oxygen_sensor_voltage(code):
    code = hex_to_int(code)
    code = code & 0xff;
    return (code / 200.0)

def oxygen_sensor_current(code):
    code = hex_to_int(code)
    code = code & 0xffff
    return code / 256.0 - 128.0


def fuel_rail_pressure_abs(code):
    code = hex_to_int(code)
    return (code * 10)

def fuel_rail_pressure_rel(code):
    code = hex_to_int(code)
    return (code * 0.079)

def egr_percent(code):
    code = hex_to_int(code)
    return code * 100.0 / 255

def egr_err_percent(code):
    code = hex_to_int(code)
    return (code - 128.0) * 100.0 / 128

def evap_purge_percent(code):
    code = hex_to_int(code)
    return code * 100.0 / 255

def fuel_level(code):
    code = hex_to_int(code)
    return code * 100.0 / 255

def evap_pressure(code):
    code = hex_to_int(code)
    return code / 4.0

def evap_pressure2(code):
    code = hex_to_int(code)
    return code - 32767

def evap_abs_pressure(code):
    code = hex_to_int(code)
    return code / 200.0



def inj_timing(code):
    code = hex_to_int(code)
    return (code - 26880) / 128.0


def fuel_rate(code):
    code = hex_to_int(code)
    return code * 0.05








def dtc_decrypt(code):
    #first byte is byte after PID and without spaces
    num = hex_to_int(code[:2]) #A byte
    res = []

    if num & 0x80: # is mil light on
        mil = 1
    else:
        mil = 0
        
    # bit 0-6 are the number of dtc's. 
    num = num & 0x7f
    
    res.append(num)
    res.append(mil)
    
    numB = hex_to_int(code[2:4]) #B byte
      
    for i in range(0,3):
        res.append(((numB>>i)&0x01)+((numB>>(3+i))&0x02))
    
    numC = hex_to_int(code[4:6]) #C byte
    numD = hex_to_int(code[6:8]) #D byte
       
    for i in range(0,7):
        res.append(((numC>>i)&0x01)+(((numD>>i)&0x01)<<1))
    
    res.append(((numD>>7)&0x01)) #EGR SystemC7  bit of different 
    
    return res
    #return "#"

def hex_to_bitstring(str):
    bitstring = ""
    for i in str:
        # silly type safety, we don't want to eval random stuff
        if type(i) == type(''): 
            v = eval("0x%s" % i)
            if v & 8 :
                bitstring += '1'
            else:
                bitstring += '0'
            if v & 4:
                bitstring += '1'
            else:
                bitstring += '0'
            if v & 2:
                bitstring += '1'
            else:
                bitstring += '0'
            if v & 1:
                bitstring += '1'
            else:
                bitstring += '0'                
    return bitstring

class Sensor:
    def __init__(self, shortName, sensorName, sensorcommand, sensorValueFunction, u):
        self.shortname = shortName
        self.name = sensorName
        self.cmd  = sensorcommand
        self.value= sensorValueFunction
        self.unit = u

SENSORS = [
    Sensor("pids"                  , "Supported PIDs"				, "0100" , hex_to_bitstring ,""       ), 
    Sensor("dtc_status"            , "S-S DTC Cleared"				, "0101" , dtc_decrypt      ,""       ),    
    Sensor("dtc_ff"                , "DTC C-F-F"				, "0102" , cpass            ,""       ),      
    Sensor("fuel_status"           , "Fuel System Stat"				, "0103" , cpass            ,""       ),
    Sensor("load"                  , "Calc Load Value"				, "0104" , percent_scale    ,""       ),    
    Sensor("temp"                  , "Coolant Temp"				, "0105" , temp             ,"C"      ),
    Sensor("short_term_fuel_trim_1", "S-T Fuel Trim"				, "0106" , fuel_trim_percent,"%"      ),
    Sensor("long_term_fuel_trim_1" , "L-T Fuel Trim"				, "0107" , fuel_trim_percent,"%"      ),
    Sensor("short_term_fuel_trim_2", "S-T Fuel Trim"				, "0108" , fuel_trim_percent,"%"      ),
    Sensor("long_term_fuel_trim_2" , "L-T Fuel Trim"				, "0109" , fuel_trim_percent,"%"      ),
    Sensor("fuel_pressure"         , "FuelRail Pressure"			, "010A" , cpass            ,""       ),
    Sensor("manifold_pressure"     , "Intk Manifold"				, "010B" , intake_m_pres    ,"kPa"    ),
    Sensor("rpm"                   , "Engine RPM"				, "010C" , rpm              ,""       ),
    Sensor("speed"                 , "Vehicle Speed"				, "010D" , speed            ,"km/h"    ),
    Sensor("timing_advance"        , "Timing Advance"				, "010E" , timing_advance   ,"degrees"),
    Sensor("intake_air_temp"       , "Intake Air Temp"				, "010F" , temp             ,"C"      ),
    Sensor("maf"                   , "AirFlow Rate(MAF)"			, "0110" , maf              ,"g/s" ),
    Sensor("throttle_pos"          , "Throttle Position"			, "0111" , throttle_pos     ,"%"      ),
    Sensor("secondary_air_status"  , "2nd Air Status"				, "0112" , cpass            ,""       ),
    Sensor("o2_sensor_positions"   , "Loc of O2 sensors"			, "0113" , cpass            ,""       ),
    Sensor("o211-a"                , "O2 Sensor current: 1 - 1"			, "0134" , oxygen_sensor_current,"mA"      ),
    Sensor("o211"                  , "O2 Sensor: 1 - 1"				, "0114" , oxygen_sensor_percent,"%"      ),
    Sensor("o212"                  , "O2 Sensor: 1 - 2"				, "0115" , oxygen_sensor_percent,"%"      ),
    Sensor("o213"                  , "O2 Sensor: 1 - 3"				, "0116" , oxygen_sensor_percent,"%"      ),
    Sensor("o214"                  , "O2 Sensor: 1 - 4"				, "0117" , oxygen_sensor_percent,"%"      ),
    Sensor("o221"                  , "O2 Sensor: 2 - 1"				, "0118" , oxygen_sensor_percent,"%"      ),
    Sensor("o222"                  , "O2 Sensor: 2 - 2"				, "0119" , oxygen_sensor_percent,"%"      ),
    Sensor("o223"                  , "O2 Sensor: 2 - 3"				, "011A" , oxygen_sensor_percent,"%"      ),
    Sensor("o224"                  , "O2 Sensor: 2 - 4"				, "011B" , oxygen_sensor_percent,"%"      ),
    Sensor("o211-v"                , "O2 Sensor: 1 - 1"				, "0114" , oxygen_sensor_voltage,"V"      ),
    Sensor("o212-v"                , "O2 Sensor: 1 - 2"				, "0115" , oxygen_sensor_voltage,"V"      ),
    Sensor("o213-v"                , "O2 Sensor: 1 - 3"				, "0116" , oxygen_sensor_voltage,"V"      ),
    Sensor("o214-v"                , "O2 Sensor: 1 - 4"				, "0117" , oxygen_sensor_voltage,"V"      ),
    Sensor("o221-v"                , "O2 Sensor: 2 - 1"				, "0118" , oxygen_sensor_voltage,"V"      ),
    Sensor("o222-v"                , "O2 Sensor: 2 - 2"				, "0119" , oxygen_sensor_voltage,"V"      ),
    Sensor("o223-v"                , "O2 Sensor: 2 - 3"				, "011A" , oxygen_sensor_voltage,"V"      ),
    Sensor("o224-v"                , "O2 Sensor: 2 - 4"				, "011B" , oxygen_sensor_voltage,"V"      ),
    Sensor("obd_standard"          , "OBD Designation"				, "011C" , cpass            ,""       ),
    Sensor("o2_sensor_position_b"  , "Loc of O2 sensor" 			, "011D" , cpass            ,""       ),
    Sensor("aux_input"             , "Aux input status"				, "011E" , cpass            ,""       ),
    Sensor("engine_time"           , "Engine Start MIN"				, "011F" , sec_to_min       ,"min"    ),

    Sensor("engine_mil_distance"     , "Engine Distance MIL"	                , "0121" , cpass                        ,"km"    ),
    Sensor("fuel_rail_pressure_rel"  , "Fuel rail pressure (relative)"		, "0122" , fuel_rail_pressure_rel       ,"kPa"    ),
    Sensor("fuel_rail_pressure_abs"  , "Fuel rail pressure (absolute)"		, "0123" , fuel_rail_pressure_abs       ,"kPa"    ),
    Sensor("to_be_implemented"       , "24 To be implemented"		        , "0124" , cpass                        ,"..."    ),
    Sensor("to_be_implemented"       , "25 To be implemented"		        , "0125" , cpass                        ,"..."    ),
    Sensor("to_be_implemented"       , "26 To be implemented"		        , "0126" , cpass                        ,"..."    ),
    Sensor("to_be_implemented"       , "27 To be implemented"		        , "0127" , cpass                        ,"..."    ),
    Sensor("to_be_implemented"       , "28 To be implemented"		        , "0128" , cpass                        ,"..."    ),
    Sensor("to_be_implemented"       , "29 To be implemented"		        , "0129" , cpass                        ,"..."    ),
    Sensor("to_be_implemented"       , "2A To be implemented"		        , "012A" , cpass                        ,"..."    ),
    Sensor("to_be_implemented"       , "2B To be implemented"		        , "012B" , cpass                        ,"..."    ),
    Sensor("egr_percent"             , "Commanded EGR"              		, "012C" , egr_percent                  ,"%"    ),
    Sensor("egr_err_percent"         , "EGR error"	                 	, "012D" , egr_err_percent              ,"%"    ),
    Sensor("evap_purge_percent"      , "Commanded EVAP purge"		        , "012E" , evap_purge_percent           ,"%"    ),
    Sensor("fuel_level"              , "Fuel level"		                , "012F" , fuel_level                   ,"%"    ),

    Sensor("starts_since_clear"      , "Warm starts since DTC clear"		, "0130" , cpass     ,""    ),
    Sensor("distance_since_clear"    , "Distance since DTC clear"		, "0131" , cpass     ,"km"    ),
    Sensor("evap_pressure"           , "Evap vapor pressure"		        , "0132" , evap_pressure     ,"Pa"    ),
    Sensor("baro_pressure"           , "Barometric pressure"		        , "0133" , cpass     ,"kPa"    ),
    Sensor("to_be_implemented"       , "34 To be implemented"		        , "0134" , cpass                        ,"..."    ),
    Sensor("to_be_implemented"       , "35 To be implemented"		        , "0135" , cpass                        ,"..."    ),
    Sensor("to_be_implemented"       , "36 To be implemented"		        , "0136" , cpass                        ,"..."    ),
    Sensor("to_be_implemented"       , "37 To be implemented"		        , "0137" , cpass                        ,"..."    ),
    Sensor("to_be_implemented"       , "38 To be implemented"		        , "0138" , cpass                        ,"..."    ),
    Sensor("to_be_implemented"       , "39 To be implemented"		        , "0139" , cpass                        ,"..."    ),
    Sensor("to_be_implemented"       , "3A To be implemented"		        , "013A" , cpass                        ,"..."    ),
    Sensor("to_be_implemented"       , "3B To be implemented"		        , "013B" , cpass                        ,"..."    ),
    Sensor("to_be_implemented"       , "3C To be implemented"		        , "013C" , cpass                        ,"..."    ),
    Sensor("to_be_implemented"       , "3D To be implemented"		        , "013D" , cpass                        ,"..."    ),
    Sensor("to_be_implemented"       , "3E To be implemented"		        , "013E" , cpass                        ,"..."    ),
    Sensor("to_be_implemented"       , "3F To be implemented"		        , "013F" , cpass                        ,"..."    ),
 

    Sensor("voltage"                 , "ECU voltage"		                , "0142" , cpass     ,"mV"    ),
    Sensor("load2"                   , "Calc Load Valu"				, "0143", percent_scale    ,"%"       ),    
    Sensor("to_be_implemented"       , "44 To be implemented"                   , "0144" , cpass                        ,"..."    ),
    Sensor("throttle_pos2"           , "Throttle Position"                      , "0145" , throttle_pos     ,"%"      ),
    Sensor("ambient_temp"            , "Ambient temperature"     		, "0146" , temp     ,"C"    ),

    Sensor("engine_mil_time"         , "Engine Run MIL"				, "014D" , sec_to_min       ,"min"    ),
    Sensor("engine_clear_time"       , "Engine Run since clear"			, "014E" , sec_to_min       ,"min"    ),

    Sensor("evap_abs_pressure"       , "Evap absolute vapor pressure"		, "0153" , evap_abs_pressure     ,"kPa"    ),
    Sensor("evap_pressure2"          , "Evap vapor pressure"		        , "0154" , evap_pressure2        ,"Pa"    ),
    Sensor("fuel_rail_pressure_abs2" , "Fuel rail pressure (absolute)"		, "0159" , fuel_rail_pressure_abs       ,"kPa"    ),
    Sensor("accel_position"          , "Accelerator Position"                   , "015A" , throttle_pos     ,"%"      ),

    Sensor("oil_temp"                , "Oil temperature"         		, "015C" , temp     ,"C"    ), 
    Sensor("injection_timing"        , "Injection timing"	         	, "015D" , inj_timing     ,"DEG"    ),
    Sensor("fuel_rate"               , "Fuel rate"		                , "015E" , fuel_rate     ,"L/h"    ),
    

    ]
     
    
#___________________________________________________________

def test():
    for i in SENSORS:
        print(i.name, i.value("F"))

if __name__ == "__main__":
    import sys
    print(oxygen_sensor_current(sys.argv[1]))
