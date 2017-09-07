#http://forums.codemasters.com/discussion/53139/f1-2017-d-box-and-udp-output-specification/p7
#http://forums.codemasters.com/discussion/46726/d-box-and-udp-telemetry-information

import socket
import struct

UDP_IP = "127.0.0.1"
UDP_PORT = 20777

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    x = 0
    y = 4
    i = 0

    params = (
    "m_time", "m_lapTime", "m_lapDistance", "m_totalDistance", "m_x", "m_y", "m_z", "m_speed", "m_xv", "m_yv", "m_zv",
    "m_xr", "m_yr", "m_zr", "m_xd", "m_yd", "m_zd", "m_susp_pos_bl", "m_susp_pos_br", "m_susp_pos_fl",
    "m_susp_pos_fr", "m_susp_vel_bl", "m_susp_vel_br", "m_susp_vel_fl", "m_susp_vel_fr", "m_wheel_speed_bl",
    "m_wheel_speed_br", "m_wheel_speed_fl", "m_wheel_speed_fr", "m_throttle", "m_steer", "m_brake",
    "m_clutch", "m_gear", "m_gforce_lat", "m_gforce_lon", "m_lap", "m_engineRate", "m_sli_pro_native_support",
    "m_car_position", "m_kers_level", "m_kers_max_level", "m_drs", "m_traction_control", "m_anti_lock_brakes",
    "m_fuel_in_tank", "m_fuel_capacity", "m_in_pits", "m_sector", "m_sector1_time", "m_sector2_time",
    "m_brakes_temp[4]", "m_wheels_pressure[4]", "m_tea", "m_info", "m_total_laps", "m_track_size",
    "m_last_lap_time", "m_max_rpm", "m_idle_rpm", "m_max_gears", "m_sessionType", "m_drsAllowed", "m_track_number",
    "m_vehicleFIAFlags")

    while (i <= 55):
        data, addr = sock.recvfrom(1280)
        output = struct.unpack('f', data[x:y]) # 4 bytes at a time
        print (i, params[i], output[0])
        i = i + 1
        if (i >= 55):
            x = 0
            y = 4
            i = 0
        else:
            x = y + 1
            y = x + 4
