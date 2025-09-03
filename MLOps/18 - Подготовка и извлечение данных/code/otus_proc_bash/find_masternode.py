"""Script to find the masternode in a cluster."""

import sys
import json

instances_list = json.load(sys.stdin)

for instance in instances_list:
    labels = instance.get("labels")

    if labels is None:
        continue

    role = labels.get("subcluster_role")
    if role == "masternode":
        print(instance.get("fqdn"))
        break
