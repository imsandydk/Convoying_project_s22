import carla
LEAD_VEHICLE_SPEED = 13  #mps
LEAD_X_INIT = -379.6
LEAD_Y_INIT = -17.6
LEAD_Z_INIT = 2.0
LEAD_X_INIT_END = -379.6
LEAD_Y_INIT_END = 0
LEAD_Z_INIT_END = 2.0
INIT_ROUTE = [carla.libcarla.Location(x=LEAD_X_INIT, y=LEAD_Y_INIT, z=0),carla.libcarla.Location(x=LEAD_X_INIT_END, y=LEAD_Y_INIT_END, z=0)]
BUFFER_LEN = 6