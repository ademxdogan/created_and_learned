#!/bin/bash

# Target domain and port

DOMAIN="[sxxx.xxx.xxx.xx](<http://xxx.xxx.xxx.xx/>)"
PORT="443"

# Certificate expiration date check

expiration_date=$(openssl s_client -servername $DOMAIN -connect $DOMAIN:$PORT </dev/null 2>/dev/null | openssl x509 -enddate -noout | awk -F= '{print $2}')
expiration_epoch=$(date -d "$expiration_date" +%s)
current_epoch=$(date +%s)
remaining_days=$(( (expiration_epoch - current_epoch) / 86400 ))

if [ $remaining_days -le 7 ]; then

  # Certificate renewal command

  echo "The certificate will expire in $remaining_days days. Sending renewal command..."

  # Add the command to renew the certificate here

  certbot certonly --dns-rfc2136 --dns-rfc2136-credentials /etc/letsencrypt/certbot.ini --non-interactive --agree-tos -m [xxx.xxx.xxx.xx](<mailto:xxx.xxx.xxx.xx>) -d "xxx.xxx.xxx.xx" -d [xxx.xxx.xxx.xx](<xxx.xxx.xxx.xx/>)
  /bin/systemctl restart ceph-radosgw.target || /etc/init.d/radosgw restart ||  /bin/systemctl restart radosgw.service
  echo "IMPORTANT EMAIL" | mail -s "Check if the radosgw certificate has been expired" [xxx.xxx.xxx.xx](<mailto:xxx.xxx.xxx.xx>)
else
  echo "The certificate will not expire in $remaining_days days. No need for renewal."
fi

