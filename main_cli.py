#!/usr/bin/python3
import sys
from netspeed import NetSpeed


if len(sys.argv) < 2:
    print(
    """Usage:
        info -- show the information of your net speed
         up  -- speed up
        down -- slow down""")
else:
    my_netspeed = NetSpeed()
    if sys.argv[1] == "info":
        print("SpeedUp: %s\nNormal speed: %s %s\nSpeedup speed: %s Mbps\nLeft time: %sh"
              % (bool(my_netspeed.status), my_netspeed.old_speed, my_netspeed.old_speed_unit_name,
                 my_netspeed.new_speed, my_netspeed.hours))
    elif sys.argv[1] == "up":
        if my_netspeed.hours == 0:
            print("Warning: Do not have any speedup time, speedup may failed!")

        status = my_netspeed.speed_up()
        if status:
            print("Speed up successfully.")
        else:
            print("Speed up failed!")
            sys.exit(1)
    elif sys.argv[1] == "down":
        status = my_netspeed.speed_down()
        if status:
            print("Slow down successfully.")
        else:
            print("Slow down failed!")
            sys.exit(1)
