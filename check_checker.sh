#!/bin/bash

if [ -z "$(ls -A /home/adem/Desktop/burdamisin)" ]
then
    echo "bos"
    exit 0
else
    cat /home/adem/Desktop/burdamisin
    exit 1

fi
