import logging
from operator import attrgetter
from argparse import ArgumentParser
import sys
import time

import robart

def main():
    parser = ArgumentParser(description="A cli wrapper for the Robart MyVacBot API")
    parser.add_argument("--ip", dest="ip", help="ip address of the robot")
    parser.add_argument("--scan", dest="scan", help="ip address of the robot")

    cmd = parser.add_argument_group("Commands")
    cmd.add_argument("--status", action="store_true", dest="cmd_status", help="command: clean")
    cmd.add_argument("--clean", action="store_true", dest="cmd_clean", help="command: clean")
    cmd.add_argument("--stop", action="store_true", dest="cmd_stop", help="command: stop")
    cmd.add_argument("--home", action="store_true", dest="cmd_home", help="command: go home")
    cmd.add_argument("--test", dest="cmd_test", help="command: test")

    ip = ''
    ips = []
    
    args = parser.parse_args()

    command_entered = False

    rob = robart.Robart_MyVacBot('10.0.0.31', '10009')

    if args.ip:
        command_entered = False
        ip = args.ip
        rob.set_rest_url(ip)
        
    if args.scan:
        command_entered = True
        network = args.scan
        ips = robart.scan(network)
        if len(ips) > 0:
            print("Found robots at {}".format(ips))
            ip = ips[0]
            
    rob.set_rest_timeout(0.5, 3)
    rob.set_rest_url(ip)
    
    try:            
        rob.get_state()
        rob.get_robotid()
    except:
        print("No robot found")
        return
        
    
    if args.cmd_status:
        command_entered = True
        print('mode: {}, charging: {}, battery_level: {}'.format(rob._mode, rob._charging, rob._battery_level))
        print('name: {}, unique_id: {}, camlas_unique_id: {}, model: {}, firmware: {}'.format(rob._name, rob._unique_id, rob._camlas_unique_id, rob._model, rob._firmware))

    if args.cmd_clean:
        command_entered = True
        rob.set_clean()
    
    if args.cmd_stop:
        command_entered = True
        rob.set_stop()
        
    if args.cmd_home:
        command_entered = True
        rob.set_home()

    if args.cmd_test:
        command_entered = True
        rob.test(args.cmd_test)

    if not command_entered:
        parser.print_help()


def printEvents(eventList):
    for event in eventList:
        print(u"EventType: {} Data: {}".format(event["eventType"], event["data"]))


if __name__ == "__main__":
    main()
