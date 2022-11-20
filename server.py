import os
import json
import logging
import sys

import stt

from flask import Flask
from flask_cors import CORS
from flask import request

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(level=logging.INFO)

base_dir = os.path.dirname(__file__)
app = Flask(__name__)
CORS(app)


@app.errorhandler(Exception)
def _(error):
    import traceback
    logging.error(traceback.format_exc())
    return json.dumps({'error': error.__str__()}), 510, {'ContentType': 'application/javascript'}


@app.route('/', methods=['GET'])
def index():
    return '<html><body>STT</body></html>', 200, {'ContentType': 'text/html'}


# curl -X POST -F "file=@sample/1284-1180-0010.wav" http://localhost/api/v1/stt
@app.route('/api/v1/stt', methods=['POST'])
def convert_speech_to_text():

    if 'file' in request.files:
        file = request.files['file']
        data = file.stream.read()

        if data is None or len(data) < 4:
            return json.dumps({'error': 'invalid file in POST'}), 510, {'ContentType': 'application/javascript'}

        job_id = stt.get_job_uuid()
        input_file = os.path.join('/tmp/', job_id)
        with open(input_file, 'wb') as writer:
            writer.write(data)

        # convert wav to right format
        output_file = os.path.join('/tmp/', job_id + '.wav')
        if not stt.process_input_audio(input_file=input_file, output_file=output_file):
            return json.dumps({'error': 'could not convert file'}), 510, {'ContentType': 'application/javascript'}

        # change bytes back to text
        text = stt.extract_text_from_speech(output_file)
        return json.dumps({'text': text}), 200, {'ContentType': 'application/javascript'}

    else:
        return json.dumps({'error': 'no file in POST'}), 510, {'ContentType': 'application/javascript'}


if __name__ == '__main__':
    logging.info("!!! RUNNING in TEST/DEBUG mode, not PRODUCTION !!!")
    app.run(port=8080)
