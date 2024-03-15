#!/usr/local/bin/bash

# Sunucuların IP adreslerini veya hostname'lerini bir dizi içinde tanımlayın
servers=("server1" "server2")

# Kopyalanacak script dosyasının yolu
script_path="/usr/home/adem/hardware_error.sh"

# Hedef dizin (sunucularda script'in kopyalanacağı yer)
target_dir="/usr/lib/nagios/plugins/"

# NRPE konfigürasyon dosyasının yolu
nrpe_cfg="/etc/nagios/nrpe.cfg"

# Komut adı (nrpe.cfg içinde tanımlanacak)
command_name="check_hardwares"
for server in "${servers[@]}"; do
    echo "Processing $server..."
    
    # Script'i sunucuya kopyala
    
    scp "$script_path" "$server:/home/adem/"
		ssh "$server" "sudo mv hardware_error.sh $target_dir/$(basename $script_path)"
    # Script'in izinlerini çalıştırılabilir yap
    ssh "$server" "sudo chmod +x $target_dir/$(basename $script_path)"

    # NRPE konfigürasyon dosyasını düzenle
    ssh "$server" "echo 'command[$command_name]=$target_dir/$(basename $script_path)' | sudo tee -a $nrpe_cfg > /dev/null"
    
    # NRPE servisini yeniden başlat (Değişikliklerin etkinleşmesi için)
    ssh "$server" "sudo systemctl restart nagios-nrpe-server"
    
    echo "Done with $server"
done


echo "All servers processed."
