import subprocess
import time
import json

log_file = "/var/log/host_tasima"

def log(message):
    with open(log_file, "a") as logf:
        logf.write(message + "\n")

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    log(f"Running command: {command}\nOutput: {result.stdout}\nError: {result.stderr}")
    return result

def get_host_input(prompt):
    return input(prompt)

def get_vms_on_host(host):
        command = f"openstack server list --all-projects --host {host} --power-state running -f json"
        result = run_command(command)
        log(f"VMs JSON: {result.stdout}")  
        return result.stdout

def parse_vm_ids(vms_json):
       
        if not vms_json.strip():
            log("No VMs found or empty JSON returned.")
            return {}
        try:
            vms = json.loads(vms_json)
            return {vm['ID']: vm for vm in vms}
        except json.JSONDecodeError as e:
            log(f"Error decoding JSON: {e}")
            raise


def parse_vm_ids(vms_json):
    
    vms = json.loads(vms_json)
    return {vm['ID']: vm for vm in vms}

def should_migrate_vm(vm_id):
    command = f"openstack server show {vm_id} -f json"
    result = run_command(command)
    try:
        vm_info = json.loads(result.stdout)
        if vm_info.get("image") == "N/A (booted from volume)":
            log(f"VM {vm_id} is booted from volume and will not be migrated.")
            return False
        return True
    except json.JSONDecodeError as e:
        log(f"Error decoding JSON for VM {vm_id}: {e}")
        return False

def migrate_vm(vm_id, target_host):
    if should_migrate_vm(vm_id):
        command = f"nova live-migration {vm_id} {target_host}"
        run_command(command)
        check_migration_status(vm_id, target_host)

def check_migration_status(vm_id, target_host):
    while True:
        command = f"openstack server show {vm_id} -f json"
        result = run_command(command)
        vm_info = result.stdout
        
        
        vm_info = json.loads(vm_info)
        
        
        vm_info = json.loads(vm_info)
        task_state = vm_info.get("OS-EXT-STS:task_state")
        vm_state = vm_info.get("OS-EXT-STS:vm_state")
        current_host = vm_info.get("OS-EXT-SRV-ATTR:host")
        
        if task_state == "migrating":
            log(f"VM {vm_id} is still migrating. Waiting...")
            time.sleep(60)
        elif vm_state == "error":
            log(f"VM {vm_id} migration encountered an error. Stopping script.")
            raise Exception("Migration error")
        elif current_host == target_host:
            log(f"VM {vm_id} successfully migrated to {target_host}.")
            break

def main():
    log("Starting host migration script")

    bosalacak_host = get_host_input("Bosaltmak istediginiz hostu girin: ")
    doldurulacak_host = get_host_input("Tasiyacaginiz hostu girin: ")

    vms_json = get_vms_on_host(bosalacak_host)
    migrate_edilecek_vmler = parse_vm_ids(vms_json)

    for vm_id in migrate_edilecek_vmler:
        migrate_vm(vm_id, doldurulacak_host)
        check_migration_status(vm_id, doldurulacak_host)

    log("Host migration script completed")

if __name__ == "__main__":
    main()
