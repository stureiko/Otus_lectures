yc compute instance create \
    --preemptible \
    --ssh-key=$HOME/.ssh/id_ed25519.pub \
    --memory=16GB \
    --cores=4 \
    --zone=ru-central1-b \
    --name=stureiko-otus-inst-1 \
    --network-interface subnet-name=stureiko-otus,nat-ip-version=ipv4