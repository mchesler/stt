import os
import json
import logging
import sys
import subprocess
import uuid

from flask import Flask
from flask_cors import CORS
from flask import request

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(level=logging.INFO)

base_dir = os.path.dirname(__file__)
app = Flask(__name__)
CORS(app)

deepspeech_executable = '/usr/local/bin/deepspeech'
model_file = '/app/models/deepspeech-0.9.3-models.pbmm'
scorer_file = '/app/models/deepspeech-0.9.3-models.scorer'
sound_file = '/app/output.wav'


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

        job_id = uuid.uuid4().__str__()
        sound_file = os.path.join('/tmp/', job_id)
        with open(sound_file, 'wb') as writer:
            writer.write(data)

        # convert wav to right format
        stt_sound_file = os.path.join('/tmp/', job_id + '.wav')
        with open(os.devnull, 'w') as f_null:
            subprocess.call(["/usr/bin/ffmpeg", "-i", sound_file, "-acodec", "pcm_s16le",
                             "-ac", "1", "-ar", "16000", stt_sound_file], stdout=f_null, stderr=f_null)

        if not os.path.isfile(stt_sound_file):
            return json.dumps({'error': 'could not convert file'}), 510, {'ContentType': 'application/javascript'}

        process = subprocess.Popen([deepspeech_executable, "--model", model_file, "--scorer", scorer_file, "--audio", stt_sound_file],
                                    stdout=subprocess.PIPE)
        out, err = process.communicate()
        if err is not None:
            raise ValueError(err)

        # change bytes back to text
        text = out.decode("utf-8").strip()
        return json.dumps({'text': text}), 200, {'ContentType': 'application/javascript'}

    else:
        return json.dumps({'error': 'no file in POST'}), 510, {'ContentType': 'application/javascript'}


if __name__ == '__main__':
    logging.info("!!! RUNNING in TEST/DEBUG mode, not PRODUCTION !!!")
    app.run(port=8080)
