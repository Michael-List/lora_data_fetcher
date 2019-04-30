#!/usr/bin/env bash

pipe=/dev/shm/receive_fifo

trap "rm -f ${pipe}" EXIT

if [[ ! -p ${pipe} ]]; then
    mkfifo ${pipe}
fi

while true; do
    printf "1) Send valid data\n2) Send false data\n3) Quit\n"
    read NUMBER

    case ${NUMBER} in
         1)
            echo "01;21.16;954.98;46.88;260;256;0.00;7;" > ${pipe}
            printf "Wrote valid data to $pipe\n"
            printf "Blocks until data was read\n"
            ;;
         2)
            echo "aaa;21.16;954.a;4d.88;260;256;0.00;7;" > ${pipe}
            printf "Wrote false data to $pipe\n"
            printf "Blocks until data was read\n"
            ;;
         3)
            printf "Exiting, goodbye!\n"
            exit;
            ;;
    esac

    printf "-----------------------------------------"
done