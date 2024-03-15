#!/bin/bash

# Dünün ve bugünün tarihlerini al (örn: Mar 13, Mar 14)
yesterday=$(date --date="yesterday" +"%b %d")
today=$(date +"%b %d")

# /var/log/kern.log dosyasında [Hardware Error] içeren ve son 1 gün içindeki satırları bul
grep -E "($yesterday|$today).*\[Hardware Error\]" /var/log/kern.log > /tmp/hardware_errors.log

# Eğer dosya boş değilse, hata bulundu
if [ -s /tmp/hardware_errors.log ]; then
    echo "Son 1 gün içinde [Hardware Error] bulundu:"
    cat /tmp/hardware_errors.log
    exit 1
else
    echo "Son 1 gün içinde [Hardware Error] bulunamadı."
    exit 0
fi
