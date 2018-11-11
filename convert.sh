#!/bin/bash

ext=".wav"

for i in ./Songs_mp3/*; do
	ffmpeg -i "${i}" ./Songs_Wav/"${i:12:-4}".wav
done
