
ssh -i ~/path/to/key/private user@global-ip-address-vm

# cd with dockerfile folder
docker build -t docker-user/repo:tag .

docker push docker-user/repo:tag

docker run -p 80:8080 -d --rm --name otusflask docker-user/repo:tag

# This command is used to run a Docker container with the name "otusflask" and expose port 80 on the host machine, which will be mapped to port 5000 in the container. The container will be run in detached mode (-d) and will be automatically removed (--rm) when it is stopped. 

# The image used for this container is "docker-user/repo:tag". This is likely a custom image created by the user "farruh7" for their Otus course project. 

# Overall, this command will start a Docker container running a Flask web application on port 5000 inside the container, which can be accessed on port 80 of the host machine


# ufw легче открыть доступ
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT

sudo iptables -t filter -A INPUT -p tcp -s 8.8.8.8 --sport 53 -d 192.168.1.1 -j ACCEPT

