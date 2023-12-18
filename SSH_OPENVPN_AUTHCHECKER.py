#!/usr/bin/env python3
from datetime import datetime, timedelta
import re

last_hour_date_time = datetime.now() - timedelta(hours = 1)
one_hour =[]
ssh_login =[]
openvpn_login =[]
auth_log_path = "/var/log/auth.log"
openvpn_log_path = "/var/log/openvpn.log"


def readlog(path):
    read_log = []
    authlog = open(path, "r")
    read_log.append(authlog.read())
    read_log = read_log[0].split('\n')
    authlog.close()
    return read_log


def is_within_last_hour(log_entry):
    # Regular expression to match timestamp formats in auth.log and openvpn.log
    auth_log_pattern = r'^\w+\s+\d+\s+\d+:\d+:\d+'
    openvpn_log_pattern = r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}'

    auth_match = re.search(auth_log_pattern, log_entry)
    openvpn_match = re.search(openvpn_log_pattern, log_entry)

    if auth_match:
        timestamp_str = auth_match.group()
    elif openvpn_match:
        timestamp_str = openvpn_match.group()
    else:
        return False

    current_datetime = datetime.now()

    if auth_match:
        log_datetime = datetime.strptime(f"{current_datetime.year} {timestamp_str}", '%Y %b %d %H:%M:%S')
    else:
        log_datetime = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

    time_difference = current_datetime - log_datetime
    return time_difference <= timedelta(minutes=5)

# Check each log entry and print True if it's within the last hour, False otherwise
for entry in readlog(auth_log_path):
    
    if (is_within_last_hour(entry) == 1):
        one_hour.append(entry)

for entry in readlog(openvpn_log_path):
    
    if (is_within_last_hour(entry) == 1):
        one_hour.append(entry)    

for entry in one_hour:
    if "preauth" in entry:
        ssh_login.append(entry)
    elif "CN" in entry:
        openvpn_login.append(entry)

if len(ssh_login) or len(openvpn_login) != 0:
    with open('/home/kimgirdi', 'a') as f:
        for i in ssh_login:
            f.write(str(i))
            f.write('\n')
        for i in openvpn_login:
            f.write(str(i)) 
            f.write('\n')






