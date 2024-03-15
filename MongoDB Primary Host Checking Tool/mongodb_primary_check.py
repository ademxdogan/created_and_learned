import pymongo
import sys
import os
import logging

# Configure the log file
log_file = '/var/log/mongocheckerV2.log'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

# MongoDB Replica Set connection string
replica_set_uri = "mongodb://secondary1:27017,secondary2:27017,primary:27017/?replicaSet=rs0"

# Connect to MongoDB
client = pymongo.MongoClient(replica_set_uri)

# Get the status of the replica set
status = client.admin.command("replSetGetStatus")

# Find the primary server
for member in status['members']:
    if member['stateStr'] == 'PRIMARY':
        primary_host = member['name'].split(':')[0]
        break
else:
    logging.error("Primary server not found!")
    sys.exit(1)

# Write the address of the primary server to a file
config_file_path = '/etc/nginx/mongodb_primary.conf'
new_content = f"server {primary_host}:27017;\n"

# Check the current content of the file
try:
    with open(config_file_path, 'r') as file:
        current_content = file.read()
except FileNotFoundError:
    current_content = ""

# If the content has changed, update the file and reload Nginx
if new_content != current_content:
    with open(config_file_path, 'w') as file:
        file.write(new_content)
    logging.info(f"Primary server: {primary_host}")
    logging.info("Configuration file updated. Reloading Nginx...")
    os.system('sudo nginx -s reload')
else:
    logging.info("Configuration file is up to date. No need to reload Nginx.")
'''
nginx.conf;
load_module /usr/lib/nginx/modules/ngx_stream_module.so;
events {
    worker_connections 1024;
}


stream {
    upstream mongodb_primary {
        include /etc/nginx/mongodb_primary.conf;
    }

    server {
        listen 27017;
        proxy_pass mongodb_primary;
        proxy_connect_timeout 1s;
    }
}
'''
