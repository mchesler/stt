FROM ubuntu:20.04

ENV LANG="C.UTF-8"

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        python3 \
        python3-pip \
        python3-setuptools \
        libasound2-plugins \
        libsox-fmt-all \
        libsox-dev \
        ffmpeg \
        sox \
        wget \
        && \
    apt-get clean

COPY . /app
WORKDIR /app

RUN pip3 --no-cache-dir install --upgrade pip
RUN pip3 install -r requirements.txt

# setup native client
RUN wget -O native_client.tar.xz https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/native_client.amd64.cpu.linux.tar.xz
RUN tar xvfJ native_client.tar.xz
RUN cp lib* /usr/local/lib/
RUN cp deepspeech /usr/local/bin/
RUN cp generate_trie /usr/local/bin/
RUN ldconfig

# Download pre-trained English model files
RUN ./dl.sh

EXPOSE 80

RUN pip3 --no-cache-dir install gunicorn

# command line version
# CMD ["./stt.py"]

CMD ["gunicorn", "--access-logfile=-", "-t", "120", "-b", "0.0.0.0:80", "server:app"]
