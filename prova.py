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

totalTime_value = 0
total_minutes = 0
total_seconds = 0
total_milles = 0
time_seconds = 0
time_milles = 0
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
lap_value = 0
engineRate_value = 0
carPosition_value = 0
drs_value = 0
fuelInTank_value = 0
fuelCapacity_value = 0
inPit_value = 0
sector_n = 0
sector1 = 0
sector2 = 0
sector3 = 0
brakesTemp_rl = 0
brakesTemp_rr = 0
brakesTemp_fl = 0
brakesTemp_fr = 0
tyrePress_r = 0
tyrePress_f = 0
totalLaps_value = 0
trackSize_value = 0
lastLapTime_value = 0
sessionType_value = 0
trackNumber_value = 0
flag_value = 0
era_value = 0
engineTemp_value = 0

totalTime = False
lapTime = False
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
fuelInTank = False
fuelCapacity = False
inPit = False
sector = False
brakesTemp = False
tyresPres = False
teamInfo = False
totalLaps = False
trackSize = False
lastLapTime = False
sessionType = False
trackNumber = False
flag = False
era = False
engineTemp = False

while True:
    data, addr = sock.recvfrom(1237)

    i = 0
    j = 0
    x = 324
    y = 0

    if data:
        while (i <= 121):
            if (i<=71) or (i==100):
                output = struct.unpack('f', data[x:x+4])

                if totalTime and i == 0:
                    totalTime_value = output[0]
                    total_minutes = int(totalTime_value//60)
                    total_seconds = int(totalTime_value-(60*total_minutes))
                    total_milles = '{:03d}'.format(int((totalTime_value-(total_seconds+(total_minutes*60)))*1000))
                    if test:
                        print(total_minutes,":",total_seconds,":",total_milles)

                if lapTime and i == 1:
                    laptime_value = output[0]
                    time_minutes = int(laptime_value//60)
                    time_seconds = int(laptime_value-(60*time_minutes))
                    time_milles = '{:03d}'.format(int((laptime_value-(time_seconds+(time_minutes*60)))*1000))
                    if test:
                        print(time_minutes,":",time_seconds,":",time_milles)

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
                    carPosition_value = int(output[0])
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

                if fuelInTank and i == 45:
                    fuelInTank_value = output[0]
                    if test:
                        print("FUEL IN TANK =",fuelInTank_value)

                if fuelCapacity and i == 46:
                    fuelCapacity_value = output[0]
                    if test:
                        print("FUEL CAPACITY =",fuelCapacity_value)

                if inPit and i == 47:
                    inPit_value = output[0]
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
                        sector1 = '{:.3f}'.format(output[0])
                    if i == 50 and output[0]!=0:
                        sector2 = '{:.3f}'.format(output[0])
                    if sector1!=0 and sector2!=0 and lapdistance_value<=100:
                        sector3 = '{:.3f}'.format((lastLapTime_value - float(sector1)) - float(sector2))
                    if lapdistance_value>600 and lapdistance_value<700:
                        sector1 = 0
                        sector2 = 0
                        sector3 = 0
                    if test:
                        print("SECTOR NUMBER =",sector_n,"SECTOR1 =",sector1,"SECTOR2 =",sector2,"SECTOR3 =",sector3)

                if brakesTemp:
                    if i == 51:
                        brakesTemp_rl = '{:06.2f}'.format(output[0])
                    if i == 52:
                        brakesTemp_rr = '{:06.2f}'.format(output[0])
                    if i == 53:
                        brakesTemp_fl = '{:06.2f}'.format(output[0])
                    if i == 54:
                        brakesTemp_fr = '{:06.2f}'.format(output[0])
                    if test:
                        print("BRAKE TEMP RL =",brakesTemp_rl,"BRAKE TEMP RR =",brakesTemp_rr,"BRAKE TEMP FL =",brakesTemp_fl,"BRAKE TEMP FR =",brakesTemp_fr)

                if tyresPres:
                    if i == 56:
                        tyrePress_r = output[0]
                    if i == 57:
                        tyrePress_f = output[0]
                    if test:
                        print("PRES REAR =",tyrePress_r,"PRES FRONT =",tyrePress_f)

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
                    totalLaps_value = int(output[0])
                    if test:
                        print("TOTAL LAPS =", totalLaps_value)

                if trackSize and i == 61:
                    trackSize_value = int(output[0])
                    if test:
                        print("TRACK SIZE =", trackSize_value)

                if lastLapTime and i == 62:
                    lastLapTime_value = output[0]
                    lastTime_minutes = int(lastLapTime_value//60)
                    lastTime_seconds = int(lastLapTime_value-(60*lastTime_minutes))
                    lastTime_milles = '{:03d}'.format(int((lastLapTime_value-(lastTime_seconds+(lastTime_minutes*60)))*1000))
                    if test:
                        print(lastTime_minutes,":",lastTime_seconds,":",lastTime_milles)

                if sessionType and i == 66:
                    sessionType_value = output[0]
                    if test:
                        if sessionType_value == 0:
                            print("SESSION TYPE = UNKNOWN")
                        if sessionType_value == 1:
                            print("SESSION TYPE = PRACTICE")
                        if sessionType_value == 2:
                            print("SESSION TYPE = QUALIFYING")
                        if sessionType_value == 3:
                            print("SESSION TYPE = RACE")

                if trackNumber and i == 68:
                    trackNumber_value = output[0]
                    if test:
                        if trackNumber_value == 0:
                            print("TRACK = MELBOURNE")
                        elif trackNumber_value == 1:
                            print("TRACK = SEPANG")
                        elif trackNumber_value == 2:
                            print("TRACK = SHANGHAI")
                        elif trackNumber_value == 3:
                            print("TRACK = BAHRAIN")
                        elif trackNumber_value == 4:
                            print("TRACK = CATALUNYA")
                        elif trackNumber_value == 5:
                            print("TRACK = MONACO")
                        elif trackNumber_value == 6:
                            print("TRACK = MONTREAL")
                        elif trackNumber_value == 7:
                            print("TRACK = SILVERSTONE")
                        elif trackNumber_value == 8:
                            print("TRACK = HOCKENHEIM")
                        elif trackNumber_value == 9:
                            print("TRACK = HUNGAROING")
                        elif trackNumber_value == 10:
                            print("TRACK = SPA")
                        elif trackNumber_value == 11:
                            print("TRACK = MONZA")
                        elif trackNumber_value == 12:
                            print("TRACK = SINGAPORE")
                        elif trackNumber_value == 13:
                            print("TRACK = SUZUKA")
                        elif trackNumber_value == 14:
                            print("TRACK = ABU DHABI")
                        elif trackNumber_value == 15:
                            print("TRACK = TEXAS")
                        elif trackNumber_value == 16:
                            print("TRACK = BRAZIL")
                        elif trackNumber_value == 17:
                            print("TRACK = AUSTRIA")
                        elif trackNumber_value == 18:
                            print("TRACK = SOCHI")
                        elif trackNumber_value == 19:
                            print("TRACK = MEXICO")
                        elif trackNumber_value == 20:
                            print("TRACK = BAKU")
                        elif trackNumber_value == 21:
                            print("TRACK = SAKHIR (SHORT)")
                        elif trackNumber_value == 22:
                            print("TRACK = SILVERSTONE (SHORT)")
                        elif trackNumber_value == 23:
                            print("TRACK = TEXAS (SHORT)")
                        elif trackNumber_value == 24:
                            print("TRACK = SUZUKA (SHORT)")
                        else:
                            print("TRACK = UNKNOWN")

                if flag and i == 69:
                    flag_value = output[0]
                    if test:
                        if flag_value == 0:
                            print("FLAG = NONE")
                        elif flag_value == 1:
                            print("FLAG = GREEN")
                        elif flag_value == 2:
                            print("FLAG = BLUE")
                        elif flag_value == 3:
                            print("FLAG = YELLOW")
                        elif flag_value == 4:
                            print("FLAG = RED")
                        else:
                            print("FLAG = UNKNOWN")

                if era and i == 70:
                    era_value = int(output[0])
                    if test:
                        print("ERA =",era_value)

                if engineTemp and i == 71:
                    engineTemp_value = '{:06.2f}'.format(output[0])
                    if test:
                        print("ENGINE TEMP =",engineTemp_value)

                if i == 100:
                    print("x=",x,i,output[0])

                #x += 4


            if (i>=76 and i<=121 and (i!=100 or i!=109)):
                output = struct.unpack('B', data[x:x+1])

                #tyre temperature
                #if i>=76 and i<80:
                    #print(i,output[0])

                #tyre wear
                #if i>=80 and i<84:
                    #print(i,output[0])

                #tyre compund
                #if i==84:
                    #print(i,output[0])

                #brake bias (bilanciamento frenata)
                #if i==85:
                    #print(i,output[0])

                #fuel mix
                #if i==86:
                    #print(i,output[0])

                #current lap valid
                #if i==87:
                    #print(i,output[0])

                #front wing damage
                #if i==92 or i==93:
                    #print(i,output[0])

                #rear wing damage
                #if i==94:
                    #print(i,output[0])

                #engine damage
                #if i==95:
                    #print(i,output[0])

                #gear box damage
                #if i==96:
                    #print(i,output[0])


                #print(i,output[0])
                x += 1


            i += 1
