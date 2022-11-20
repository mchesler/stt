import os
import subprocess
import uuid

def get_job_uuid():
    return uuid.uuid4().__str__()

def process_input_audio(input_file, output_file):
    with open(os.devnull, "w") as f_null:
        subprocess.call(["/usr/bin/ffmpeg", "-i", input_file, "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000", output_file], stdout=f_null, stderr=f_null)

    if not os.path.isfile(output_file):
        return False

    return True

def extract_text_from_speech(input_file):
    deepspeech_executable = '/usr/local/bin/deepspeech'
    model_file = '/app/deepspeech-0.9.3-models.pbmm'
    scorer_file = '/app/deepspeech-0.9.3-models.scorer'

    process = subprocess.Popen(
        [
            deepspeech_executable,
            "--model", model_file,
            "--scorer", scorer_file,
            "--audio", input_file
        ],
        stdout=subprocess.PIPE)

    out, err = process.communicate()
    if err is not None:
        raise ValueError(err)

    return out.decode("utf-8").strip()
