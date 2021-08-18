from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import argparse
import ipaddress
import discoverhue
from phue import Bridge
from helpers import *
import os
import pygame

app = Flask(__name__)

pygame.init()
pygame.mixer.init()


@app.route('/discover_bridge', methods=['GET'])
def discover():
    try:
        if request.method == 'GET':
            found = discoverhue.find_bridges()
            for bridge in found:
                print(' Bridge ID {br} at {ip}'.format(br=bridge, ip=found[bridge]))
            return make_response(jsonify(found), 200)
    except Exception as e:
        print(e)


@app.route('/control_lights', methods=['POST'])
def control():
    try:
        # Validate if valid ip_address
        ipaddress.ip_address(request.json['ip'])

        if request.method == 'POST':
            # Create bridge object
            bridge = Bridge(request.json['ip'])
            bridge.connect()
            status = bridge.get_api()
            if any('error' in i for i in status):
                return make_response(jsonify(status), 500)

            lights = bridge.get_group('lab', 'lights')
            current_status = bridge.get_group('lab')['state']['any_on']

            # Light parameters command
            [r, g, b] = request.json['rgb'] \
                if ('rgb' in request.json and request.json['rgb'] is not None) \
                else [255, 255, 255]
            on = request.json['on'] if ('on' in request.json and request.json['on'] is not None) else None
            bri = request.json['bri'] if ('bri' in request.json and request.json['bri'] is not None) else 254
            sat = request.json['sat'] if ('sat' in request.json and request.json['sat'] is not None) else 254
            lights = request.json['lights'] \
                if ('lights' in request.json and request.json['lights'] is not None) \
                else lights
            light_ids = [int(light) for light in lights]  # get the light_id in int format

            xy = rgbTohue(r, g, b)
            command = {'bri': getValue(bri), 'xy': xy, "sat": getValue(sat)}

            if on is not None and current_status != on:
                command['on'] = on

            # execute commands in lights
            bridge.set_light(light_ids, command, transitiontime=0)

            print(bridge.get_api())  # Get the status after change

            return make_response(jsonify({'message': 'command executed succesfully'}), 200)
    except ValueError:
        print(f"IP address {request.json['ip']} is not valid")
    except Exception as e:
        print(e)



if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description="Phillips hue lights and music control")
    PARSER.add_argument('--debug', action='store_true',
                        help="Use flask debug/dev mode with file change reloading")
    ARGS = PARSER.parse_args()

    PORT = 5555

    # cross origen support
    CORS(app)

    if ARGS.debug:
        print("Running in debug mode")
        app.run(host='0.0.0.0', port=PORT, debug=True)
    else:
        app.run(host='0.0.0.0', port=PORT, debug=False)
