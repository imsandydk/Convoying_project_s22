

# ==============================================================================
# -- Convoying Project ---
# ==============================================================================


import glob
import os
import sys

try:
    sys.path.append(glob.glob('./carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass


# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================


import carla

from carla import ColorConverter as cc

import argparse
import collections
import datetime
import logging
import math
import random
import re
import weakref
try:
    import numpy as np
except ImportError:
    raise RuntimeError('cannot import numpy, make sure numpy package is installed')

   
# ==============================================================================
# -- main() --------------------------------------------------------------------
# ==============================================================================


def main():
    
    try:
        #Create a client and connect to server 
        client = carla.Client('localhost', 2000)

        #Once the client is created, set its time-out. This limits all networking operations so that these don't block the client forever. An error will be returned if connection fails
        client.set_timeout(20.0)
        
        #The client can also get a list of available maps to change the current one. This will destroy the current world and create a new one
        world = client.load_world('Town06')
        print(client.get_available_maps())

        #Set weather
        weather = carla.WeatherParameters(
        cloudiness=40.0,
        precipitation=30.0,
        sun_altitude_angle=20.0)

        world.set_weather(weather)

        print(world.get_weather())

        # Retrieve a snapshot of the world at current frame.

        # world_snapshot = world.get_snapshot()

    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')


if __name__ == '__main__':

    main()
