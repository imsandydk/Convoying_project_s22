import carla
LEAD_VEHICLE_SPEED = 37  #mph 
LEAD_X_INIT = -379.6
LEAD_Y_INIT = -17.6
LEAD_Z_INIT = 2.0
LEAD_X_INIT_END = -379.6
LEAD_Y_INIT_END = 0
LEAD_Z_INIT_END = 2.0
INIT_ROUTE = [carla.libcarla.Location(x=LEAD_X_INIT, y=LEAD_Y_INIT, z=0),carla.libcarla.Location(x=LEAD_X_INIT_END, y=LEAD_Y_INIT_END, z=0)]
convoy = None
SPEED_REG = True
def get_convoy_config(convoy_len):
    print("convoy_len:",convoy_len)
    if convoy_len == 2:
        convoy = {
            'buffer_len': 6,
            'KP': 1.0,
            'KI': 1.0,
            'KD': 0.1,
            'distance_to_stop': 30,
            'max_speed': 100
        }
    elif convoy_len == 3:
        convoy = {
            'buffer_len': 6,
            'KP': 1.0,
            'KI': 1.0,
            'KD': 0.1,
            'distance_to_stop': 30,
            'max_speed': 80
        }
    elif convoy_len == 4:
        convoy = {
            'buffer_len': 6,
            'KP': 1.0,
            'KI': 1.0,
            'KD': 0.1,
            'distance_to_stop': 25,
            'max_speed': 80
        }
    elif convoy_len == 5:
        convoy = {
            'buffer_len': 6,
            'KP': 0.5,
            'KI': 0.0,
            'KD': 0.0,
            'distance_to_stop': 20,
            'max_speed': 70
        }
    elif convoy_len == 6:
        convoy = {
            'buffer_len': 6,
            'KP': 1.0,
            'KI': 1.0,
            'KD': 0.1,
            'distance_to_stop': 15,
            'max_speed': 70
        }
    return convoy