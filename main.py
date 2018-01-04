#http://forums.codemasters.com/discussion/53139/f1-2017-d-box-and-udp-output-specification/
#http://forums.codemasters.com/discussion/46726/d-box-and-udp-telemetry-information

import socket
import struct
import tkinter as tk
import threading

UDP_IP = "127.0.0.1"
UDP_PORT = 20777

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

mph_to_kmh = 2.239*1.60934

panel = tk.Tk()


def create_dictionaries():
    global game_values, index_converter

    game_values = {
        'totalTime' : tk.StringVar(),
        'lapTime' : tk.StringVar(),
        'lapDistance' : tk.StringVar(),
        'totalDistance' : tk.StringVar(),
        'speed' : tk.StringVar(),
        'wheelSpeed_rl' : tk.StringVar(),
        'wheelSpeed_rr' : tk.StringVar(),
        'wheelSpeed_fl' : tk.StringVar(),
        'wheelSpeed_fr' : tk.StringVar(),
        'throttle' : tk.StringVar(),
        'steer' : tk.StringVar(),
        'brake' : tk.StringVar(),
        'clutch' : tk.StringVar(),
        'gear' : tk.StringVar(),
        'gforceLat' : tk.StringVar(),
        'gforceLon' : tk.StringVar(),
        'lap' : tk.StringVar(),
        'engineRate' : tk.StringVar(),
        'sliProNativeSupport' : tk.StringVar(),
        'carPosition' : tk.StringVar(),
        'kersLevel' : tk.StringVar(),
        'kersMaxLevel' : tk.StringVar(),
        'drs' : tk.StringVar(),
        'tractionControl' : tk.StringVar(),
        'antiLockBrakes' : tk.StringVar(),
        'fuelInTank' : tk.StringVar(),
        'fuelCapacity' : tk.StringVar(),
        'inPit' : tk.StringVar(),
        'sector' : tk.StringVar(),
        'sector1' : tk.StringVar(),
        'sector2' : tk.StringVar(),
        'brakesTemp_rl' : tk.StringVar(),
        'brakesTemp_rr' : tk.StringVar(),
        'brakesTemp_fl' : tk.StringVar(),
        'brakesTemp_fr' : tk.StringVar(),
        'tyrePress_rl' : tk.StringVar(),
        'tyrePress_rr' : tk.StringVar(),
        'tyrePress_fl' : tk.StringVar(),
        'tyrePress_fr' : tk.StringVar(),
        'teamInfo' : tk.StringVar(),
        'totalLaps' : tk.StringVar(),
        'trackSize' : tk.StringVar(),
        'lastLapTime' : tk.StringVar(),
        'maxRpm' : tk.StringVar(),
        'idleRpm' : tk.StringVar(),
        'maxGears' : tk.StringVar(),
        'sessionType' : tk.StringVar(),
        'drsAllowed' : tk.StringVar(),
        'trackNumber' : tk.StringVar(),
        'flag' : tk.StringVar(),
        'era' : tk.StringVar(),
        'engineTemp' : tk.StringVar(),
        'gforceVert' : tk.StringVar(),
    }

    index_converter = {
        value : key
        for key, value in zip(
            game_values.keys(),
            [
             0,  1,  2,  3,  7,  25, 26, 27, 28,
             29, 30, 31, 32, 33, 34, 35, 36, 37,
             38, 39, 40, 41, 42, 43, 44, 45, 46,
             47, 48, 49, 50, 51, 52, 53, 54, 55,
             56, 57, 58, 59, 60, 61, 62, 63, 64,
             65, 66, 67, 68, 69, 70, 71, 72
            ]
        )
    }


def run_gamedata_panel():
    global panel, game_values
    panel.title("F1Metry GamePanel")
    panel.geometry("320x720")
    labels = [tk.Label(panel, text=l).grid(row=x, column=0) for l, x in zip(game_values.keys(), range(len(game_values.keys())))]
    values = [tk.Label(panel, textvariable=v).grid(row=x, column=1) for v, x in zip(game_values.values(), range(len(game_values.values())))]
    panel.mainloop()


def mainloop():
    while True:
        data, addr = sock.recvfrom(1289)

        if data:
            x = 0
            for i in range(0,72):
                value =  struct.unpack('f', data[x:x+4])[0]
                if i in index_converter.keys():
                    if i != 7:
                        game_values[index_converter[i]].set(str(value))
                    else:
                        game_values[index_converter[i]].set(str(value * mph_to_kmh))
                x+=4


if __name__ == "__main__":
    create_dictionaries()
    collector = threading.Thread(target=mainloop)
    collector.start()
    run_gamedata_panel()
