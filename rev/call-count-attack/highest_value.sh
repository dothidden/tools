#!/bin/sh

# this takes the highest value

f="uiuctf{ar3_y0u_4_r3al_vm_wh3r3_(gpt_g3n3r4t3d_th1s_f14g)"
s=""

while :; do
    now=0
    c=0
    for i in {30..127}; do
        hex="\x$(printf "%x" $i)"
        s="${f}${hex}"
        result=$(echo -ne ${s} | \
            valgrind --tool=callgrind ./chal program 2>&1 | \
            grep -Eo ": [0-9]+$" | \
            cut -c 3-)

        echo -en "\rtrying: $s"
        if [ "$result" -gt "$now" ]; then
            now="$result"
            c="${hex}"
        fi

        rm -r callgrind* 2>/dev/null
        rm -r vgcore* 2>/dev/null
    done
    f="${f}${c}"
done
