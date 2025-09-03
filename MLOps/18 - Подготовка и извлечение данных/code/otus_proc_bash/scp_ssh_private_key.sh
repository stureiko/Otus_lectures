vm_name=$1

YC_USER=osipov
YC_PROXY_VM_PUBLIC_IP=$(
    yc compute instance get $vm_name \
        --format json | jq -r .network_interfaces[0].primary_v4_address.one_to_one_nat.address
)

log "Proxy VM public IP: $YC_PROXY_VM_PUBLIC_IP"

scp ~/.ssh/yandex_cloud $YC_USER@$YC_PROXY_VM_PUBLIC_IP:~/.ssh/dataproc

log "SSH private key copied to proxy VM"