#!/usr/bin/bash

while getopts i:o:f aflag; do
    case $aflag in
            i) input=$OPTARG;;
            o) output=$OPTARG;;
            f) format=$OPTARG;;
    esac
done


echo "Splitting audio...";
spleeter separate -i ${input} -p spleeter:2stems -o ${output};
echo "Done Splitting Audio..."
echo "instrumental chosen...";

output_folder=$(basename $(echo ${input%.*}))

echo "vocal chosen...";

ffmpeg -i audio/${output_folder}/vocals.wav audio/${output_folder}/${output_folder}_vocal.mp3
ffmpeg -i audio/${output_folder}/accompaniment.wav audio/${output_folder}/${output_folder}_instrumental.mp3


status=$?

rm audio/${output_folder}/accompaniment.wav
rm audio/${output_folder}/vocals.wav

if [ ${format} = "vocals" ]; then
    rm audio/${output_folder/${output_folder}_instrumental.mp3}
elif [ ${format} = "instrumental" ]; then
    rm audio/${output_folder/${output_folder}_vocals.mp3}
fi

FILE=audio/${output_folder}/${output_folder}_vocals.mp3
if [ -f "$FILE" ]; then
    echo "Vocals successfully written.";
fi

FILE=audio/${output_folder}/${output_folder}_instrumental.mp3
if [ -f "$FILE" ]; then
    echo "Instrumental successfully written."
fi
echo "Exiting program..."
