#!/usr/bin/env sh

pid=$1
address=$2
window=`xdotool search qemu 2>/dev/null | tail -n1`

rm -r ./captures
mkdir ./captures

xdotool windowactivate "$window"

for i in {000..270}; do
    xdotool key Left
    sleep 0.05
    xdotool key Left
    sleep 0.05
    spectacle -aebno "captures/img$i.png"
    wait
    sudo ./skip_level "$pid" "$address" &>/dev/null
    echo "$i done"
done

for i in {000..270}; do
    file="./captures/img$i.png"
    convert "$file" -fill "#000" -opaque "#a9a9a9" "$file"
    convert "$file" -fill "#000" -opaque "#ffffff" "$file"
    convert "$file" -fill "#000" -opaque "#ff0000" "$file"
    convert "$file" -fill "#000" -opaque "#add8e6" "$file"
    echo "done $i"
done

echo "sticking all together"
convert +append ./captures/img*.png out.png
