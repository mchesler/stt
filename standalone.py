#!/usr/bin/python3

import os
import sys

import uuid
import stt

# add this path to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__' :

    job_uuid = stt.get_job_uuid()
    input_file = f"/tmp/{job_uuid}.input.wav"
    output_file = f"/tmp/{job_uuid}.wav"

    # copy incoming audio to input
    with open(input_file, 'wb') as writer:
        writer.write(sys.stdin.buffer.read())

    # convert wav to right format
    if not stt.process_input_audio(input_file=input_file, output_file=output_file):
        print("Could not convert file")


    text = stt.extract_text_from_speech(output_file)

    print(text)
