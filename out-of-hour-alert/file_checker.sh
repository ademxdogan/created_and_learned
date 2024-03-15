#!/usr/local/bin/bash

if [ -z "$(ls -A /home/kimgirdi)" ]
then
    echo "bos"
    exit 0
else
    cat /home/kimgirdi
    exit 1

fi
