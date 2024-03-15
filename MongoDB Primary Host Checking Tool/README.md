This script is prepared to find the primary one among your multiple mongodb servers and dynamically update the proxy configuration. It works by adding it to the cronjob and allows you to update the configuration with short interruptions. 

When the script runs, it tries to connect to the structure in the domain you wrote in and writes the primary server to a file.

If it makes a change in this file, it notices this and reloads the nginx service. If it has not made any changes, it does not touch it. 

I also added the sample nginx configuration so that dynamic changes can be made.
