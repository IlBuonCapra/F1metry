#http://forums.codemasters.com/discussion/53139/f1-2017-d-box-and-udp-output-specification/
#http://forums.codemasters.com/discussion/46726/d-box-and-udp-telemetry-information

import socket
import struct

UDP_IP = "127.0.0.1"
UDP_PORT = 20777

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

test = True

mph_to_kmh = 2.239*1.60934

laptime_value = 0
time_minutes = 0
time_seconds = 0
time_milles = 0
lapdistance_value = 0
totaldistance_value = 0
speed_value = 0
throttle_value = 0
steer_value = 0
brake_value = 0
gear_value = 0
lap_value =
engineRate_value = 0
carPosition_value = 0
drs_value = 0
inPit_value = 0
sector_n = 0
sector1 = 0
sector2 = 0
sector3 = 0
totalLaps_value = 0
lasLapTime_value = 0

lapTime = True
lapDistance = False
totalDistance = False
speed = False
throttle = False
steer = False
brake = False
gear = False
lap = False
engineRate = False
carPosition = False
drs = False
inPit = False
sector = False
totalLaps = False
lastLapTime = False
era = False

while True:
    data, addr = sock.recvfrom(1237)

    i = 0
    x = 0
    y = 4

    if data:
        while (i <= 75):
            output = struct.unpack('f', data[x:y])

            if lapTime and i == 1:
                laptime_value = output[0]
                time_minutes = int(laptime_value//60)
                time_seconds = int(laptime_value-(60*time_minutes))
                time_milles = '{:03d}'.format(int((laptime_value-(time_seconds+(time_minutes*60)))*1000))
                if test:
                    print(laptime_value,"|",time_minutes,":",time_seconds,":",time_milles)


            if lapDistance and i == 2:
                lapdistance_value = output[0]
                if test:
                    print("DISTANCE CURRENT LAP =", lapdistance_value)

            if totalDistance and i == 3:
                totaldistance_value = output[0]
                if test:
                    print("TOTAL DISTANCE =",totaldistance_value)


            if speed and i == 7:
                speed_value = int(output[0]*mph_to_kmh)
                if test:
                    print ("SPEED' =",speed_value)


            if throttle and i == 29:
                throttle_value = int(output[0]*100)
                if test:
                    print ("THROTTLE =",throttle_value)


            if steer and i == 30:
                steer_value = int(output[0]*100)
                if test:
                    print("STEER =",steer_value)


            if brake and i == 31:
                brake_value = int(output[0]*100)
                if test:
                    print ("BRAKE =",brake_value)


            if gear and i == 33:
                gear_value = int(output[0])
                if test:
                    if gear_value == 0:
                        print ("GEAR = R")
                    elif gear_value == 1:
                        print ("GEAR = N")
                    else:
                        print ("GEAR =", int(output[0]-1))


            if lap and i == 36:
                lap_value = int(output[0]+1)
                if test:
                    print("CURRENT LAP NUMBER =",lap_value)


            if engineRate and i == 37:
                engineRate_value = int(output[0])
                if test:
                    print("ENGINE RATE =",engineRate_value)


            if carPosition and i == 39:
                carPosition_value = output[0]
                if test:
                    print("CAR POSITION =",carPosition_value)


            if drs and i == 42:
                drs_value = output[0]
                if test:
                    if drs_value == 0:
                        print("DRS CLOSE")
                    elif drs_value == 1:
                        print("DRS OPEN")
                    else:
                        print("DRS UNKNOWN")


            if inPit and i == 47:
                inPit_value = inoutput[0]
                if test:
                    if inPit_value == 2:
                        print("AT BOX")
                    elif inPit_value == 1:
                        print("IN PIT LANE")
                    elif inPit_value == 0:
                        print("IN TRACK")


            if sector:
                if i == 48:
                    sector_n = int(output[0] + 1)
                if i == 49 and output[0]!=0:
                    sector1 = output[0]
                if i == 50 and output[0]!=0:
                    sector2 = output[0]
                if sector1!=0 and sector2!=0 and lapdistance_value<=100:
                    sector3 = (lasLapTime_value - sector1) - sector2
                if lapdistance_value>600 and lapdistance_value<700:
                    sector1 = 0
                    sector2 = 0
                    sector3 = 0
                if test:
                    print("SECTOR NUMBER =",sector_n,"SECTOR1 =",sector1,"SECTOR2 =",sector2,"SECTOR3 =",sector3)

            #DA MODIFICARE
            if teamInfo and i == 59:
                teaminfo_value = output[0]
                if test:
                    if era == 0:
                        if teaminfo_value == 0:
                            print("TEAM = REDBULL")
                        if teaminfo_value == 1:
                            print("TEAM = FERRARI")
                        if teaminfo_value == 2:
                            print("TEAM = MCLAREN")
                        if teaminfo_value == 3:
                            print("TEAM = RENAULT")
                        if teaminfo_value == 4:
                            print("TEAM = MERCEDES")
                        if teaminfo_value == 5:
                            print("TEAM = SAUBER")
                        if teaminfo_value == 6:
                            print("TEAM = FORCE INDIA")
                        if teaminfo_value == 7:
                            print("TEAM = WILLIAMS")
                        if teaminfo_value == 8:
                            print("TEAM = TORO ROSSO")
                        if teaminfo_value == 11:
                            print("TEAM = HAAS")
                    if era == 1:
                        if teaminfo_value == 0:
                            print("TEAM = WILLIAMS 192")
                        if teaminfo_value == 1:
                            print("TEAM = WILLIAMS 1998")
                        if teaminfo_value == 2:
                            print("TEAM = MCLAREN 2008")
                        if teaminfo_value == 3:
                            print("TEAM = FERRARI 2004")
                        if teaminfo_value == 4:
                            print("TEAM = FERRARI 1995")
                        if teaminfo_value == 5:
                            print("TEAM = FERRARI 2007")
                        if teaminfo_value == 6:
                            print("TEAM = MCLAREN 1998")
                        if teaminfo_value == 7:
                            print("TEAM = WILLIAMS 1996")
                        if teaminfo_value == 8:
                            print("TEAM = RENAULT 2006")
                        if teaminfo_value == 10:
                            print("TEAM = FERRARI 2002")
                        if teaminfo_value == 11:
                            print("TEAM = REDBULL 2010")
                        if teaminfo_value == 12:
                            print("TEAM = MCLAREN 1991")


            if totalLaps and i == 60:
                totalLaps_value = output[0]
                if test:
                    print("TOTAL LAPS = ", totalLaps_value)


            if lastLapTime and i == 62:
                lasLapTime_value = output[0]
                if test:
                    print("TIME LAST LAP = ", lasLapTime_value)

            if sessionType and i == 66:



            if era and i == 70:
                era_value = output[0]
                if test:
                    print("ERA =",era_value)



            i += 1
            x += 4
            y += 4
