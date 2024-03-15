#!/bin/bash

# Kullanıcı adları ve karşılık gelen public SSH anahtarlarını içeren bir dizi
declare -A USERS_AND_KEYS=(
    ["id"]=["pub-key"]
       # Daha fazla kullanıcı ve anahtar ekleyebilirsiniz
)

# Her kullanıcı için döngü
for user in "${!USERS_AND_KEYS[@]}"; do
    echo "Kullanıcı oluşturuluyor: $user"
    # Kullanıcıyı oluştur (eğer mevcut değilse)
    id -u "$user" &>/dev/null || sudo useradd -m -s /bin/bash "$user"

    # Kullanıcının anahtarını eklemek için .ssh dizinini ve authorized_keys dosyasını oluştur
    sudo mkdir -p /home/"$user"/.ssh
    echo "${USERS_AND_KEYS[$user]}" | sudo tee -a /home/"$user"/.ssh/authorized_keys > /dev/null

    # Doğru izinleri ayarla
    sudo chmod 700 /home/"$user"/.ssh
    sudo chmod 600 /home/"$user"/.ssh/authorized_keys
    sudo chown -R "$user":"$user" /home/"$user"/.ssh

    # Kullanıcıyı sudo grubuna ekle
    sudo usermod -aG sudo "$user"

    echo "Kullanıcı $user için SSH anahtarı eklendi ve sudo grubuna eklendi."
done

echo "Tüm kullanıcılar oluşturuldu, SSH anahtarları eklendi ve sudo grubuna eklendi."
