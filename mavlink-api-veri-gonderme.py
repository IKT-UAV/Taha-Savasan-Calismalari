from pymavlink import mavutil
import time

# Define global variables
iha_batarya = None
iha_yonelme = None


# Function to handle MAVLink messages
def handle_message(msg):
    global iha_batarya, iha_yonelme
    if msg.get_type() == 'GLOBAL_POSITION_INT':
        iha_enlem = msg.lat / 1e7
        iha_boylam = msg.lon / 1e7
        iha_irtifa = msg.alt / 1000  # Convert to meters
        #print(f"iha_enlem: {iha_enlem}, iha_boylam: {iha_boylam}, iha_irtifa: {iha_irtifa}")

    elif msg.get_type() == 'ATTITUDE':
        iha_dikilme = msg.pitch * 180 / 3.14159
        iha_yonelme = msg.yaw * 180 / 3.14159
        iha_yatis = msg.roll * 180 / 3.14159
        #print(f"iha_dikilme: {iha_dikilme}, iha_yonelme: {iha_yonelme}, iha_yatis: {iha_yatis}")

    elif msg.get_type() == 'BATTERY_STATUS':
        iha_batarya = {msg.battery_remaining}
        #print(f"iha_batarya: {iha_batarya}")

    elif msg.get_type() == 'HEARTBEAT':
        base_mode = msg.base_mode
        autopilot_enabled = base_mode & mavutil.mavlink.MAV_MODE_FLAG_AUTO_ENABLED
        #print(f"iha_otonom: {bool(autopilot_enabled)}")
    elif msg.get_type() == 'SYSTEM_TIME':
        timestamp = msg.time_unix_usec
        #print(f"timestamp: {timestamp}")


print(iha_yonelme,iha_batarya)
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
