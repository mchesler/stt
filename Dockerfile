FROM ubuntu:20.04

ENV LANG="C.UTF-8"
ENV DEBIAN_FRONTEND="noninteractive"

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

# Download native client and pre-trained English model files
RUN ./dl.sh

# setup native client
RUN tar xvfJ native_client.amd64.cpu.linux.tar.xz
RUN cp lib* /usr/local/lib/
RUN cp deepspeech /usr/local/bin/
RUN ldconfig

EXPOSE 80

RUN pip3 --no-cache-dir install gunicorn

# command line version
# CMD ["./stt.py"]

CMD ["gunicorn", "--access-logfile=-", "-t", "120", "-b", "0.0.0.0:80", "server:app"]
