# Получаем RQDN мастер ноды
yc compute instance list --format json | jq -r . \
    | python3 find_masternode.py
