yc compute instance create \
    --preemptible \
    --ssh-key=$HOME/.ssh/id_ed25519.pub \
    --memory=16GB \
    --cores=4 \
    --zone=ru-central1-b \
    --name=stureiko-otus-inst-1 \
    --create-boot-disk image-folder-id=standard-images,image-family=ubuntu-2204-lts \
    --network-interface subnet-name=default-ru-central1-b,nat-ip-version=ipv4