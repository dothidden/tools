#!/bin/sh

# this takes the first value that is smaller than its predecessor

f="n00bz{Y0u_60D_1t_60d4Mm17_1m_Pr0Ud_0f"
s=""

while :; do
    prev=0
    for i in {30..127}; do
        hex="\x$(printf "%x" $i)"
        s="${f}${hex}\x00"
        result=$(echo -ne ${s} | \
            valgrind --tool=callgrind ./ccode 2>&1 | \
            grep -Eo ": [0-9]+$" | \
            cut -c 3-)

        echo -en "\rtrying: $s"
        if [ "$result" -lt "$prev" ]; then
            f="${f}${hex}"
            echo -e "\n$f"
            break;
        fi
        prev="$result"

        rm -r callgrind* 2>/dev/null
        rm -r vgcore* 2>/dev/null
    done
done
