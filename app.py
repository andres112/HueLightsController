from flask import Flask
from flask_cors import CORS
import argparse

app = Flask(__name__)

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
