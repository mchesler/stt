#!/bin/bash

VERSION="0.9.3"

for file in native_client.amd64.cpu.linux.tar.xz deepspeech-${VERSION}-models.{pbmm,scorer}; do
  if [ ! -f "./${file}" ]; then
    echo "${file} does not exist"
    curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v${VERSION}/${file}
  fi
done
