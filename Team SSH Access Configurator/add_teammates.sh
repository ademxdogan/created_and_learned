#!/bin/bash

# An array containing usernames and their corresponding public SSH keys
declare -A USERS_AND_KEYS=(
    ["id"]="pub-key"
    # You can add more users and keys here
)

# Loop through each user
for user in "${!USERS_AND_KEYS[@]}"; do
    echo "Creating user: $user"
    # Create the user if it doesn't exist
    id -u "$user" &>/dev/null || sudo useradd -m -s /bin/bash "$user"

    # Create the .ssh directory and authorized_keys file to add the user's key
    sudo mkdir -p /home/"$user"/.ssh
    echo "${USERS_AND_KEYS[$user]}" | sudo tee -a /home/"$user"/.ssh/authorized_keys > /dev/null

    # Set the correct permissions
    sudo chmod 700 /home/"$user"/.ssh
    sudo chmod 600 /home/"$user"/.ssh/authorized_keys
    sudo chown -R "$user":"$user" /home/"$user"/.ssh

    # Add the user to the sudo group
    sudo usermod -aG sudo "$user"

    echo "SSH key added for user $user and added to the sudo group."
done

echo "All users created, SSH keys added, and added to the sudo group."
