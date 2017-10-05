#http://forums.codemasters.com/discussion/53139/f1-2017-d-box-and-udp-output-specification/
#http://forums.codemasters.com/discussion/46726/d-box-and-udp-telemetry-information

from tkinter import *
import socket
import struct

UDP_IP = "127.0.0.1"
UDP_PORT = 20777

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

mph_to_kmh = 2.239*1.60934

dict = {
    'globalTime' : '0',
    'globalTime_minutes' : '0',
    'globalTime_seconds' : '0',
    'globalTime_milles' : '0',
    'lapTime' : '0',
    'lapTime_minutes' : '0',
    'lapTime_seconds' : '0',
    'lapTime_milles' : '0',
    'lapDistance' : '0',
    'speed' : '0',
    'throttle' : '0',
    'steer' : '0',
    'brake' : '0',
    'gear' : '0',
    'lap' : '0',
    'engineRate' : '0',
    'carPosition' : '0',
    'drs' : '0',
    'fuelInTank' : '0',
    'fuelCapacity' : '0',
    'inPit' : '0',
    'sector' : '0',
    'sector1' : '0',
    'sector2' : '0',
    'sector3' : '0',
    'brakesTemp_rl' : '0',
    'brakesTemp_rr' : '0',
    'brakesTemp_fl' : '0',
    'brakesTemp_fr' : '0',
    'tyrePress_r' : '0',
    'tyrePress_f' : '0',
    'totalLaps' : '0',
    'trackSize' : '0',
    'lastLapTime' : '0',
    'lastLapTime_minutes' : '0',
    'lastLapTime_seconds' : '0',
    'lastLapTime_milles' : '0',
    'sessionType' : '0',
    'trackNumber' : '0',
    'flag' : '0',
    'era' : '0',
    'engineTemp' : '0'
}



while True:
    gui = Tk()
    gui.title("F1Telemetry")
    gui.geometry("300x200")
    var = StringVar()
    var.set(dict['speed'])
    label_speed = Label(gui,textvariable=var).pack()

    print(dict['speed'])
    data, addr = sock.recvfrom(1237)

    i = 0
    x = 0

    if data:
        while (i <= 121):
            if (i<=71):
                output = struct.unpack('f', data[x:x+4])

                #global Time
                if i == 0:
                    dict['globalTime'] = output[0]
                    dict['globalTime_minutes'] = int(dict['globalTime']//60)
                    dict['globalTime_seconds'] = int(dict['globalTime']-(60*dict['globalTime_minutes']))
                    dict['globalTime_milles'] = '{:03d}'.format(int((dict['globalTime']-(dict['globalTime_seconds']+(dict['globalTime_minutes']*60)))*1000))

                #current lap Time
                if i == 1:
                    dict['lapTime'] = output[0]
                    dict['lapTime_minutes'] = int(dict['lapTime']//60)
                    dict['lapTime_seconds'] = int(dict['lapTime']-(60*dict['lapTime_minutes']))
                    dict['lapTime_milles'] = '{:03d}'.format(int((dict['lapTime']-(dict['lapTime_seconds']+(dict['lapTime_minutes']*60)))*1000))

                #distance of the current Lap
                if i == 2:
                    dict['lapDistance'] = int(output[0])

                #current speed
                if i == 7:
                    dict['speed'] = int(output[0]*mph_to_kmh)

                #current throttle in percentage
                if i == 29:
                    dict['throttle'] = int(output[0]*100)

                #current steer (-99=left, 0=center, 100=right)
                if i == 30:
                    dict['steer'] = int(output[0]*100)

                #current bracke in percentage
                if i == 31:
                    dict['brake'] = int(output[0]*100)

                #current gear (0=R, 1=N, 2=1...)
                if i == 33:
                    dict['gear'] = int(output[0])

                #current lap
                if i == 36:
                    dict['lap'] = int(output[0]+1)

                #current engine Rate
                if i == 37:
                    dict['engineRate'] = int(output[0])

                #current car position
                if i == 39:
                    dict['carPosition'] = int(output[0])

                if i == 42:
                    dict['drs'] = output[0]

                if i == 45:
                    dict['fuelInTank'] = output[0]

                if i == 46:
                    dict['fuelCapacity'] = output[0]

                if i == 47:
                    dict['inPit'] = output[0]

                if i == 48:
                    dict['sector'] = int(output[0] + 1)

                if i == 49 and output[0]!=0:
                    dict['sector1'] = '{:.3f}'.format(output[0])

                if i == 50 and output[0]!=0:
                    dict['sector2'] = '{:.3f}'.format(output[0])

                #if int(dict['sector1'])!=0 and int(dict['sector2'])!=0 and int(dict['lapDistance'])<=100:
                    #dict['sector3'] = '{:.3f}'.format(float(dict['lastLapTime']) - float(dict['sector1']) - float(dict['sector2']))

                if i == 51:
                    dict['brakesTemp_rl'] = '{:06.2f}'.format(output[0])
                if i == 52:
                    dict['brakesTemp_rr'] = '{:06.2f}'.format(output[0])
                if i == 53:
                    dict['brakesTemp_fl'] = '{:06.2f}'.format(output[0])
                if i == 54:
                    dict['brakesTemp_fr'] = '{:06.2f}'.format(output[0])

                if i == 56:
                    dict['tyrePress_r'] = output[0]
                if i == 57:
                    dict['tyrePress_f'] = output[0]

                #DA MODIFICARE
                '''if i == 59:
                    dict['teaminfo_value']
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
                                print("TEAM = MCLAREN 1991")'''

                if i == 60:
                    dict['totalLaps'] = int(output[0])

                if i == 61:
                    dict['trackSize'] = int(output[0])

                if i == 62:
                    dict['lastLapTime'] = output[0]
                    dict['lastLapTime_minutes'] = int(dict['lastLapTime']//60)
                    dict['lastLApTime_seconds'] = int(dict['lastLapTime']-(60*dict['lastLapTime_minutes']))
                    dict['lastLApTime_milles'] = '{:03d}'.format(int((dict['lastLapTime']-(dict['lastLApTime_seconds']+(dict['lastLapTime_minutes']*60)))*1000))

                if i == 66:
                    dict['sessionType'] = output[0]

                if i == 68:
                    dict['trackNumber'] = output[0]

                if i == 69:
                    dict['flag'] = output[0]

                if i == 70:
                    dict['era'] = int(output[0])

                if i == 71:
                    dict['engineTemp'] = '{:06.2f}'.format(output[0])

                x += 4


            '''if (i>=76 and i<=121 and (i!=100 or i!=109)):
                output = struct.unpack('B', data[x:x+1])

                #tyre temperature
                if i>=76 and i<80:
                    print(i,output[0])

                #tyre wear
                if i>=80 and i<84:
                    print(i,output[0])

                #tyre compund
                if i==84:
                    print(i,output[0])

                #brake bias (bilanciamento frenata)
                if i==85:
                    print(i,output[0])

                #fuel mix
                if i==86:
                    print(i,output[0])

                #current lap valid
                if i==87:
                    print(i,output[0])

                #front wing damage
                if i==92 or i==93:
                    print(i,output[0])

                #rear wing damage
                if i==94:
                    print(i,output[0])

                #engine damage
                if i==95:
                    print(i,output[0])

                #gear box damage
                if i==96:
                    print(i,output[0])

                print(i,output[0])'''

            i += 1

    gui.mainloop()
