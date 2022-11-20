#!/bin/bash

VERSION="0.9.3"

for file in deepspeech-${VERSION}-models.{pbmm,scorer}; do
  if [ ! -f "./${file}" ]; then
    echo "${file} does not exist"
    curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v${VERSION}/${file}
  fi
done

