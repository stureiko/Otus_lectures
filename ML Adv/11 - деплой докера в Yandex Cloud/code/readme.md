# Add user to docker group

```bash
sudo groupadd docker  # create docker group
sudo usermod -aG docker $USER  # add current user to docker group
```
