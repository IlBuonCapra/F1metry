#http://forums.codemasters.com/discussion/53139/f1-2017-d-box-and-udp-output-specification/
#http://forums.codemasters.com/discussion/46726/d-box-and-udp-telemetry-information

import socket
import struct

UDP_IP = "127.0.0.1"
UDP_PORT = 20777

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

mph_to_kmh = 2.239*1.60934

while True:
    data, addr = sock.recvfrom(1237)

    i = 0
    x = 0
    y = 4

    gear = False
    speed = False
    throttle = False
    brake = False
    drs = False
    engineRate = False
    inPit = False
    carPosition = False

    if data:
        #print("RICEVENDO DATI")
        while (i <= 60):
            output = struct.unpack('f', data[x:y])

            if gear and i == 33:    #gear
                if output[0] == 0:
                    print ("MARCIA = R")
                elif output[0] == 1:
                    print ("MARCIA = N")
                else:
                    print ("MARCIA =", int(output[0]-1))

            if speed and i == 7:  #speed
                print ("VELOCITA' = ", round(output[0]*mph_to_kmh, 1))

            if throttle and i == 29:    #throttle
                 print ("ACCELERAZIONE = ", output[0]*100)

            if brake and i == 31:   #brake
                print ("FRENO = ", output[0]*100)

            if drs and i == 42:     #drs
                if output[0] == 0:
                    print("DRS CHIUSO")
                elif output[0] == 1:
                    print("DRS APERTO")
                else:
                    print("DRS STATO SCONOSCIUTO")

            if engineRate and i == 37:
                print("NUMERO DI GIRI = ", round(output[0],2))

            if inPit and i == 47:
                if output[0] == 2:
                    print("AI BOX")
                elif output[0] == 1:
                    print("NELLA PIT LANE")
                elif output[0] == 0:
                    print("IN PISTA")

            if carPosition and i == 39:
                print("POSIZIONE = ",output[0])




            i += 1
            x += 4
            y += 4

    # print (i, round(output[0]*2.272, 7))
