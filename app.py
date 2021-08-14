from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import argparse
import discoverhue

app = Flask(__name__)


@app.route('/discover', methods=['GET'])
def discover():
    try:
        if request.method == 'GET':
            found = discoverhue.find_bridges()
            for bridge in found:
                print(' Bridge ID {br} at {ip}'.format(br=bridge, ip=found[bridge]))
            return make_response(jsonify({'response': 'Done!'}), 200)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description="Stressor Test Platform API")
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
