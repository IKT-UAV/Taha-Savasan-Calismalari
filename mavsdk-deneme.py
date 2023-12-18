from pymavlink import mavutil
import time
import json

# Function to handle MAVLink messages
def handle_message(msg):
    data = {
        "takim_numarasi": 1,
        "iha_hiz": 28,
        "iha_kilitlenme": 1,
        "hedef_merkez_X": 300,
        "hedef_merkez_Y": 230,
        "hedef_genislik": 30,
        "hedef_yukseklik": 43,
        "gps_saati": {"saat": 11, "dakika": 38, "saniye": 37, "milisaniye": 654}
    }

    if msg.get_type() == 'GLOBAL_POSITION_INT':
        data["iha_enlem"] = msg.lat / 1e7
        data["iha_boylam"] = msg.lon / 1e7
        data["iha_irtifa"] = msg.alt / 1000  # Convert to meters

    elif msg.get_type() == 'ATTITUDE':
        data["iha_dikilme"] = msg.pitch * 180 / 3.14159
        data["iha_yonelme"] = msg.yaw * 180 / 3.14159
        data["iha_yatis"] = msg.roll * 180 / 3.14159

    elif msg.get_type() == 'BATTERY_STATUS':
        data["iha_batarya"] = msg.battery_remaining

    elif msg.get_type() == 'HEARTBEAT':
        base_mode = msg.base_mode
        data["iha_otonom"] = bool(base_mode & mavutil.mavlink.MAV_MODE_FLAG_AUTO_ENABLED)

    elif msg.get_type() == 'SYSTEM_TIME':
        timestamp = msg.time_unix_usec
        data["timestamp"] = timestamp

    print(json.dumps(data, indent=2))

# Connect to the Pixhawk Cube Orange (assuming it is connected to COM20)
the_connection = mavutil.mavlink_connection('com20')

# Wait for the first heartbeat
the_connection.wait_heartbeat()

# Set up message intervals using MAV_CMD_SET_MESSAGE_INTERVAL
the_connection.mav.command_long_send(
    the_connection.target_system,
    the_connection.target_component,
    mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
    0,  # Confirmation
    mavutil.mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT,  # Message ID
    1000000,  # Microseconds between messages (1 Hz)
    0, 0, 0, 0, 0  # Parameters 4-9 (not used for this command)
)

the_connection.mav.command_long_send(
    the_connection.target_system,
    the_connection.target_component,
    mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
    0,  # Confirmation
    mavutil.mavlink.MAVLINK_MSG_ID_ATTITUDE,  # Message ID
    1000000,  # Microseconds between messages (1 Hz)
    0, 0, 0, 0, 0  # Parameters 4-9 (not used for this command)
)

# Main loop to continuously handle messages
try:
    while True:
        msg = the_connection.recv_match()
        if msg:
            handle_message(msg)
except KeyboardInterrupt:
    pass
finally:
    the_connection.close()
