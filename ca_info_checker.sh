/usr/bin/bash
output_file="/tmp/certificateds"
domains="/tmp/fulllinks"
# Clear the output file at the beginning of the script
> "$output_file"

# Read each line in the file
while read -r line; do
    # Skip lines with wildcard domains
    if [[ "$line" == *"www.*."* ]]; then
        echo "Skipping wildcard domain: $line"
        continue
    fi

    # Get the certificate information for the website, with a 5-second timeout
    cert_info=$(timeout 5 bash -c "echo | openssl s_client -connect '$line:443' -showcerts 2>/dev/null")

    # Check if the timeout command succeeded
    if [ $? -eq 0 ]; then
        # Extract the CA information
        ca_info=$(echo "$cert_info" | openssl x509 -noout -issuer 2>/dev/null)

        # Check if the CA information is empty
        if [ -z "$ca_info" ]; then
            echo "No CA information found for $line"
        else
            # Print and write the CA information to the output file
            echo "CA for $line: $ca_info"
            echo "CA for $line: $ca_info" >> "$output_file"
        fi
    else
        # Print a timeout message
        echo "Timeout occurred for $line"
    fi
done < $domains
