#! /usr/bin/env python
import psutil
import json
import socket
import datetime
import time

from opensearchpy import OpenSearch



def get_cpu_info():
    now =  datetime.datetime.utcnow()
    time = now.strftime("%Y-%m-%dT%H:%M:%S") + ".%03d" % (now.microsecond / 1000) + "Z"
    cpu_dict={"user":"", "nice":"", "system":"", "idle":"", "iowait":"","hostname":str(socket.gethostname()), "@timestamp":time}
    tp = psutil.cpu_times_percent()
    timepercentage_info = dict(enumerate(tp))  #user, nice, system, idle, iowait, irq=, softirq, steal, guest, guest_nice
    for i in (range(len(timepercentage_info))):
        if i == 0:
            cpu_dict["user"] = timepercentage_info[i]
        elif i == 1:
            cpu_dict["nice"] = timepercentage_info[i]
        elif i == 2:
            cpu_dict["system"] = timepercentage_info[i]
        elif i == 3:
            cpu_dict["idle"] = timepercentage_info[i]    
        elif i == 4:
            cpu_dict["iowait"] = timepercentage_info[i]
      
    json_output=json.dumps(cpu_dict)
    
    return json_output    




###################################################################
###################################################################
###################################################################
################### For OpenSearch ################################
###################################################################
###################################################################
###################################################################

host = 'xxx.xxx.xxx.xxx'
port = 9200
auth = ('admin', 'admin')

client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    http_auth = auth,
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False
)

index_name = 'cpuusage_py'


def create_index(index_name):

    index_body = {
  'settings': {
    'index': {
      'number_of_shards': 4
    }
  }
}
    response = client.indices.create(index_name, body=index_body)
    print('\nCreating index:')
    print(response)

def upload_doc():
    response = client.index(
        index = index_name,
        body = output,
        refresh = True,
    )
    print('\nAdding document:')
    print(response)

while True: 
    time.sleep(1)
    output = get_cpu_info()
    upload_doc()
