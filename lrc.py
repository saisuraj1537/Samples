from dronekit import connect, VehicleMode
import time
import math

# Connect to the Vehicle
vehicle = connect('/dev/serial0', baud=57600, wait_ready=True)  # Adjust connection if needed

def set_velocity(vx, vy, vz, duration):
    """
    Move the drone with the given velocity for the specified duration.
    vx: velocity in X direction (m/s)
    vy: velocity in Y direction (m/s)
    vz: velocity in Z direction (m/s) (positive downwards)
    duration: time in seconds
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0, 0, 0,  # Target system, component, frame
        0b0000111111000111,  # Mask: ignore all except velocity
        0, 0, 0,  # Position (not used)
        vx, vy, vz,  # Velocity (m/s)
        0, 0, 0,  # Acceleration (not used)
        0, 0  # Yaw, Yaw rate (not used)
    )
    
    for _ in range(int(duration * 10)):  # Send command multiple times per second
        vehicle.send_mavlink(msg)
        time.sleep(0.1)

def move_left(distance_cm, speed_mps=1.0):
    """
    Move the drone left (negative Y direction) by a given distance in cm.
    """
    distance_m = distance_cm / 100.0
    duration = distance_m / speed_mps  # Time required
    set_velocity(0, -speed_mps, 0, duration)

def move_right(distance_cm, speed_mps=1.0):
    """
    Move the drone right (positive Y direction) by a given distance in cm.
    """
    distance_m = distance_cm / 100.0
    duration = distance_m / speed_mps  # Time required
    set_velocity(0, speed_mps, 0, duration)

# Ensure the vehicle is in GUIDED mode
if vehicle.mode != VehicleMode("GUIDED"):
    vehicle.mode = VehicleMode("GUIDED")
    time.sleep(2)

print("Moving left 500 cm...")
move_left(500, 1.0)

print("Moving right 50 cm...")
move_right(50, 1.0)

print("Movement completed.")

# Close vehicle connection
vehicle.close()
